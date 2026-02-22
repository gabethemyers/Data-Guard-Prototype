-- Create the three schemas
CREATE SCHEMA IF NOT EXISTS staging;
CREATE SCHEMA IF NOT EXISTS validation;
CREATE SCHEMA IF NOT EXISTS canonical;

-- Grant permissions (for now, just to your user)
GRANT ALL ON SCHEMA staging TO gabriel;
GRANT ALL ON SCHEMA validation TO gabriel;
GRANT ALL ON SCHEMA canonical TO gabriel;
