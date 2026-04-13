-- Products table for storing real product data
CREATE TABLE IF NOT EXISTS products_catalog (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name TEXT NOT NULL,
    brand TEXT,
    category TEXT,
    barcode TEXT UNIQUE,
    image_url TEXT,
    ingredients_text TEXT, -- Raw ingredients from label
    ingredients_list TEXT[], -- Array of ingredient names
    awareness_score INTEGER,
    summary TEXT,
    fssai_note TEXT,
    verdict TEXT,
    recommendation TEXT,
    data_source TEXT, -- 'openfoodfacts', 'bigbasket', 'user_submitted', 'verified', 'manual'
    is_verified BOOLEAN DEFAULT FALSE,
    search_count INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Index for fast product name search
CREATE INDEX IF NOT EXISTS idx_products_catalog_name ON products_catalog USING gin(to_tsvector('english', name));
CREATE INDEX IF NOT EXISTS idx_products_catalog_brand ON products_catalog(brand);
CREATE INDEX IF NOT EXISTS idx_products_catalog_barcode ON products_catalog(barcode);
CREATE INDEX IF NOT EXISTS idx_products_catalog_search_count ON products_catalog(search_count DESC);

-- Product ingredients junction table (parsed and classified)
CREATE TABLE IF NOT EXISTS product_ingredients_catalog (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    product_id UUID REFERENCES products_catalog(id) ON DELETE CASCADE,
    ingredient_name TEXT NOT NULL,
    classification TEXT, -- generally_recognised, worth_knowing, commonly_questioned
    one_line_note TEXT,
    regulatory_note TEXT,
    position INTEGER, -- order in ingredient list (1 = first ingredient)
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_product_ingredients_catalog_product_id ON product_ingredients_catalog(product_id);
CREATE INDEX IF NOT EXISTS idx_product_ingredients_catalog_name ON product_ingredients_catalog(ingredient_name);

-- User contributions table (for crowdsourcing data)
CREATE TABLE IF NOT EXISTS user_contributions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    product_name TEXT NOT NULL,
    brand TEXT,
    barcode TEXT,
    ingredients_text TEXT NOT NULL,
    image_url TEXT,
    submitted_by TEXT, -- user email or anonymous
    status TEXT DEFAULT 'pending', -- pending, approved, rejected
    admin_notes TEXT,
    reviewed_by TEXT,
    reviewed_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_user_contributions_status ON user_contributions(status);
CREATE INDEX IF NOT EXISTS idx_user_contributions_created ON user_contributions(created_at DESC);

-- Comments
COMMENT ON TABLE products_catalog IS 'Verified product catalog with real ingredient data from multiple sources';
COMMENT ON TABLE product_ingredients_catalog IS 'Parsed and classified ingredients for each product';
COMMENT ON TABLE user_contributions IS 'User-submitted product data pending review';
