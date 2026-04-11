-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Products table
CREATE TABLE IF NOT EXISTS products (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name TEXT NOT NULL,
    name_normalized TEXT NOT NULL,
    brand TEXT,
    category TEXT,
    image_url TEXT,
    awareness_score INTEGER DEFAULT 50,
    summary TEXT,
    fssai_note TEXT,
    search_count INTEGER DEFAULT 1,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    last_verified TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_products_name ON products(name_normalized);
CREATE INDEX IF NOT EXISTS idx_products_category ON products(category);

-- Product ingredients table
CREATE TABLE IF NOT EXISTS product_ingredients (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    product_id UUID REFERENCES products(id) ON DELETE CASCADE,
    ingredient_name TEXT NOT NULL,
    aliases TEXT,
    classification TEXT NOT NULL CHECK (classification IN ('generally_recognised', 'worth_knowing', 'commonly_questioned')),
    one_line_note TEXT,
    regulatory_note TEXT
);

CREATE INDEX IF NOT EXISTS idx_pi_product ON product_ingredients(product_id);

-- Ingredient rules master table
CREATE TABLE IF NOT EXISTS ingredient_rules (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name TEXT NOT NULL UNIQUE,
    aliases TEXT[],
    classification TEXT NOT NULL 
        CHECK (classification IN ('generally_recognised', 'worth_knowing', 'commonly_questioned')),
    what_it_is TEXT,
    commonly_found_in TEXT,
    one_line_note TEXT,
    countries_restricted TEXT[],
    fssai_position TEXT,
    applies_to TEXT DEFAULT 'both' 
        CHECK (applies_to IN ('food', 'cosmetic', 'both')),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Recommendations table
CREATE TABLE IF NOT EXISTS recommendations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    trigger_category TEXT,
    recommended_name TEXT NOT NULL,
    recommended_brand TEXT,
    recommended_image TEXT,
    buy_link TEXT,
    is_sponsored BOOLEAN DEFAULT FALSE,
    category TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Search history table
CREATE TABLE IF NOT EXISTS search_history (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    query TEXT NOT NULL,
    product_id UUID REFERENCES products(id) ON DELETE SET NULL,
    ip_hash TEXT,
    searched_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_history_date ON search_history(searched_at DESC);
