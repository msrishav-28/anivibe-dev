#!/bin/bash
# Database migration script

echo "🔄 Running database migrations..."

# Generate migration if needed
alembic revision --autogenerate -m "Auto-generated migration"

# Run migrations
alembic upgrade head

echo "✅ Migrations completed!"
