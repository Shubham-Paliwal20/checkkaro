import { useState, useEffect } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { supabase } from '../lib/supabaseClient'
import { useAuth } from '../context/AuthContext'
import SEO from '../components/SEO'

const CATEGORIES = ['All', 'Food', 'Cosmetics', 'Health', 'Lifestyle', 'Product Review']

const CAT_COLORS = {
  'Food':           { bg: '#fff7ed', text: '#ea580c', dot: '#f97316' },
  'Cosmetics':      { bg: '#fdf2f8', text: '#be185d', dot: '#ec4899' },
  'Health':         { bg: '#f0fdf4', text: '#15803d', dot: '#22c55e' },
  'Lifestyle':      { bg: '#eff6ff', text: '#1d4ed8', dot: '#3b82f6' },
  'Product Review': { bg: '#faf5ff', text: '#7e22ce', dot: '#a855f7' },
}

export const STATIC_BLOGS = [
  {
    id: 'static-1',
    slug: 'static-1',
    title: 'Why You Should Read Food Labels Before Buying Packaged Snacks in India',
    excerpt: 'Most Indians never read the ingredient list on packaged food. Here\'s what you\'re missing — and why it matters for your family\'s health.',
    content: `Most Indians pick up a packet of chips or biscuits without a second glance at the ingredient list. But what if that list told a very different story than the attractive packaging?

India's packaged food industry is booming. With over 40,000 food products on shelves, we're eating more processed food than ever before. And yet, most of us have no idea what's actually inside these products.

**What to look for on a food label**

The first thing to understand is that ingredients are listed in descending order of quantity. So if sugar is the first ingredient in your "health" cereal — it's mostly sugar.

Common red flags to watch out for:
- **Partially hydrogenated oils**: A source of trans fats, linked to heart disease
- **High Fructose Corn Syrup (HFCS)**: Added sugar that's metabolised differently by your body
- **Artificial colours like Tartrazine (E102)**: Linked to hyperactivity in children
- **Sodium nitrite**: Used in processed meats, a known carcinogen at high levels
- **MSG**: While generally safe for most, causes reactions in sensitive individuals

**The "natural flavours" trick**

Brands love to use the phrase "natural flavours" — but this can mean almost anything. Natural strawberry flavour, for example, can legally be derived from wood shavings treated with chemicals. It doesn't have to come from actual strawberries.

**What FSSAI requires**

The Food Safety and Standards Authority of India (FSSAI) mandates that all packaged foods display:
- Complete ingredient list
- Nutritional information per 100g
- Any allergens in bold
- Manufacturing and expiry date
- Vegetarian/non-vegetarian symbol

**Start small**

You don't need to become an expert overnight. Start by checking the first three ingredients on your next grocery run. If you can't pronounce them or don't know what they are — that's a sign to look them up on Parkho before buying.

Knowledge is your best defence against misleading marketing. The next time a brand claims "no added sugar" or "made with real fruits" — check the label. The truth is always there.`,
    category: 'Food',
    author_name: 'Parkho Editorial',
    cover_image: 'https://images.unsplash.com/photo-1606787366850-de6330128bfc?w=800&q=80',
    created_at: new Date(Date.now() - 2 * 24 * 60 * 60 * 1000).toISOString(),
    status: 'approved',
    isStatic: true,
  },
  {
    id: 'static-2',
    slug: 'static-2',
    title: 'Parabens in Indian Skincare: Should You Really Be Worried?',
    excerpt: 'Parabens are in almost every moisturiser, shampoo, and cream on the market. But are they actually dangerous? Here\'s what the science says.',
    content: `Walk into any pharmacy or beauty store in India and pick up a moisturiser. Flip it over. Chances are high you'll find methylparaben, propylparaben, or butylparaben somewhere in the ingredient list.

Parabens are preservatives. They've been used in cosmetics since the 1950s to prevent bacteria and mould from growing in your lotions and creams. Without them, your moisturiser could become a petri dish within weeks.

**Why people are worried**

The alarm bells started in 2004 when a UK study found traces of parabens in breast tumour tissue. Headlines screamed that parabens cause cancer. Social media ran with it. "Paraben-free" became the hottest marketing claim in beauty.

But here's what that study actually showed: parabens were present in the tissue. It did NOT show that parabens caused the cancer, or that they wouldn't have been present in healthy tissue too. Correlation is not causation.

**What regulators say**

The European Scientific Committee on Consumer Safety (SCCS) reviewed the evidence extensively. Their conclusion:
- Methylparaben and ethylparaben are safe at current use levels
- Propylparaben and butylparaben: safe below 0.19% concentration
- Isopropylparaben and isobutylparaben: insufficient safety data, best avoided

FSSAI in India follows similar guidelines. Most products use parabens at concentrations of 0.01–0.3%, well within safe limits.

**Who should be careful**

If you have sensitive skin or hormone-related conditions, you may want to limit paraben exposure as a precaution — not because the science is conclusive, but because the precautionary principle makes sense.

Pregnant women and parents of young children may also prefer to choose paraben-free options, especially for products applied to large areas of skin regularly.

**The bottom line**

Parabens at typical cosmetic concentrations are not proven to cause harm in healthy adults. The "paraben-free" marketing trend has outpaced the actual scientific concern. However, if you prefer to avoid them — plenty of alternatives like phenoxyethanol exist, each with their own profile worth checking.

Use Parkho to check any ingredient you're unsure about. Knowledge beats both blind trust and unnecessary panic.`,
    category: 'Cosmetics',
    author_name: 'Parkho Editorial',
    cover_image: 'https://images.unsplash.com/photo-1556228578-8c89e6adf883?w=800&q=80',
    created_at: new Date(Date.now() - 4 * 24 * 60 * 60 * 1000).toISOString(),
    status: 'approved',
    isStatic: true,
  },
  {
    id: 'static-3',
    slug: 'static-3',
    title: 'Hidden Sugar in "Healthy" Indian Foods — What Brands Don\'t Tell You',
    excerpt: 'Oats, granola, fruit juice, multigrain bread — they all sound healthy. But the sugar content might shock you.',
    content: `India has one of the highest rates of diabetes in the world — over 100 million diabetics and counting. Yet somehow, we're eating more "health foods" than ever. Something doesn't add up.

The problem isn't just mithai and soft drinks. The hidden sugar problem runs through foods we consider healthy.

**The usual suspects**

*Packaged fruit juices*: A 200ml tetra pack of "100% fruit juice" can contain 20–25 grams of sugar. That's more sugar than a can of cola per 200ml. The fibre that slows sugar absorption in whole fruit is gone. What remains is essentially sugar water with vitamins.

*Flavoured yoghurt*: Plain dahi is one of the healthiest foods you can eat. Flavoured yoghurt brands add 15–25g of sugar per 100g serving. Check the label — sugar is often the second ingredient.

*Multigrain bread*: The word "multigrain" just means multiple grains. It doesn't mean whole grain, low-GI, or low-sugar. Many multigrain breads in India contain added sugar and refined flour as the primary ingredient.

*Breakfast cereals*: Some popular cereals marketed to children contain over 30% sugar by weight. They're cereal-flavoured candy, essentially.

*Granola and muesli*: Brands like to show photos of nuts and oats. But check the label — honey, glucose syrup, and brown sugar can make these calorie and sugar bombs.

**How sugar hides in ingredient lists**

Manufacturers use many names for sugar to make it less obvious:
- Dextrose, fructose, sucrose, maltose
- Corn syrup, glucose syrup, high fructose corn syrup
- Fruit juice concentrate
- Cane juice, coconut sugar, jaggery
- Maltodextrin (acts like sugar in the body)

**What to do**

Look at the nutritional information, not just the ingredients. Check "Total Sugars" per 100g. As a rule of thumb:
- Under 5g per 100g = low sugar
- 5–15g per 100g = moderate
- Over 15g per 100g = high sugar

Real healthy eating in India doesn't need to be complicated. Dal, sabzi, roti, curd, fruits — traditional Indian food is naturally low in added sugar. The health food industry has simply repackaged junk food with better marketing.`,
    category: 'Food',
    author_name: 'Parkho Editorial',
    cover_image: 'https://images.unsplash.com/photo-1490645935967-10de6ba17061?w=800&q=80',
    created_at: new Date(Date.now() - 6 * 24 * 60 * 60 * 1000).toISOString(),
    status: 'approved',
    isStatic: true,
  },
  {
    id: 'static-4',
    slug: 'static-4',
    title: '5 Harmful Ingredients Hiding in Your Daily Face Cream',
    excerpt: 'Your moisturiser may be doing more harm than good. These five ingredients are worth avoiding — especially in products you use every day.',
    content: `We put moisturiser on our face every single day. Which makes the ingredients in it especially important — because daily exposure to even small amounts of harmful chemicals adds up over time.

Here are five ingredients to watch for in your face cream.

**1. Sodium Lauryl Sulphate (SLS)**

SLS is a detergent that creates foam and lather. It's cheap, effective at cleaning, and harsh. In face creams, it can strip your skin's natural moisture barrier, cause irritation, and worsen conditions like rosacea and eczema. It's more commonly found in face washes than creams, but check anyway.

**2. Synthetic Fragrances (Parfum)**

"Parfum" or "Fragrance" on an ingredient list is a legal black box. A single fragrance ingredient can contain up to 200 individual chemicals — and manufacturers don't have to disclose them. Synthetic fragrances are the number one cause of cosmetic allergic reactions.

If your face cream has a pleasant scent but "fragrance" is the source — consider switching to a fragrance-free option, especially if you have sensitive skin.

**3. Mineral Oil (Paraffinum Liquidum)**

Derived from petroleum, mineral oil is cheap and used as a moisturising agent in many budget face creams. The problem: it forms an occlusive layer on skin that traps moisture but also clogs pores. For oily or acne-prone skin, this can be problematic. For dry, non-acne-prone skin, it's generally harmless.

**4. Oxybenzone (in SPF moisturisers)**

If your daily moisturiser has SPF, check if oxybenzone is listed. This chemical UV filter has been detected in human blood, urine, and breast milk after topical application. The FDA has flagged it as needing more safety data. Mineral sunscreens with zinc oxide or titanium dioxide are safer alternatives.

**5. Formaldehyde-releasing preservatives**

DMDM Hydantoin, Imidazolidinyl Urea, Diazolidinyl Urea, and Quaternium-15 all release small amounts of formaldehyde over time. Formaldehyde is a known carcinogen and allergen. These preservatives are still legal and widely used in India. Check your face cream's ingredient list carefully.

**What to do**

You don't need to throw away everything you own. Start by checking the products you use on your face daily — the ones with the most contact time and largest application area. Use Parkho to check any ingredient you're unsure about.

Switching to cleaner formulations doesn't have to be expensive. Many affordable Indian brands now offer products without these ingredients.`,
    category: 'Cosmetics',
    author_name: 'Parkho Editorial',
    cover_image: 'https://images.unsplash.com/photo-1598440947619-2c35fc9aa908?w=800&q=80',
    created_at: new Date(Date.now() - 8 * 24 * 60 * 60 * 1000).toISOString(),
    status: 'approved',
    isStatic: true,
  },
  {
    id: 'static-5',
    slug: 'static-5',
    title: 'E-Numbers in Indian Food: Which Are Safe and Which to Avoid',
    excerpt: 'E-numbers are everywhere in packaged food. But not all of them are harmful. Here\'s a simple guide to understanding what they mean.',
    content: `You've seen them on every packet of processed food: E102, E211, E621. These codes look technical and mysterious. But they're just a standardised numbering system for food additives approved for use in food production.

Not all E-numbers are harmful. Many are derived from natural sources. Here's how to make sense of them.

**How E-numbers are categorised**

- E100–E199: Colours
- E200–E299: Preservatives
- E300–E399: Antioxidants
- E400–E499: Thickeners, stabilisers, emulsifiers
- E500–E599: Acidity regulators
- E600–E699: Flavour enhancers
- E900+: Sweeteners, glazing agents, others

**Commonly used and generally safe**

*E300 (Vitamin C / Ascorbic acid)*: An antioxidant derived from vitamin C. Completely safe. Used to prevent oxidation and preserve colour.

*E322 (Lecithin)*: Usually derived from soy or sunflower. An emulsifier found in chocolate. Generally safe and occurs naturally in eggs.

*E330 (Citric acid)*: Found naturally in citrus fruits. Used as a preservative and flavour enhancer. Very safe.

*E440 (Pectin)*: Derived from fruit peels. Used as a gelling agent in jams. Completely natural and safe.

**Ones to be cautious about**

*E102 (Tartrazine)*: A synthetic yellow dye. Linked to hyperactivity in children in some studies. Banned in Norway and Austria. Used widely in Indian snacks, drinks, and confectionery.

*E110 (Sunset Yellow)*: Another synthetic dye. Associated with allergic reactions, particularly in people sensitive to aspirin.

*E211 (Sodium Benzoate)*: A preservative. When combined with Vitamin C (E300) in acidic drinks, it can form benzene — a known carcinogen. Commonly found in soft drinks and pickles.

*E621 (MSG / Monosodium Glutamate)*: A flavour enhancer. Generally considered safe by regulatory bodies, but some people report sensitivity symptoms. Used heavily in Chinese food and instant noodles.

*E951 (Aspartame)*: An artificial sweetener. Safe for most people but should be avoided by those with phenylketonuria (PKU). There's ongoing debate about long-term effects at high doses.

**The simple rule**

Numbers in the 100s (colours) and 200s (preservatives) deserve the most scrutiny. Numbers in the 300s and 400s are usually harmless or naturally derived.

When in doubt, use Parkho to check any E-number before buying.`,
    category: 'Food',
    author_name: 'Parkho Editorial',
    cover_image: 'https://images.unsplash.com/photo-1567306226416-28f0efdc88ce?w=800&q=80',
    created_at: new Date(Date.now() - 10 * 24 * 60 * 60 * 1000).toISOString(),
    status: 'approved',
    isStatic: true,
  },
  {
    id: 'static-6',
    slug: 'static-6',
    title: 'How to Read a Cosmetic Ingredient List Like an Expert',
    excerpt: 'INCI names look intimidating. But once you know the basics, you\'ll never look at a skincare product the same way again.',
    content: `Aqua. Glycerin. Niacinamide. Cetearyl Alcohol. If you've tried reading the back of a moisturiser and given up — you're not alone. Cosmetic ingredient lists (written in INCI format) look like a chemistry textbook.

But here's the secret: you only need to understand a few basics to become a smarter cosmetics consumer.

**What is INCI?**

INCI stands for International Nomenclature of Cosmetic Ingredients. It's a standardised system used globally to name cosmetic ingredients. The same ingredient will have the same INCI name on a product sold in India, Europe, or the US — making it easier to research and compare.

**Rule 1: Order matters**

Ingredients are listed in descending order by concentration. The first ingredient is present in the highest amount. Usually the first 1–5 ingredients make up 80–90% of the product.

If water (Aqua) is first — it's mostly water. If a "vitamin C serum" lists sodium ascorbyl phosphate 10th — there's very little actual vitamin C in it.

**Rule 2: The 1% threshold**

After a certain point in the list (usually around the 10th–15th ingredient), concentrations drop below 1%. Ingredients after this point can be listed in any order. This is where you'll often find preservatives, fragrances, and actives present in tiny amounts.

**Key ingredient categories to know**

*Humectants* (attract moisture): Glycerin, Hyaluronic Acid, Sodium PCA
*Emollients* (soften skin): Squalane, Jojoba Oil, Cetearyl Alcohol
*Occlusives* (seal in moisture): Petrolatum, Dimethicone, Beeswax
*Actives* (target skin concerns): Niacinamide, Retinol, Salicylic Acid, AHA/BHA
*Preservatives*: Phenoxyethanol, Parabens, DMDM Hydantoin
*Emulsifiers* (keep oil and water mixed): Polysorbate 20, Ceteareth-20

**Words that are just water**

"Aqua," "Eau," "Water" — all the same thing. Some fancy brands write it as "Alpine Spring Water" or "Thermal Water" — it's still water. Don't pay a premium for it.

**Red flags in ingredient lists**

- Alcohol Denat high up the list (drying, irritating)
- "Fragrance" or "Parfum" with no further detail
- Many silicones in anti-ageing products (they fill wrinkles temporarily but do nothing long-term)
- "Collagen" in a topical cream (too large to penetrate skin — it just sits on top)

**Your cheat sheet**

Next time you pick up a skincare product:
1. Check the first 5 ingredients — what's the base?
2. Look for your target active — where does it appear in the list?
3. Check for fragrance and known irritants
4. Use Parkho to look up anything unfamiliar

It takes 2 minutes and could save you from spending ₹2,000 on a product that doesn't do what it claims.`,
    category: 'Cosmetics',
    author_name: 'Parkho Editorial',
    cover_image: 'https://images.unsplash.com/photo-1596755389378-c31d21fd1273?w=800&q=80',
    created_at: new Date(Date.now() - 12 * 24 * 60 * 60 * 1000).toISOString(),
    status: 'approved',
    isStatic: true,
  },
  {
    id: 'static-7',
    slug: 'static-7',
    title: 'Processed Meats and Cancer: What the WHO Classification Actually Means for Your Diet',
    excerpt: 'In 2015, the WHO classified processed meats as a Group 1 carcinogen — the same category as cigarettes. But does that mean a slice of salami is as dangerous as smoking? Here\'s what the science actually says.',
    content: `In October 2015, the International Agency for Research on Cancer (IARC) — the cancer research arm of the World Health Organisation — released a report that made headlines worldwide. Processed meats were classified as Group 1 carcinogens. Red meat was placed in Group 2A (probably carcinogenic).

The internet had a panic. But most of the coverage missed a critical distinction that changes everything.

**What "Group 1 carcinogen" actually means**

Group 1 simply means there is *sufficient evidence* that the substance causes cancer in humans. It says nothing about how much cancer risk is involved. This is where the cigarette comparison breaks down completely.

Tobacco smoking causes approximately 19% of all cancers globally. Processed meat consumption at current average intake levels is associated with approximately a 17–18% *relative* increase in colorectal cancer risk — which translates to an absolute increase of about 1% in lifetime colorectal cancer risk (from roughly 5% to 6% for someone eating 50g of processed meat daily).

To put it simply: the evidence that processed meat causes cancer is as strong as the evidence that tobacco does. The *amount* of cancer caused is vastly different.

**What counts as processed meat?**

The WHO defines processed meat as meat that has been transformed through salting, curing, fermentation, smoking or other processes to enhance flavour or improve preservation. This includes:
- Sausages, frankfurters, hot dogs
- Ham, bacon, salami, pepperoni
- Corned beef and canned meat
- Biltong and beef jerky
- Meat-based ready meals

In the Indian context: packaged salami, chicken sausages, canned meats, and instant products with meat flavouring.

**Why does processed meat raise cancer risk?**

Three main mechanisms researchers have identified:

*N-nitrosamines*: Sodium nitrite and sodium nitrate — used to cure meats — react with amines from proteins during digestion and during high-temperature cooking to form N-nitrosamines. Several N-nitrosamines are classified IARC Group 1 carcinogens. This is the most established mechanism.

*Haem iron*: Red meat is rich in haem iron, which can promote the formation of N-nitroso compounds in the colon.

*Heterocyclic amines (HCAs) and polycyclic aromatic hydrocarbons (PAHs)*: Cooking meat at high temperatures (grilling, smoking) creates HCAs and PAHs — both genotoxic compounds.

**The dose matters enormously**

The IARC analysis found that eating 50g of processed meat per day — roughly two slices of bacon or one sausage — was associated with an 18% increase in relative risk of colorectal cancer.

People who eat processed meat occasionally, as a small component of an otherwise vegetable and fibre-rich diet, are at significantly lower risk than daily consumers. The harm is real, but it is dose-dependent.

**Practical guidance for Indian diets**

India's traditional diet is already largely protective. High fibre intake from dal, vegetables, and whole grains reduces colorectal cancer risk. The concern applies primarily to urban Indians increasingly eating packaged processed meats regularly, and children eating packaged meat snacks daily.

You do not need to eliminate processed meat entirely. But if you eat it daily — consider reducing to occasional consumption. When you do eat it, prefer freshly prepared forms over heavily cured products, and balance your diet with high-fibre foods.

Use Parkho to check the ingredient lists of packaged meat products — particularly to identify sodium nitrite (E250) and sodium nitrate (E251) content.`,
    category: 'Food',
    author_name: 'Parkho Editorial',
    cover_image: 'https://images.unsplash.com/photo-1504674900247-0877df9cc836?w=800&q=80',
    created_at: new Date(Date.now() - 14 * 24 * 60 * 60 * 1000).toISOString(),
    status: 'approved',
    isStatic: true,
  },
  {
    id: 'static-8',
    slug: 'static-8',
    title: 'Aspartame, Sucralose or Stevia? What 2023 Research Changed About Artificial Sweeteners',
    excerpt: 'The WHO issued a major advisory on non-sugar sweeteners in 2023. Three landmark studies raised new concerns about sweeteners we thought were safe. Here is what the evidence actually says.',
    content: `For decades, artificial sweeteners seemed like the perfect solution: all the sweetness of sugar, none of the calories, no blood glucose spike. Diabetics used them. Dieters swore by them. Health authorities called them safe.

Then 2023 arrived with research findings that complicated the picture considerably.

**The WHO advisory of 2023**

In May 2023, the World Health Organisation released a guideline recommending against the use of non-sugar sweeteners (NSS) for weight control. The WHO reviewed 283 studies and concluded that using sweeteners does not help with long-term weight management — and may be associated with increased risk of Type 2 diabetes and cardiovascular disease with long-term use.

**What happened with aspartame**

In July 2023, IARC classified aspartame as "possibly carcinogenic to humans" (Group 2B) — based on limited evidence of an association with hepatocellular carcinoma (liver cancer) in human observational studies.

Simultaneously, the WHO's JECFA committee maintained the acceptable daily intake (ADI) of 40 mg/kg body weight as safe — meaning a 70 kg person would need to consume 9–14 cans of diet soda daily to approach the limit.

The apparent contradiction: IARC classified it as possibly carcinogenic. JECFA said current intake is safe. Both are simultaneously true because IARC evaluates whether a substance can cause cancer at any dose, while JECFA evaluates harm at typical intake levels. For most people consuming aspartame in normal amounts, the risk is extremely low.

**The sucralose finding that surprised researchers**

Sucralose has long been considered the safest artificial sweetener because it largely passes through the body unchanged.

However, a 2023 paper in the Journal of Toxicology and Environmental Health found that sucralose-6-acetate — a metabolite in commercial sucralose — is genotoxic in vitro, causing DNA strand breaks in human cells. Separately, a Nature Medicine (2023) study found sucralose increased markers of immune activation in healthy volunteers.

EFSA and FDA have not changed safety classifications for sucralose in response, citing limited evidence. But the findings have prompted calls for further investigation.

**Stevia: the cleanest profile**

Stevia (steviol glycosides, E960) continues to have the most favourable safety profile. FDA GRAS; EFSA ADI of 4 mg/kg/day; no gut microbiome disruption in short-term human studies; some clinical data suggesting modest blood pressure-lowering and insulin-sensitising effects at higher doses.

Important distinction: the whole stevia leaf and crude stevia extracts are NOT approved for food use in the USA — only purified steviol glycosides are permitted. People with ragweed, chrysanthemum, or daisy (Asteraceae) allergy may rarely react to stevia.

**Erythritol: the 2023 cardiovascular signal**

Erythritol — widely used in keto and sugar-free products — received unexpected attention when a March 2023 Nature Medicine study (Hazen SL, Cleveland Clinic) found: (1) high serum erythritol levels were associated with increased 3-year major adverse cardiovascular events in a prospective cohort, and (2) consuming erythritol significantly increased platelet aggregation in 8 healthy volunteers.

The important caveat: serum erythritol includes erythritol produced endogenously by the body from glucose — so higher levels may be a marker of metabolic dysfunction rather than a direct effect of dietary erythritol. No regulatory body has changed erythritol's safety classification, and it remains the best-tolerated sugar alcohol with very minimal GI effects.

**What should you use?**

Based on current evidence:
- Stevia is the best-evidenced choice for most people
- Erythritol at moderate amounts is likely fine; large daily amounts warrant caution given the 2023 platelet data
- Aspartame at moderate intake (1–2 diet drinks/day) is probably safe but worth limiting for heavy users
- For diabetics: stevia and erythritol are preferable as they have the least impact on blood glucose
- For children: the WHO recommends children should not be habituated to excessive sweetness from any source

The bigger principle remains: no sweetener is superior to gradually reducing overall sweetness preference. But if you are going to use them, stevia currently has the cleanest evidence profile.`,
    category: 'Food',
    author_name: 'Parkho Editorial',
    cover_image: 'https://images.unsplash.com/photo-1548636581-eb82ef43c3ec?w=800&q=80',
    created_at: new Date(Date.now() - 16 * 24 * 60 * 60 * 1000).toISOString(),
    status: 'approved',
    isStatic: true,
  },
  {
    id: 'static-9',
    slug: 'static-9',
    title: 'The Ultra-Processed Food Trap: Why the NOVA Classification Is Changing Nutrition Science',
    excerpt: 'Not all processed food is harmful. But "ultra-processed" food — engineered in factories from substances extracted from food — is a different story. Here\'s the science behind NOVA and why it matters for India.',
    content: `"Processed food is bad." You've heard it. But it is an oversimplification that creates more confusion than clarity. Yoghurt is processed. Cheese is processed. Frozen vegetables are processed. So is bread.

The problem is that we have been lumping all processed food together. A food classification system called NOVA has been changing how nutrition scientists think about this — with significant implications for Indian diets.

**What is NOVA?**

Developed by Carlos Monteiro and colleagues at the University of Sao Paulo, NOVA classifies food into four groups based on the extent and purpose of processing — not nutrient content.

Group 1: Unprocessed or minimally processed foods — Fresh fruit, vegetables, plain meat, eggs, milk, plain pulses, nuts, seeds. Processing is minimal — washing, cutting, freezing, pasteurising.

Group 2: Processed culinary ingredients — Oils, butter, ghee, salt, sugar, flour, vinegar. Derived from Group 1 foods and used in cooking. Not meant to be eaten alone.

Group 3: Processed foods — Foods made by combining Group 1 and Group 2 items — tinned tomatoes, cheese, cured meats, pickles, freshly baked bread. Processing serves to preserve food or enhance taste.

Group 4: Ultra-processed foods (UPF) — Industrial formulations made from extracted or synthesised substances: hydrolysed protein, modified starch, high-fructose corn syrup, artificial flavours, synthetic colours, emulsifiers, humectants, thickeners. They contain ingredients you would never find in a home kitchen and are designed for hyperpalatability — engineered to make you eat more.

Common UPF examples in India: instant noodles, packaged biscuits and chips, carbonated beverages, flavoured milk drinks, packaged breakfast cereals, flavoured yoghurt with stabilisers, processed cheese slices, instant soups.

**The clinical evidence**

The landmark study was conducted by Kevin Hall and colleagues at the US National Institutes of Health, published in Cell Metabolism in 2019. It was the first randomised controlled trial directly comparing ultra-processed versus unprocessed diets.

20 adults were admitted to a clinical facility and randomly assigned to either an ultra-processed or an unprocessed diet for two weeks, then crossed over. Both diets were matched for total calories, sugar, fat, and fibre offered. Critically, participants could eat as much or as little as they wanted.

The results:
- On the ultra-processed diet, participants consumed an average of 508 additional calories per day compared to the unprocessed diet
- They ate faster on the ultra-processed diet
- They gained approximately 0.9 kg on the ultra-processed diet and lost 0.9 kg on the unprocessed diet

This was the first controlled evidence that UPF promote overconsumption — not just because they are calorie-dense, but because they disrupt satiety signals.

Subsequent large cohort studies (EPIC, NutriNet-Sante, UK Biobank involving hundreds of thousands of participants) consistently found associations between high UPF intake and higher rates of obesity, Type 2 diabetes, cardiovascular disease, depression, colorectal cancer, and faster cognitive decline.

**The emulsifier link**

One specific mechanism that has received significant scientific attention: several emulsifiers used in ultra-processed foods — carboxymethyl cellulose (E466), polysorbate 80, carrageenan — disrupted the intestinal mucosal barrier and altered gut microbiome composition in animal models. A 2022 human cohort study found higher E466 intake was associated with increased Crohn's disease risk.

Researchers are investigating whether chronic low-level exposure to multiple emulsifiers across dozens of UPF products daily is cumulatively damaging gut barrier function in humans.

**What this means for India**

India is undergoing one of the fastest nutritional transitions in the world. Urban Indians — particularly young adults and children — are rapidly shifting from traditional Group 1/2/3 diets (dal, sabzi, roti, rice, curd) to ultra-processed food as primary sources of calories.

The irony is that Indian traditional food already meets many criteria for what nutritionists now recommend: minimally processed staples, high in fibre, naturally fermented products (idli, dosa, kanji, achaar), moderate fat, low added sugar.

NOVA gives us a more useful question than "is this food healthy?" Ask instead: "Is this food recognisable as something that came from nature, or is it an industrial product engineered from food substances?"

You do not need to eliminate all NOVA 4 foods. But if ultra-processed food constitutes more than 20–25% of your daily calories — as it does for many urban Indians now — the evidence suggests your health would benefit from shifting that proportion toward NOVA 1 and 3 foods.`,
    category: 'Food',
    author_name: 'Parkho Editorial',
    cover_image: 'https://images.unsplash.com/photo-1565299624946-b28f40a0ae38?w=800&q=80',
    created_at: new Date(Date.now() - 18 * 24 * 60 * 60 * 1000).toISOString(),
    status: 'approved',
    isStatic: true,
  },
  {
    id: 'static-10',
    slug: 'static-10',
    title: 'Retinol: The Science Behind the Most Clinically Proven Anti-Ageing Skincare Ingredient',
    excerpt: 'Retinol has more peer-reviewed evidence behind it than almost any other skincare ingredient. Here is how it works at the cellular level, how to use it correctly, and who must avoid it entirely.',
    content: `If you had to pick one skincare ingredient with the strongest clinical evidence for anti-ageing, it would not be a serum full of exotic plant extracts. It would be retinol — a derivative of Vitamin A that has been studied continuously since the 1970s.

**What retinol actually does**

Retinol belongs to a class of compounds called retinoids. When applied to skin, retinol undergoes a two-step conversion:

Retinol → Retinaldehyde → Retinoic acid (the biologically active form)

Retinoic acid binds to nuclear receptors in skin cells (RAR and RXR receptors), triggering changes in gene expression that produce four measurable effects:

Increased cell turnover: Retinoids speed up the natural cycle of skin cell renewal — new cells reach the surface faster, pushing out damaged, pigmented, and thickened cells. This addresses hyperpigmentation, uneven texture, and dullness.

Stimulation of collagen synthesis: Retinoids directly stimulate fibroblasts (the collagen-producing cells) to increase collagen I and III production. They also inhibit MMP-1 — an enzyme that degrades existing collagen. Net result: thicker, firmer skin.

Normalisation of follicular keratinisation: Retinoids regulate the way cells in pores shed, preventing plugging that causes blackheads and whiteheads. This is why tretinoin is an FDA-approved first-line treatment for acne.

Inhibition of melanin synthesis: By dispersing melanin granules and inhibiting tyrosinase, retinoids reduce hyperpigmentation — post-inflammatory marks, melasma, and age spots.

**The clinical evidence**

The evidence for retinoids is not based on one or two industry-funded studies. It comes from decades of independent research.

A 1993 trial by Griffiths et al. in the New England Journal of Medicine demonstrated that 0.1% tretinoin significantly reduced fine wrinkles, mottled pigmentation, and skin roughness versus placebo over 48 weeks — with histological evidence of new collagen formation.

A 2007 study by Varani et al. in Archives of Dermatology showed that even 0.4% retinol — the over-the-counter concentration — significantly increased collagen production and improved skin thickness.

**The retinoid hierarchy**

From weakest to strongest in terms of conversion to active retinoic acid:

Retinyl palmitate → Retinol → Retinaldehyde (retinal) → Tretinoin (retinoic acid)

Tretinoin is the prescription form — already the final active compound. Works faster (3–6 months for visible results), causes more initial irritation, requires a dermatologist's prescription.

Retinol is the most common OTC option. At 0.1–0.5%, it produces measurable clinical results over 6–12 months of consistent use.

Retinaldehyde (retinal) is 11 times more potent than retinol and requires only one conversion step. An underrated option available in several Indian brands.

Bakuchiol, from babchi seeds, is a plant-based alternative that activates some of the same receptor pathways with significantly less irritation. A good option for beginners or sensitive skin.

**The retinoid reaction: why people give up too soon**

The most common reason people abandon retinol: they experience redness, flaking, dryness, and increased sensitivity in the first 4–8 weeks and assume the product is damaging their skin.

The "retinoid reaction" is a normal consequence of accelerated cell turnover. It is not damage. Most people's skin fully acclimatises within 8–12 weeks.

How to minimise it: start at the lowest concentration, apply only at night, begin with once or twice per week, use a gentle non-foaming cleanser and a good moisturiser, and always use SPF daily.

**Who must avoid retinol**

This is critical. All retinoids are contraindicated in pregnancy. Oral isotretinoin causes severe foetal malformations and is absolutely forbidden in pregnancy.

Topical retinol has far lower systemic absorption. However, dermatological consensus and all major guidelines recommend that pregnant women and women trying to conceive should avoid all topical retinoids as a precaution. Breastfeeding women should also avoid retinoids until weaning.

**Starting retinol: a practical protocol**

Week 1–4: 0.025% or 0.05%, once per week. Week 5–8: Increase to twice per week if no significant reaction. Week 9–12: Three times per week. After 3 months: Every other night. After 6 months: Nightly use if tolerated.

Always use SPF during the day. Results from retinol are real, but they require patience. Most clinical studies show measurable improvements at the 6-month mark.`,
    category: 'Cosmetics',
    author_name: 'Parkho Editorial',
    cover_image: 'https://images.unsplash.com/photo-1620916566398-39f1143ab7be?w=800&q=80',
    created_at: new Date(Date.now() - 20 * 24 * 60 * 60 * 1000).toISOString(),
    status: 'approved',
    isStatic: true,
  },
  {
    id: 'static-11',
    slug: 'static-11',
    title: 'Chemical vs Mineral Sunscreen: What the Science Actually Says in 2024',
    excerpt: 'The FDA flagged four major chemical UV filters as lacking sufficient safety data. Hawaii banned two of them. Here\'s what the evidence says — and which sunscreen is actually better for your skin.',
    content: `Sunscreen is the single most evidence-backed anti-ageing skincare product that exists. The evidence that UV radiation causes photoageing, hyperpigmentation, and skin cancer is overwhelming and unambiguous.

But the debate about which type of sunscreen to use — chemical versus mineral — has intensified over the past five years, driven by real regulatory action and legitimate scientific concerns.

**The fundamental difference**

Chemical (organic) UV filters — oxybenzone, octinoxate, avobenzone, octocrylene, homosalate — work by absorbing UV photons and converting them to heat. They are invisible on skin and easy to formulate into lightweight textures.

Mineral (inorganic) UV filters — zinc oxide and titanium dioxide — work by scattering and reflecting UV photons. They are photostable, provide broad-spectrum UVA and UVB coverage, and leave a white cast (though nano-formulations reduce this significantly).

**What the FDA found**

In February 2019, the FDA released a proposed rule updating sunscreen regulations. The finding: only zinc oxide and titanium dioxide had sufficient safety data to be classified as "generally recognised as safe and effective" (GRASE). Four chemical filters — oxybenzone, octinoxate, homosalate, and octisalate — were classified as "not GRASE" due to insufficient systemic absorption safety data.

This does NOT mean these ingredients are proven harmful. It means the safety studies required for a drug ingredient have not been completed.

A subsequent 2020 FDA clinical study found that blood levels of oxybenzone, octinoxate, octocrylene, and homosalate exceeded the FDA's safety threshold after a single day of whole-body application.

**Specific concerns with key chemical filters**

Oxybenzone (benzophenone-3): Significantly absorbed through skin — detected in blood, urine, and breast milk. Animal and in vitro studies show oestrogenic and anti-androgenic activity. Toxic to coral reefs — Hawaii and Palau have banned it. FDA "not GRASE."

Octinoxate: Significant systemic absorption; weak oestrogen and anti-androgen activity in animal studies; banned alongside oxybenzone in Hawaii; FDA "not GRASE."

Octocrylene: Increasingly recognised as a significant contact allergen; degrades in sunscreen products to benzophenone; highly cross-reactive with ketoprofen (NSAID), causing severe photoallergic reactions.

Avobenzone: Provides the broadest UVA coverage of the chemical filters but is photolabile — degrades within 30 minutes in sunlight without photostabilisers.

**The case for mineral sunscreens**

Zinc oxide and titanium dioxide are FDA GRASE — the safest classification. They do not penetrate intact skin, are not systemically absorbed, are photostable, provide broad-spectrum UVA and UVB protection, have no endocrine disruption concerns, and are not toxic to coral reefs.

Main disadvantage: white cast — a real cosmetic issue for deeper Indian skin tones.

**Nano-particles: an important nuance**

Many modern mineral sunscreens use nano-sized particles to reduce white cast. Multiple independent studies by the TGA (Australia), SCCS (EU), and FDA found that nano-ZnO and nano-TiO2 particles do NOT penetrate intact healthy skin beyond the stratum corneum. The nano-particle safety concern on intact skin is not supported by clinical evidence.

However, spray sunscreens with nano-mineral particles raise inhalation concerns. Prefer lotion or cream mineral sunscreens over sprays.

**What this means for Indian skin**

India's climate — intense UV year-round, high humidity — makes daily SPF use non-negotiable.

For everyday facial use: A zinc oxide-based mineral sunscreen provides the most complete safety profile. SPF 30–50 is sufficient for daily indoor or commuting use.

For full-body outdoor application: A chemical sunscreen with avobenzone and photostabiliser (without oxybenzone or octinoxate) is a reasonable practical compromise.

For children: Mineral sunscreens are strongly preferred due to higher surface area-to-body-weight ratio.

The non-negotiable rule: wear sunscreen every day, reapply every 2 hours when outdoors, and use enough. An imperfectly chosen sunscreen used consistently is far better than a theoretically perfect sunscreen sitting in your drawer.`,
    category: 'Cosmetics',
    author_name: 'Parkho Editorial',
    cover_image: 'https://images.unsplash.com/photo-1526947425960-945c6e72858f?w=800&q=80',
    created_at: new Date(Date.now() - 22 * 24 * 60 * 60 * 1000).toISOString(),
    status: 'approved',
    isStatic: true,
  },
  {
    id: 'static-12',
    slug: 'static-12',
    title: 'Your Skin Barrier: The Science Behind Why It Matters More Than Any Serum You Use',
    excerpt: 'Every dermatologist gives the same advice first: fix your skin barrier before adding actives. Here\'s the biology behind why — and what common skincare habits are silently damaging it every day.',
    content: `Walk into any dermatologist's office with a skin complaint — acne, hyperpigmentation, redness, sensitivity, premature ageing — and the first question is almost never "which serum should I try?" It is almost always about your cleansing routine or how many active ingredients you are using at once.

No active ingredient, however well-formulated or clinically backed, works optimally on a compromised skin barrier. And a surprising number of skincare routines are actively damaging the very barrier they depend on.

**What the skin barrier actually is**

The skin barrier refers primarily to the outermost layer of the epidermis: the stratum corneum. It is described using a "brick and mortar" analogy — dead skin cells (corneocytes, the bricks) held together by a lipid matrix (the mortar) composed of ceramides (approximately 50%), cholesterol (25%), and free fatty acids (15%).

This structure prevents transepidermal water loss (TEWL), acts as a physical barrier to pathogens and allergens, regulates the skin's microbiome, and maintains an acidic pH of approximately 4.5–5.5 (the "acid mantle").

**What happens when the barrier is damaged**

A damaged skin barrier becomes more permeable, with cascading consequences:

More water loss: TEWL increases, causing dryness, tightness, and flaking.

More irritant penetration: Normally excluded allergens breach the barrier more easily, causing sensitisation and allergic reactions.

Microbiome disruption: The skin's normal microbiome depends on acidic pH. A compromised barrier shifts pH toward alkaline, allowing Staphylococcus aureus (associated with eczema) to outcompete beneficial bacteria.

Inflammation spiral: A broken barrier activates keratinocyte inflammatory pathways, which further damages barrier function — a self-perpetuating cycle seen in eczema, rosacea, and acne.

In eczema (atopic dermatitis), the genetic root cause is often mutations in the gene encoding filaggrin — a protein critical for corneocyte structure. People with this mutation are born with structurally weaker barriers, explaining why eczema runs in families.

**What is silently damaging your skin barrier**

Over-cleansing: Soaps and many foaming cleansers are alkaline (pH 9–11) — far above the skin's natural pH of 4.5–5.5. A single wash with an alkaline cleanser disrupts the acid mantle for 1.5–3 hours. Sodium lauryl sulphate (SLS) — the most common surfactant in face washes — disrupts the lipid bilayer directly, denatures stratum corneum proteins, and measurably increases TEWL even after rinsing.

Signs of over-cleansing: skin feels "squeaky clean" after washing (that feeling IS barrier disruption), persistent tightness, increased oiliness as the skin overcompensates, new sensitivities to products that previously caused no irritation.

Over-exfoliation: AHAs, BHAs, physical scrubs, and retinoids all accelerate cell turnover. Used too aggressively or in combination without adequate recovery time, they thin the stratum corneum faster than it can regenerate.

The "skin cycling" protocol popularised by dermatologist Dr. Whitney Bowe — retinol night, recovery night, exfoliant night, recovery night — was designed specifically to address this.

Alcohol-heavy toners: SD alcohol and alcohol denat disrupt ceramide synthesis and increase TEWL with repeated use.

Hard water: Delhi, Mumbai, and much of urban India have hard tap water. Hard water forms insoluble calcium-soap deposits on skin, disrupts pH, and depletes natural moisturising factors.

**The ceramide research**

Ceramides are the most critical components of the skin barrier. In eczema, ceramide levels are measurably reduced even in clinically unaffected skin.

A 2020 systematic review found ceramide-containing moisturisers significantly reduced TEWL and improved skin hydration in eczema patients versus placebo. Ceramide-rich creams are recommended as first-line therapy by the National Eczema Association.

Products containing ceramide NP, ceramide AP, ceramide EOP, cholesterol, and fatty acids in balanced ratios — mimicking the natural stratum corneum lipid profile — are the most evidence-based moisturisers available.

**Niacinamide: a barrier-supporting active**

Niacinamide (vitamin B3) is one of the few OTC actives with direct evidence for barrier improvement. At 2–5%, it increases ceramide synthesis in keratinocytes, reduces TEWL, improves stratum corneum thickness, and has anti-inflammatory properties. It is also one of the most universally tolerated actives — making it ideal for barrier-damaged skin.

**A barrier-first approach**

Before adding any active ingredient — retinol, vitamin C, AHA, BHA — ask whether your barrier is intact. Signs of a compromised barrier: new sensitivities to products that previously did not bother you, persistent redness, skin that feels tight after cleansing, dryness that does not resolve with regular moisturising.

If any of these apply, the answer is not more actives. The answer is: gentle low-pH cleanser, ceramide-based moisturiser, SPF, and nothing else for 4–6 weeks. Let your barrier repair. Then, one active at a time, reintroduce cautiously.

The most expensive skincare routine cannot work effectively on a broken barrier. The simplest routine built on barrier protection often outperforms it.`,
    category: 'Cosmetics',
    author_name: 'Parkho Editorial',
    cover_image: 'https://images.unsplash.com/photo-1631729371254-42c2892f0e6e?w=800&q=80',
    created_at: new Date(Date.now() - 24 * 24 * 60 * 60 * 1000).toISOString(),
    status: 'approved',
    isStatic: true,
  },
]

function timeAgo(dateStr) {
  const diff = Date.now() - new Date(dateStr).getTime()
  const days = Math.floor(diff / (1000 * 60 * 60 * 24))
  if (days === 0) return 'Today'
  if (days === 1) return 'Yesterday'
  if (days < 30) return `${days} days ago`
  return new Date(dateStr).toLocaleDateString('en-IN', { day: 'numeric', month: 'short', year: 'numeric' })
}

function CatBadge({ cat }) {
  const c = CAT_COLORS[cat] || { bg: '#f3f4f6', text: '#374151', dot: '#9ca3af' }
  return (
    <span style={{ background: c.bg, color: c.text }} className="text-xs font-bold px-3 py-1 rounded-full">
      {cat}
    </span>
  )
}

export default function Blog() {
  const [dbBlogs, setDbBlogs]   = useState([])
  const [category, setCategory] = useState('All')
  const { user, openAuthModal } = useAuth()
  const navigate = useNavigate()

  useEffect(() => {
    // Load DB blogs in background — static blogs show immediately
    supabase.from('blogs').select('id,title,slug,excerpt,category,author_name,cover_image,created_at')
      .eq('status', 'approved').order('created_at', { ascending: false })
      .then(({ data }) => { if (data && data.length > 0) setDbBlogs(data) })
      .catch(() => {})
  }, [])

  const allBlogs = [...dbBlogs, ...STATIC_BLOGS]
  const filtered = category === 'All' ? allBlogs : allBlogs.filter(b => b.category === category)
  const featured = filtered[0]
  const sideBlogs = filtered.slice(1, 4)
  const gridBlogs = filtered.slice(4)

  const blogListSchema = {
    '@context': 'https://schema.org',
    '@type': 'CollectionPage',
    name: 'Parkho Blog — Food, Cosmetics & Healthy Living',
    description: 'Articles about food ingredients, cosmetic safety, E-numbers, FSSAI regulations and healthy living in India.',
    url: 'https://www.parkho.in/blog',
    publisher: { '@type': 'Organization', name: 'Parkho', url: 'https://www.parkho.in' },
    hasPart: [...STATIC_BLOGS, ...dbBlogs].slice(0, 10).map(b => ({
      '@type': 'BlogPosting',
      headline: b.title,
      url: `https://www.parkho.in/blog/${b.slug}`,
      datePublished: b.created_at || '2025-01-01',
      author: { '@type': 'Person', name: b.author_name || 'Parkho Editorial' },
    })),
  }

  return (
    <>
    <SEO
      title="Blog — Food, Cosmetics & Healthy Living"
      description="Read expert articles about food ingredients, E-numbers, cosmetic safety, FSSAI regulations and healthy choices for Indian consumers. Written by nutritionists and consumer health experts."
      keywords="food ingredients blog India, cosmetic safety articles, E numbers explained India, FSSAI food additives, healthy eating India, Parkho blog"
      canonical="/blog"
      ogType="website"
      structuredData={blogListSchema}
    />
    <div className="min-h-screen bg-gray-50">

      {/* ── HERO BANNER ── */}
      <div className="relative overflow-hidden" style={{ minHeight: 320, background: '#0e1a2e' }}>

        {/* Left panel — food image */}
        <div className="absolute inset-y-0 left-0 overflow-hidden" style={{ width: '42%' }}>
          <img
            src="https://images.unsplash.com/photo-1490818387583-1baba5e638af?w=900&q=80"
            alt="" className="w-full h-full object-cover" style={{ opacity: 0.85 }}
          />
          <div className="absolute inset-0" style={{ background: 'linear-gradient(to right, rgba(14,26,46,0.1) 0%, rgba(14,26,46,0.98) 100%)' }} />
        </div>

        {/* Right panel — cosmetics image */}
        <div className="absolute inset-y-0 right-0 overflow-hidden" style={{ width: '42%' }}>
          <img
            src="https://images.unsplash.com/photo-1522335789203-aabd1fc54bc9?w=900&q=80"
            alt="" className="w-full h-full object-cover" style={{ opacity: 0.85 }}
          />
          <div className="absolute inset-0" style={{ background: 'linear-gradient(to left, rgba(14,26,46,0.1) 0%, rgba(14,26,46,0.98) 100%)' }} />
        </div>

        {/* Center dark background for text */}
        <div className="absolute inset-0" style={{ background: 'radial-gradient(ellipse 60% 100% at 50% 50%, rgba(14,26,46,0.55) 0%, transparent 100%)' }} />

        <div className="relative max-w-6xl mx-auto px-4 py-16 text-center">
          <div className="inline-flex items-center gap-2 bg-white/20 backdrop-blur-sm border border-white/30 rounded-full px-4 py-1.5 text-white text-xs font-semibold mb-5 tracking-widest uppercase">
            <span style={{ color: '#FF9933' }}>●</span> Community Knowledge Hub
          </div>
          <h1 className="font-poppins font-black text-white mb-2" style={{ fontSize: 'clamp(32px, 6vw, 58px)', letterSpacing: '-1px', textShadow: '0 2px 20px rgba(0,0,0,0.4)' }}>
            Parkho <span style={{ color: '#FF9933' }}>Blog</span>
          </h1>
          <p className="text-white/70 text-sm sm:text-base mb-1 font-semibold tracking-widest uppercase">Food · Cosmetics · Health · Lifestyle</p>
          <p className="text-white/60 text-sm max-w-lg mx-auto mt-3 leading-relaxed">
            Real insights from real people. Know what's in your products, understand ingredients, and make better choices.
          </p>
        </div>

        {/* Wave */}
        <div className="absolute bottom-0 left-0 right-0">
          <svg viewBox="0 0 1440 50" fill="none" xmlns="http://www.w3.org/2000/svg" preserveAspectRatio="none" style={{ display: 'block', width: '100%', height: 50 }}>
            <path d="M0 50L360 20L720 40L1080 15L1440 30V50H0Z" fill="#f9fafb"/>
          </svg>
        </div>
      </div>

      {/* ── CATEGORY FILTER ── */}
      <div className="max-w-6xl mx-auto px-4 pt-8 pb-2">
        <div className="flex gap-2 flex-wrap">
          {CATEGORIES.map(cat => (
            <button key={cat} onClick={() => setCategory(cat)}
              className="px-4 py-1.5 rounded-full text-sm font-semibold transition-all border"
              style={category === cat
                ? { background: '#1B3F8A', color: '#fff', borderColor: '#1B3F8A' }
                : { background: '#fff', color: '#6b7280', borderColor: '#e5e7eb' }}>
              {cat}
            </button>
          ))}
        </div>
      </div>

      {/* ── MAIN CONTENT ── */}
      <div className="max-w-6xl mx-auto px-4 py-8">

        {filtered.length === 0 ? (
          <div className="text-center py-20">
            <div className="text-5xl mb-4">📝</div>
            <h3 className="font-poppins font-bold text-navy text-xl mb-2">No blogs in this category yet</h3>
            <button onClick={() => user ? navigate('/blog/write') : openAuthModal()}
              style={{ background: '#FF9933' }}
              className="mt-4 text-white font-bold px-6 py-2.5 rounded-xl hover:opacity-90 transition-opacity">
              Write First Blog
            </button>
          </div>
        ) : (
          <>
            {/* ── FEATURED + SIDEBAR LAYOUT ── */}
            {featured && (
              <div className="grid grid-cols-1 lg:grid-cols-5 gap-6 mb-10">

                {/* Featured (large left) */}
                <Link to={`/blog/${featured.slug}`}
                  className="lg:col-span-3 relative rounded-2xl overflow-hidden group shadow-md"
                  style={{ minHeight: 420 }}>
                  <img
                    src={featured.cover_image || 'https://images.unsplash.com/photo-1512621776951-a57141f2eefd?w=800&q=80'}
                    alt={featured.title}
                    className="absolute inset-0 w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
                    onError={e => { e.target.onerror=null; e.target.src='https://images.unsplash.com/photo-1512621776951-a57141f2eefd?w=800&q=80' }}
                  />
                  <div className="absolute inset-0" style={{ background: 'linear-gradient(to top, rgba(0,0,0,0.85) 0%, rgba(0,0,0,0.3) 50%, rgba(0,0,0,0.05) 100%)' }} />
                  <div className="absolute inset-0 flex flex-col justify-end p-6 sm:p-8">
                    <CatBadge cat={featured.category} />
                    <h2 className="font-poppins font-black text-white text-xl sm:text-2xl leading-snug mt-3 mb-3 group-hover:text-orange-300 transition-colors">
                      {featured.title}
                    </h2>
                    <p className="text-gray-300 text-sm leading-relaxed mb-4 line-clamp-2"
                      style={{ display: '-webkit-box', WebkitLineClamp: 2, WebkitBoxOrient: 'vertical', overflow: 'hidden' }}>
                      {featured.excerpt}
                    </p>
                    <div className="flex items-center justify-between">
                      <div className="text-gray-400 text-xs">
                        ✍ <span className="text-white font-medium">{featured.author_name}</span> · {timeAgo(featured.created_at)}
                      </div>
                      <span className="inline-flex items-center gap-1.5 bg-white/20 backdrop-blur text-white text-xs font-bold px-4 py-2 rounded-xl hover:bg-orange-500 transition-colors">
                        READ MORE →
                      </span>
                    </div>
                  </div>
                </Link>

                {/* Sidebar (right) */}
                <div className="lg:col-span-2 flex flex-col gap-4">
                  {sideBlogs.map(blog => (
                    <Link key={blog.id} to={`/blog/${blog.slug}`}
                      className="bg-white rounded-2xl overflow-hidden shadow-sm hover:shadow-md transition-shadow group border border-gray-100 flex gap-0">
                      <div className="w-32 sm:w-36 flex-shrink-0 overflow-hidden">
                        <img
                          src={blog.cover_image || 'https://images.unsplash.com/photo-1512621776951-a57141f2eefd?w=400&q=80'}
                          alt={blog.title}
                          className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
                          style={{ minHeight: 110 }}
                          loading="lazy" decoding="async"
                          onError={e => { e.target.onerror=null; e.target.src='https://images.unsplash.com/photo-1512621776951-a57141f2eefd?w=400&q=80' }}
                        />
                      </div>
                      <div className="p-3 sm:p-4 flex flex-col justify-between flex-1">
                        <div>
                          <CatBadge cat={blog.category} />
                          <h3 className="font-poppins font-bold text-navy text-sm leading-snug mt-2 group-hover:text-orange-500 transition-colors"
                            style={{ display: '-webkit-box', WebkitLineClamp: 2, WebkitBoxOrient: 'vertical', overflow: 'hidden' }}>
                            {blog.title}
                          </h3>
                        </div>
                        <div className="text-xs text-gray-400 mt-2">
                          {blog.author_name} · {timeAgo(blog.created_at)}
                        </div>
                      </div>
                    </Link>
                  ))}
                </div>
              </div>
            )}

            {/* ── GRID: remaining blogs ── */}
            {gridBlogs.length > 0 && (
              <>
                <div className="flex items-center gap-3 mb-6">
                  <div className="h-px flex-1 bg-gray-200" />
                  <span className="text-xs font-bold text-gray-400 tracking-widest uppercase">More Articles</span>
                  <div className="h-px flex-1 bg-gray-200" />
                </div>
                <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
                  {gridBlogs.map(blog => (
                    <Link key={blog.id} to={`/blog/${blog.slug}`}
                      className="bg-white rounded-2xl overflow-hidden shadow-sm hover:shadow-md transition-shadow group border border-gray-100">
                      <div className="h-44 overflow-hidden relative">
                        <img
                          src={blog.cover_image || 'https://images.unsplash.com/photo-1512621776951-a57141f2eefd?w=600&q=80'}
                          alt={blog.title}
                          className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
                          loading="lazy" decoding="async"
                          onError={e => { e.target.onerror=null; e.target.src='https://images.unsplash.com/photo-1512621776951-a57141f2eefd?w=600&q=80' }}
                        />
                        <div className="absolute top-3 left-3">
                          <CatBadge cat={blog.category} />
                        </div>
                      </div>
                      <div className="p-5">
                        <h3 className="font-poppins font-bold text-navy text-base leading-snug mb-2 group-hover:text-orange-500 transition-colors"
                          style={{ display: '-webkit-box', WebkitLineClamp: 2, WebkitBoxOrient: 'vertical', overflow: 'hidden' }}>
                          {blog.title}
                        </h3>
                        <p className="text-gray-500 text-sm leading-relaxed"
                          style={{ display: '-webkit-box', WebkitLineClamp: 2, WebkitBoxOrient: 'vertical', overflow: 'hidden' }}>
                          {blog.excerpt}
                        </p>
                        <div className="flex items-center justify-between text-xs text-gray-400 mt-4 pt-3 border-t border-gray-100">
                          <span className="font-medium text-gray-600">✍ {blog.author_name}</span>
                          <span>{timeAgo(blog.created_at)}</span>
                        </div>
                      </div>
                    </Link>
                  ))}
                </div>
              </>
            )}
          </>
        )}

        {/* ── WRITE CTA BANNER ── */}
        <div className="mt-14 rounded-2xl overflow-hidden border border-gray-100 shadow-sm bg-white">
          <div className="flex flex-col sm:flex-row items-center gap-0">
            {/* Left image strip */}
            <div className="w-full sm:w-48 h-32 sm:h-auto flex-shrink-0 overflow-hidden">
              <img src="https://images.unsplash.com/photo-1455390582262-044cdead277a?w=400&q=80"
                alt="write" className="w-full h-full object-cover" style={{ minHeight: 140 }}
                onError={e => { e.target.onerror=null; e.target.style.display='none' }} />
            </div>
            {/* Content */}
            <div className="flex-1 flex flex-col sm:flex-row items-center justify-between gap-6 p-7 sm:p-8">
              <div>
                <div className="flex items-center gap-2 mb-2">
                  <div className="w-7 h-0.5 rounded" style={{ background: '#FF9933' }} />
                  <span className="text-xs font-bold tracking-widest uppercase" style={{ color: '#FF9933' }}>Share Your Knowledge</span>
                </div>
                <h3 className="font-poppins font-black text-2xl mb-1" style={{ color: '#1B3F8A' }}>Have something to share?</h3>
                <p className="text-gray-500 text-sm">Write about ingredients, products, or your health journey. Help others make better choices.</p>
              </div>
              <button onClick={() => user ? navigate('/blog/write') : openAuthModal()}
                style={{ background: '#1B3F8A', whiteSpace: 'nowrap' }}
                className="text-white font-bold px-8 py-3.5 rounded-xl hover:opacity-90 transition-opacity shadow-md text-sm flex-shrink-0">
                ✍️ Write a Blog
              </button>
            </div>
          </div>
        </div>

      </div>
    </div>
    </>
  )
}
