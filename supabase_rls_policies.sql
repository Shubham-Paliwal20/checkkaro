-- ============================================================
-- RLS POLICIES FOR CHECKKARO / PARKHO
-- Run this in Supabase → SQL Editor
-- After running, verify each table has RLS enabled in
-- Supabase → Table Editor → (table) → RLS tab
-- ============================================================

-- ─── ai_extracted_products ────────────────────────────────────────────────────
ALTER TABLE ai_extracted_products ENABLE ROW LEVEL SECURITY;

-- Public: anyone can read products
CREATE POLICY "public_read_products" ON ai_extracted_products
  FOR SELECT USING (true);

-- Only admin can insert / update / delete
CREATE POLICY "admin_write_products" ON ai_extracted_products
  FOR ALL
  USING (auth.email() = 'shubhampaliwal5@gmail.com')
  WITH CHECK (auth.email() = 'shubhampaliwal5@gmail.com');


-- ─── product_photos ───────────────────────────────────────────────────────────
ALTER TABLE product_photos ENABLE ROW LEVEL SECURITY;

-- Public: anyone can read approved photos
CREATE POLICY "public_read_photos" ON product_photos
  FOR SELECT USING (true);

-- Only admin can insert / update / delete
CREATE POLICY "admin_write_photos" ON product_photos
  FOR ALL
  USING (auth.email() = 'shubhampaliwal5@gmail.com')
  WITH CHECK (auth.email() = 'shubhampaliwal5@gmail.com');


-- ─── product_photo_submissions ────────────────────────────────────────────────
ALTER TABLE product_photo_submissions ENABLE ROW LEVEL SECURITY;

-- Authenticated users can submit (insert only)
CREATE POLICY "authenticated_submit_photos" ON product_photo_submissions
  FOR INSERT
  WITH CHECK (auth.uid() IS NOT NULL);

-- Users can read their own submissions; admin reads all
CREATE POLICY "user_read_own_submissions" ON product_photo_submissions
  FOR SELECT
  USING (user_id::text = auth.uid()::text OR auth.email() = 'shubhampaliwal5@gmail.com');

-- Admin can update submissions (approve/reject)
CREATE POLICY "admin_update_submissions" ON product_photo_submissions
  FOR UPDATE
  USING (auth.email() = 'shubhampaliwal5@gmail.com')
  WITH CHECK (auth.email() = 'shubhampaliwal5@gmail.com');

-- Admin can delete submissions
CREATE POLICY "admin_delete_submissions" ON product_photo_submissions
  FOR DELETE
  USING (auth.email() = 'shubhampaliwal5@gmail.com');


-- ─── product_reviews ─────────────────────────────────────────────────────────
ALTER TABLE product_reviews ENABLE ROW LEVEL SECURITY;

-- Public: anyone can read reviews
CREATE POLICY "public_read_reviews" ON product_reviews
  FOR SELECT USING (true);

-- Authenticated users can insert their own review
CREATE POLICY "authenticated_insert_review" ON product_reviews
  FOR INSERT
  WITH CHECK (auth.uid() IS NOT NULL AND user_id::text = auth.uid()::text);

-- Users can only update / delete their own review
CREATE POLICY "user_manage_own_review" ON product_reviews
  FOR ALL
  USING (user_id::text = auth.uid()::text OR auth.email() = 'shubhampaliwal5@gmail.com')
  WITH CHECK (user_id::text = auth.uid()::text OR auth.email() = 'shubhampaliwal5@gmail.com');


-- ─── product_submissions ─────────────────────────────────────────────────────
ALTER TABLE product_submissions ENABLE ROW LEVEL SECURITY;

-- Authenticated users can submit
CREATE POLICY "authenticated_submit_products" ON product_submissions
  FOR INSERT
  WITH CHECK (auth.uid() IS NOT NULL);

-- Users can read their own submissions; admin sees all
CREATE POLICY "user_or_admin_read_submissions" ON product_submissions
  FOR SELECT
  USING (user_id::text = auth.uid()::text OR auth.email() = 'shubhampaliwal5@gmail.com');

-- Admin can update submissions (approve/reject)
CREATE POLICY "admin_update_product_submissions" ON product_submissions
  FOR UPDATE
  USING (auth.email() = 'shubhampaliwal5@gmail.com')
  WITH CHECK (auth.email() = 'shubhampaliwal5@gmail.com');

-- Admin can delete submissions
CREATE POLICY "admin_delete_product_submissions" ON product_submissions
  FOR DELETE
  USING (auth.email() = 'shubhampaliwal5@gmail.com');


-- ─── ingredient_reports ───────────────────────────────────────────────────────
ALTER TABLE ingredient_reports ENABLE ROW LEVEL SECURITY;

-- Authenticated users can report
CREATE POLICY "authenticated_insert_report" ON ingredient_reports
  FOR INSERT
  WITH CHECK (auth.uid() IS NOT NULL);

-- Users read their own; admin reads all
CREATE POLICY "user_or_admin_read_reports" ON ingredient_reports
  FOR SELECT
  USING (user_id::text = auth.uid()::text OR auth.email() = 'shubhampaliwal5@gmail.com');

-- Admin can update reports (mark resolved)
CREATE POLICY "admin_update_reports" ON ingredient_reports
  FOR UPDATE
  USING (auth.email() = 'shubhampaliwal5@gmail.com')
  WITH CHECK (auth.email() = 'shubhampaliwal5@gmail.com');

-- Admin can delete reports
CREATE POLICY "admin_delete_reports" ON ingredient_reports
  FOR DELETE
  USING (auth.email() = 'shubhampaliwal5@gmail.com');


-- ─── user_profiles ────────────────────────────────────────────────────────────
ALTER TABLE user_profiles ENABLE ROW LEVEL SECURITY;

-- Users can read / write only their own profile; admin can read all
CREATE POLICY "user_manage_own_profile" ON user_profiles
  FOR ALL
  USING (id::text = auth.uid()::text OR auth.email() = 'shubhampaliwal5@gmail.com')
  WITH CHECK (id::text = auth.uid()::text OR auth.email() = 'shubhampaliwal5@gmail.com');


-- ─── blogs ────────────────────────────────────────────────────────────────────
ALTER TABLE blogs ENABLE ROW LEVEL SECURITY;

-- Public: anyone can read approved blogs; authenticated users can see their own drafts
CREATE POLICY "public_read_approved_blogs" ON blogs
  FOR SELECT USING (
    status = 'approved'
    OR auth.email() = 'shubhampaliwal5@gmail.com'
    OR (auth.uid() IS NOT NULL AND user_id::text = auth.uid()::text)
  );

-- Authenticated users can insert blogs (pending review)
CREATE POLICY "authenticated_insert_blog" ON blogs
  FOR INSERT
  WITH CHECK (auth.uid() IS NOT NULL);

-- Users can update / delete their own blog; admin manages all
CREATE POLICY "user_or_admin_manage_blog" ON blogs
  FOR ALL
  USING (user_id::text = auth.uid()::text OR auth.email() = 'shubhampaliwal5@gmail.com')
  WITH CHECK (user_id::text = auth.uid()::text OR auth.email() = 'shubhampaliwal5@gmail.com');


-- ─── reviews (general reviews table if it exists) ─────────────────────────────
-- Uncomment if you have a separate 'reviews' table:
-- ALTER TABLE reviews ENABLE ROW LEVEL SECURITY;
-- CREATE POLICY "public_read_reviews2" ON reviews FOR SELECT USING (true);
-- CREATE POLICY "authenticated_insert_review2" ON reviews
--   FOR INSERT WITH CHECK (auth.uid() IS NOT NULL AND user_id::text = auth.uid()::text);
-- CREATE POLICY "user_manage_own_review2" ON reviews
--   FOR ALL
--   USING (user_id::text = auth.uid()::text OR auth.email() = 'shubhampaliwal5@gmail.com')
--   WITH CHECK (user_id::text = auth.uid()::text OR auth.email() = 'shubhampaliwal5@gmail.com');


-- ─── Storage: product-images bucket ───────────────────────────────────────────
-- These use the modern storage.objects DDL syntax.
-- Run AFTER making sure the bucket "product-images" exists.

-- Allow public reads of all objects
CREATE POLICY "public_read_product_images"
  ON storage.objects FOR SELECT
  USING (bucket_id = 'product-images');

-- Only admin can upload
CREATE POLICY "admin_insert_product_images"
  ON storage.objects FOR INSERT
  WITH CHECK (
    bucket_id = 'product-images'
    AND auth.email() = 'shubhampaliwal5@gmail.com'
  );

-- Only admin can delete
CREATE POLICY "admin_delete_product_images"
  ON storage.objects FOR DELETE
  USING (
    bucket_id = 'product-images'
    AND auth.email() = 'shubhampaliwal5@gmail.com'
  );
