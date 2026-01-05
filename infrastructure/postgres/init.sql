-- SecureShare - PostgreSQL Initialization Script

-- Enable required extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- Create database if not exists (already created by POSTGRES_DB env var)
-- This script runs after database creation

-- Set timezone to UTC
SET timezone = 'UTC';

-- Create initial schema
CREATE SCHEMA IF NOT EXISTS secureshare;

-- Grant privileges
GRANT ALL PRIVILEGES ON SCHEMA secureshare TO secureshare;

-- Log initialization
DO $$
BEGIN
  RAISE NOTICE 'SecureShare database initialized successfully';
END $$;
