-- Migration: replace awareness_score with grade (A/B/C/D)
-- Run once in Supabase SQL editor

ALTER TABLE ai_extracted_products
  ADD COLUMN IF NOT EXISTS grade TEXT DEFAULT 'C' CHECK (grade IN ('A','B','C','D'));

-- Back-fill existing rows from awareness_score
UPDATE ai_extracted_products SET grade =
  CASE
    WHEN awareness_score >= 90 THEN 'A'
    WHEN awareness_score >= 75 THEN 'B'
    WHEN awareness_score >= 55 THEN 'C'
    ELSE 'D'
  END
WHERE grade = 'C' OR grade IS NULL;

-- Index for grade-based filtering
CREATE INDEX IF NOT EXISTS idx_ai_products_grade ON ai_extracted_products(grade);
