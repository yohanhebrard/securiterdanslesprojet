"""
Rate Limiting Middleware
Protects against abuse using Redis-backed sliding window
"""
import time
from typing import Callable

from fastapi import Request, Response, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
import redis

from app.core.config import settings


class RateLimitMiddleware(BaseHTTPMiddleware):
    """
    Redis-backed rate limiting middleware

    Uses sliding window algorithm for accurate rate limiting:
    - Global: 100 requests per minute per IP
    - Upload: 10 requests per hour per IP
    - Download: 50 requests per hour per IP
    """

    def __init__(self, app):
        super().__init__(app)

        if settings.RATE_LIMIT_ENABLED:
            # Connect to Redis
            self.redis_client = redis.from_url(
                settings.REDIS_URL,
                decode_responses=True,
            )
        else:
            self.redis_client = None

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """Process request with rate limiting"""

        # Skip if rate limiting is disabled
        if not settings.RATE_LIMIT_ENABLED or self.redis_client is None:
            return await call_next(request)

        # Get client IP
        client_ip = request.client.host
        path = request.url.path

        # Define rate limit rules
        limits = []

        # Global rate limit (100 req/min)
        limits.append({
            "key": f"ratelimit:global:{client_ip}",
            "limit": settings.RATE_LIMIT_GLOBAL_PER_MINUTE,
            "window": 60,  # seconds
            "message": "Too many requests. Please try again later.",
        })

        # Upload-specific rate limit (10 req/hour)
        if "/upload" in path and request.method == "POST":
            limits.append({
                "key": f"ratelimit:upload:{client_ip}",
                "limit": settings.RATE_LIMIT_UPLOAD_PER_HOUR,
                "window": 3600,  # seconds
                "message": "Upload limit exceeded. Please try again later.",
            })

        # Download-specific rate limit (50 req/hour)
        if "/download" in path and request.method == "GET":
            limits.append({
                "key": f"ratelimit:download:{client_ip}",
                "limit": settings.RATE_LIMIT_DOWNLOAD_PER_HOUR,
                "window": 3600,  # seconds
                "message": "Download limit exceeded. Please try again later.",
            })

        # Check all rate limits
        current_time = int(time.time())

        for limit_config in limits:
            key = limit_config["key"]
            limit = limit_config["limit"]
            window = limit_config["window"]
            message = limit_config["message"]

            # Sliding window rate limit check
            try:
                # Remove expired entries (older than window)
                min_score = current_time - window
                self.redis_client.zremrangebyscore(key, 0, min_score)

                # Count requests in current window
                request_count = self.redis_client.zcard(key)

                if request_count >= limit:
                    # Rate limit exceeded
                    raise HTTPException(
                        status_code=429,
                        detail=message,
                        headers={"Retry-After": str(window)},
                    )

                # Add current request to sorted set
                self.redis_client.zadd(key, {str(current_time): current_time})

                # Set expiration on key (cleanup)
                self.redis_client.expire(key, window)

            except HTTPException:
                raise
            except Exception as e:
                # Log error but don't block request if Redis fails
                print(f"Rate limit check failed: {e}")

        # Process request
        response = await call_next(request)

        # Add rate limit headers
        response.headers["X-RateLimit-Limit"] = str(settings.RATE_LIMIT_GLOBAL_PER_MINUTE)

        return response
