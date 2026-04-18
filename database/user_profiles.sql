-- Run this in your Supabase SQL editor

CREATE TABLE IF NOT EXISTS public.user_profiles (
  id            UUID        PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
  phone         TEXT,
  -- Quiz answers (optional, for monetisation insights)
  age_group         TEXT,
  health_concern    TEXT,
  diet_type         TEXT,
  check_frequency   TEXT,
  product_category  TEXT,
  quiz_completed    BOOLEAN   DEFAULT FALSE,
  created_at    TIMESTAMPTZ DEFAULT NOW()
);

-- Row-Level Security: users can only read/write their own profile
ALTER TABLE public.user_profiles ENABLE ROW LEVEL SECURITY;

CREATE POLICY "select_own_profile" ON public.user_profiles
  FOR SELECT USING (auth.uid() = id);

CREATE POLICY "insert_own_profile" ON public.user_profiles
  FOR INSERT WITH CHECK (auth.uid() = id);

CREATE POLICY "update_own_profile" ON public.user_profiles
  FOR UPDATE USING (auth.uid() = id);
