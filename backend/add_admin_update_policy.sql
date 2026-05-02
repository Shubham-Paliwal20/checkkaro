-- Run this once in Supabase dashboard → SQL Editor
-- Allows the admin user to update ai_extracted_products directly from the frontend

-- Enable RLS if not already enabled (safe to run even if already enabled)
ALTER TABLE ai_extracted_products ENABLE ROW LEVEL SECURITY;

-- Allow admin to update products (needed for ingredient approval)
CREATE POLICY "Admin can update products"
ON ai_extracted_products
FOR UPDATE
USING (auth.jwt() ->> 'email' = 'shubhampaliwal5@gmail.com');

-- Allow everyone to read products (needed for product pages)
CREATE POLICY "Anyone can read products"
ON ai_extracted_products
FOR SELECT
USING (true);

-- Allow admin to insert products
CREATE POLICY "Admin can insert products"
ON ai_extracted_products
FOR INSERT
WITH CHECK (auth.jwt() ->> 'email' = 'shubhampaliwal5@gmail.com');
