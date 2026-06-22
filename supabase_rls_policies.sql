-- ============================================================
-- RLS POLICIES FOR CHECKKARO / PARKHO
-- Run this in Supabase → SQL Editor
-- Safe to re-run: existing policies are dropped before re-creating.
-- ============================================================

-- ─── ai_extracted_products ────────────────────────────────────────────────────
ALTER TABLE ai_extracted_products ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS "public_read_products"   ON ai_extracted_products;
DROP POLICY IF EXISTS "admin_write_products"   ON ai_extracted_products;

CREATE POLICY "public_read_products" ON ai_extracted_products
  FOR SELECT USING (true);

CREATE POLICY "admin_write_products" ON ai_extracted_products
  FOR ALL
  USING (auth.email() = 'shubhampaliwal5@gmail.com')
  WITH CHECK (auth.email() = 'shubhampaliwal5@gmail.com');


-- ─── product_photos ───────────────────────────────────────────────────────────
ALTER TABLE product_photos ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS "public_read_photos"   ON product_photos;
DROP POLICY IF EXISTS "admin_write_photos"   ON product_photos;

CREATE POLICY "public_read_photos" ON product_photos
  FOR SELECT USING (true);

CREATE POLICY "admin_write_photos" ON product_photos
  FOR ALL
  USING (auth.email() = 'shubhampaliwal5@gmail.com')
  WITH CHECK (auth.email() = 'shubhampaliwal5@gmail.com');


-- ─── product_photo_submissions ────────────────────────────────────────────────
-- Column that stores the submitter: user_id (uuid or text)
ALTER TABLE product_photo_submissions ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS "authenticated_submit_photos"  ON product_photo_submissions;
DROP POLICY IF EXISTS "user_read_own_submissions"    ON product_photo_submissions;
DROP POLICY IF EXISTS "admin_update_submissions"     ON product_photo_submissions;
DROP POLICY IF EXISTS "admin_delete_submissions"     ON product_photo_submissions;

CREATE POLICY "authenticated_submit_photos" ON product_photo_submissions
  FOR INSERT
  WITH CHECK (auth.uid() IS NOT NULL);

CREATE POLICY "user_read_own_submissions" ON product_photo_submissions
  FOR SELECT
  USING (user_id::text = auth.uid()::text OR auth.email() = 'shubhampaliwal5@gmail.com');

CREATE POLICY "admin_update_submissions" ON product_photo_submissions
  FOR UPDATE
  USING (auth.email() = 'shubhampaliwal5@gmail.com')
  WITH CHECK (auth.email() = 'shubhampaliwal5@gmail.com');

CREATE POLICY "admin_delete_submissions" ON product_photo_submissions
  FOR DELETE
  USING (auth.email() = 'shubhampaliwal5@gmail.com');


-- ─── product_reviews ─────────────────────────────────────────────────────────
-- Column that stores the reviewer: user_id
ALTER TABLE product_reviews ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS "public_read_reviews"        ON product_reviews;
DROP POLICY IF EXISTS "authenticated_insert_review" ON product_reviews;
DROP POLICY IF EXISTS "user_manage_own_review"      ON product_reviews;

CREATE POLICY "public_read_reviews" ON product_reviews
  FOR SELECT USING (true);

CREATE POLICY "authenticated_insert_review" ON product_reviews
  FOR INSERT
  WITH CHECK (auth.uid() IS NOT NULL AND user_id::text = auth.uid()::text);

CREATE POLICY "user_manage_own_review" ON product_reviews
  FOR ALL
  USING (user_id::text = auth.uid()::text OR auth.email() = 'shubhampaliwal5@gmail.com')
  WITH CHECK (user_id::text = auth.uid()::text OR auth.email() = 'shubhampaliwal5@gmail.com');


-- ─── product_submissions ─────────────────────────────────────────────────────
-- Column that stores the submitter: user_id
ALTER TABLE product_submissions ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS "authenticated_submit_products"       ON product_submissions;
DROP POLICY IF EXISTS "user_or_admin_read_submissions"      ON product_submissions;
DROP POLICY IF EXISTS "admin_update_product_submissions"    ON product_submissions;
DROP POLICY IF EXISTS "admin_delete_product_submissions"    ON product_submissions;

CREATE POLICY "authenticated_submit_products" ON product_submissions
  FOR INSERT
  WITH CHECK (auth.uid() IS NOT NULL);

CREATE POLICY "user_or_admin_read_submissions" ON product_submissions
  FOR SELECT
  USING (user_id::text = auth.uid()::text OR auth.email() = 'shubhampaliwal5@gmail.com');

CREATE POLICY "admin_update_product_submissions" ON product_submissions
  FOR UPDATE
  USING (auth.email() = 'shubhampaliwal5@gmail.com')
  WITH CHECK (auth.email() = 'shubhampaliwal5@gmail.com');

CREATE POLICY "admin_delete_product_submissions" ON product_submissions
  FOR DELETE
  USING (auth.email() = 'shubhampaliwal5@gmail.com');


-- ─── ingredient_reports ───────────────────────────────────────────────────────
-- Column that stores the reporter: user_id
ALTER TABLE ingredient_reports ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS "authenticated_insert_report"  ON ingredient_reports;
DROP POLICY IF EXISTS "user_or_admin_read_reports"   ON ingredient_reports;
DROP POLICY IF EXISTS "admin_update_reports"         ON ingredient_reports;
DROP POLICY IF EXISTS "admin_delete_reports"         ON ingredient_reports;

CREATE POLICY "authenticated_insert_report" ON ingredient_reports
  FOR INSERT
  WITH CHECK (auth.uid() IS NOT NULL);

CREATE POLICY "user_or_admin_read_reports" ON ingredient_reports
  FOR SELECT
  USING (user_id::text = auth.uid()::text OR auth.email() = 'shubhampaliwal5@gmail.com');

CREATE POLICY "admin_update_reports" ON ingredient_reports
  FOR UPDATE
  USING (auth.email() = 'shubhampaliwal5@gmail.com')
  WITH CHECK (auth.email() = 'shubhampaliwal5@gmail.com');

CREATE POLICY "admin_delete_reports" ON ingredient_reports
  FOR DELETE
  USING (auth.email() = 'shubhampaliwal5@gmail.com');


-- ─── user_profiles ────────────────────────────────────────────────────────────
-- Primary key column: id (uuid matching auth.uid())
ALTER TABLE user_profiles ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS "user_manage_own_profile" ON user_profiles;

CREATE POLICY "user_manage_own_profile" ON user_profiles
  FOR ALL
  USING (id::text = auth.uid()::text OR auth.email() = 'shubhampaliwal5@gmail.com')
  WITH CHECK (id::text = auth.uid()::text OR auth.email() = 'shubhampaliwal5@gmail.com');


-- ─── blogs ────────────────────────────────────────────────────────────────────
-- Column that stores the author: author_id  (NOT user_id)
ALTER TABLE blogs ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS "public_read_approved_blogs"  ON blogs;
DROP POLICY IF EXISTS "authenticated_insert_blog"   ON blogs;
DROP POLICY IF EXISTS "user_or_admin_manage_blog"   ON blogs;

CREATE POLICY "public_read_approved_blogs" ON blogs
  FOR SELECT USING (
    status = 'approved'
    OR auth.email() = 'shubhampaliwal5@gmail.com'
    OR (auth.uid() IS NOT NULL AND author_id::text = auth.uid()::text)
  );

CREATE POLICY "authenticated_insert_blog" ON blogs
  FOR INSERT
  WITH CHECK (auth.uid() IS NOT NULL);

CREATE POLICY "user_or_admin_manage_blog" ON blogs
  FOR ALL
  USING (author_id::text = auth.uid()::text OR auth.email() = 'shubhampaliwal5@gmail.com')
  WITH CHECK (author_id::text = auth.uid()::text OR auth.email() = 'shubhampaliwal5@gmail.com');


-- ─── reviews (homepage testimonials table — separate from product_reviews) ─────
-- Column that stores the reviewer: user_id
ALTER TABLE reviews ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS "public_read_approved_reviews"   ON reviews;
DROP POLICY IF EXISTS "authenticated_insert_review_hp" ON reviews;
DROP POLICY IF EXISTS "user_manage_own_review_hp"      ON reviews;
DROP POLICY IF EXISTS "admin_manage_all_reviews"       ON reviews;

-- Public: only approved reviews are readable; restrict columns via application layer
CREATE POLICY "public_read_approved_reviews" ON reviews
  FOR SELECT USING (is_approved = true OR auth.email() = 'shubhampaliwal5@gmail.com');

-- Authenticated users can insert their own review
CREATE POLICY "authenticated_insert_review_hp" ON reviews
  FOR INSERT
  WITH CHECK (auth.uid() IS NOT NULL AND user_id::text = auth.uid()::text);

-- Users can update / delete only their own review; admin manages all
CREATE POLICY "user_manage_own_review_hp" ON reviews
  FOR UPDATE
  USING (user_id::text = auth.uid()::text OR auth.email() = 'shubhampaliwal5@gmail.com')
  WITH CHECK (user_id::text = auth.uid()::text OR auth.email() = 'shubhampaliwal5@gmail.com');

-- Admin can delete any review
CREATE POLICY "admin_manage_all_reviews" ON reviews
  FOR DELETE
  USING (auth.email() = 'shubhampaliwal5@gmail.com');


-- ─── Storage: product-images bucket ───────────────────────────────────────────
-- Run AFTER making sure the bucket "product-images" exists in Supabase → Storage.

DROP POLICY IF EXISTS "public_read_product_images"   ON storage.objects;
DROP POLICY IF EXISTS "admin_insert_product_images"  ON storage.objects;
DROP POLICY IF EXISTS "admin_delete_product_images"  ON storage.objects;

CREATE POLICY "public_read_product_images"
  ON storage.objects FOR SELECT
  USING (bucket_id = 'product-images');

CREATE POLICY "admin_insert_product_images"
  ON storage.objects FOR INSERT
  WITH CHECK (
    bucket_id = 'product-images'
    AND auth.email() = 'shubhampaliwal5@gmail.com'
  );

CREATE POLICY "admin_delete_product_images"
  ON storage.objects FOR DELETE
  USING (
    bucket_id = 'product-images'
    AND auth.email() = 'shubhampaliwal5@gmail.com'
  );
