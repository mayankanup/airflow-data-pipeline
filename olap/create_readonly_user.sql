-- Read-only role for Metabase BI (Phase 5). Run on olap DB as postgres.
DO $$ BEGIN
  IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'metabase_reader') THEN
    CREATE ROLE metabase_reader LOGIN PASSWORD 'metabase_reader';
  END IF;
END $$;
GRANT CONNECT ON DATABASE olap TO metabase_reader;
GRANT USAGE ON SCHEMA public TO metabase_reader;
GRANT SELECT ON TABLE daily_sales_summary TO metabase_reader;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO metabase_reader;
