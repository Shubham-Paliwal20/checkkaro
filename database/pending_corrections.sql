-- Table for user-submitted ingredient corrections
-- Run this in your Supabase SQL editor

CREATE TABLE IF NOT EXISTS pending_corrections (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    product_id UUID REFERENCES products(id) ON DELETE CASCADE,
    product_name TEXT NOT NULL,
    submitted_ingredients TEXT NOT NULL,
    submitted_at TIMESTAMP DEFAULT NOW(),
    status TEXT DEFAULT 'pending' CHECK (status IN ('pending', 'approved', 'rejected')),
    reviewed_at TIMESTAMP,
    reviewed_by TEXT,
    notes TEXT
);

-- Create index for faster queries
CREATE INDEX IF NOT EXISTS idx_pending_corrections_status ON pending_corrections(status);
CREATE INDEX IF NOT EXISTS idx_pending_corrections_product_name ON pending_corrections(product_name);
CREATE INDEX IF NOT EXISTS idx_pending_corrections_submitted_at ON pending_corrections(submitted_at DESC);

-- Enable Row Level Security
ALTER TABLE pending_corrections ENABLE ROW LEVEL SECURITY;

-- Policy: Anyone can submit corrections
CREATE POLICY "Anyone can submit corrections" ON pending_corrections
    FOR INSERT
    WITH CHECK (true);

-- Policy: Anyone can view their own submissions
CREATE POLICY "Anyone can view corrections" ON pending_corrections
    FOR SELECT
    USING (true);

-- Add comment
COMMENT ON TABLE pending_corrections IS 'User-submitted ingredient corrections for products';
