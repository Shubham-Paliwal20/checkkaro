CREATE TABLE IF NOT EXISTS ingredient_reports (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  product_id TEXT NOT NULL,
  product_name TEXT NOT NULL,
  user_id UUID REFERENCES auth.users(id),
  user_email TEXT,
  reported_ingredients TEXT NOT NULL,
  reason TEXT,
  status TEXT DEFAULT 'pending' CHECK (status IN ('pending', 'approved', 'rejected')),
  created_at TIMESTAMPTZ DEFAULT NOW(),
  reviewed_at TIMESTAMPTZ
);
ALTER TABLE ingredient_reports ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Users can insert own reports" ON ingredient_reports FOR INSERT WITH CHECK (auth.uid() = user_id);
CREATE POLICY "Admins can read all reports" ON ingredient_reports FOR SELECT USING (true);
CREATE POLICY "Admins can update reports" ON ingredient_reports FOR UPDATE USING (true);
