#!/bin/bash

set -e

# Environment variables
DB_NAME=${POSTGRES_DB:-airflow_db}
DB_USER=${POSTGRES_USER:-airflow_user}
DB_PASS=${POSTGRES_PASSWORD:-airflow_pass}

# Create the database and user, and grant privileges
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" <<-EOSQL
    CREATE DATABASE $DB_NAME;
    CREATE USER $DB_USER WITH PASSWORD '$DB_PASS';
    GRANT ALL PRIVILEGES ON DATABASE $DB_NAME TO $DB_USER;

    -- PostgreSQL 15 requires additional privileges:
    \c $DB_NAME
    GRANT ALL ON SCHEMA public TO $DB_USER;
EOSQL

echo "Database $DB_NAME and user $DB_USER created with all privileges."
