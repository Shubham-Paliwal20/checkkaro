-- Add verdict and recommendation fields to products table
ALTER TABLE products 
ADD COLUMN IF NOT EXISTS verdict TEXT,
ADD COLUMN IF NOT EXISTS recommendation TEXT;

-- Add index for faster searches
CREATE INDEX IF NOT EXISTS idx_products_search_count ON products(search_count DESC);
