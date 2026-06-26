-- Run this in Supabase SQL Editor (Dashboard → SQL Editor → New query → Run)

-- 1. Add barcode column to ai_extracted_products
ALTER TABLE ai_extracted_products
  ADD COLUMN IF NOT EXISTS barcode TEXT;

CREATE UNIQUE INDEX IF NOT EXISTS idx_ai_products_barcode_unique
  ON ai_extracted_products (barcode)
  WHERE barcode IS NOT NULL;

-- 2. Add barcode + source columns to product_submissions (for OFF imports)
ALTER TABLE product_submissions
  ADD COLUMN IF NOT EXISTS barcode TEXT,
  ADD COLUMN IF NOT EXISTS source  TEXT DEFAULT 'user';
