CREATE TABLE staging.batches (
    batch_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    batch_name VARCHAR(255) NOT NULL,
    imported_by VARCHAR(100) NOT NULL,
    imported_at TIMESTAMP NOT NULL DEFAULT NOW(),
    total_records INTEGER NOT NULL,
    status VARCHAR(50) NOT NULL DEFAULT 'pending',
    metadata JSONB,

    CONSTRAINT chk_status CHECK (status IN 
        ('pending', 'validating', 'pass', 'fail', 'partial', 'promoted'))
);

CREATE INDEX idx_batches_status ON staging.batches(status);
CREATE INDEX idx_batches_imported_at ON staging.batches(imported_at DESC);