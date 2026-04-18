-- Run this in your Supabase SQL editor

CREATE TABLE IF NOT EXISTS public.reviews (
  id            UUID        PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id       UUID        REFERENCES auth.users(id) ON DELETE SET NULL,
  reviewer_name TEXT        NOT NULL,
  review_text   TEXT        NOT NULL,
  rating        INTEGER     CHECK (rating >= 1 AND rating <= 5) DEFAULT 5,
  is_approved   BOOLEAN     DEFAULT TRUE,
  created_at    TIMESTAMPTZ DEFAULT NOW()
);

ALTER TABLE public.reviews ENABLE ROW LEVEL SECURITY;

-- Anyone can read approved reviews
CREATE POLICY "read_approved_reviews" ON public.reviews
  FOR SELECT USING (is_approved = TRUE);

-- Logged-in users can insert their own review
CREATE POLICY "insert_own_review" ON public.reviews
  FOR INSERT WITH CHECK (auth.uid() = user_id);
