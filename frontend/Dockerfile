# ==============================================================================
# SecureShare Frontend - Multi-stage Dockerfile
# ==============================================================================

# Stage 1: Builder
FROM node:18-alpine as builder

WORKDIR /build

# Copy package files
COPY package.json package-lock.json ./

# Install dependencies
RUN npm ci --only=production

# Copy source code
COPY . .

# Build application
RUN npm run build

# ==============================================================================
# Stage 2: Runtime (Nginx)
FROM nginx:1.25-alpine

# Security: Remove default nginx user and create custom one
RUN deluser nginx && \
    adduser -D -H -u 1000 -s /sbin/nologin nginx

# Copy built assets from builder
COPY --from=builder /build/dist /usr/share/nginx/html

# Copy custom nginx configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Security headers and hardening
RUN echo "server_tokens off;" > /etc/nginx/conf.d/security.conf

# Set ownership
RUN chown -R nginx:nginx /usr/share/nginx/html && \
    chown -R nginx:nginx /var/cache/nginx && \
    chown -R nginx:nginx /var/log/nginx && \
    chown -R nginx:nginx /etc/nginx/conf.d && \
    touch /var/run/nginx.pid && \
    chown -R nginx:nginx /var/run/nginx.pid

# Switch to non-root user
USER nginx

# Expose port
EXPOSE 80

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD wget --no-verbose --tries=1 --spider http://localhost/ || exit 1

CMD ["nginx", "-g", "daemon off;"]
