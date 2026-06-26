import 'package:dio/dio.dart';
import 'package:flutter/material.dart';
import '../../core/config/app_config.dart';
import '../../core/theme/app_theme.dart';

const _staticContent = {
  'static-1': '''Most Indians pick up a packet of chips or biscuits without a second glance at the ingredient list. But what if that list told a very different story than the attractive packaging?

India's packaged food industry is booming. With over 40,000 food products on shelves, we're eating more processed food than ever before. And yet, most of us have no idea what's actually inside these products.

## What to look for on a food label

The first thing to understand is that ingredients are listed in descending order of quantity. So if sugar is the first ingredient in your "health" cereal — it's mostly sugar.

Common red flags to watch out for:
- **Partially hydrogenated oils**: A source of trans fats, linked to heart disease
- **High Fructose Corn Syrup (HFCS)**: Added sugar that's metabolised differently by your body
- **Artificial colours like Tartrazine (E102)**: Linked to hyperactivity in children
- **Sodium nitrite**: Used in processed meats, a known carcinogen at high levels
- **MSG**: While generally safe for most, causes reactions in sensitive individuals

## The "natural flavours" trick

Brands love to use the phrase "natural flavours" — but this can mean almost anything. Natural strawberry flavour can legally be derived from wood shavings treated with chemicals. It doesn't have to come from actual strawberries.

## What FSSAI requires

The Food Safety and Standards Authority of India (FSSAI) mandates that all packaged foods display a complete ingredient list, nutritional information per 100g, any allergens in bold, manufacturing and expiry date, and vegetarian/non-vegetarian symbol.

## Start small

You don't need to become an expert overnight. Start by checking the first three ingredients on your next grocery run. If you can't pronounce them or don't know what they are — look them up on Parkho before buying.''',

  'static-2': '''Walk into any pharmacy or beauty store in India and pick up a moisturiser. Flip it over. Chances are high you'll find methylparaben, propylparaben, or butylparaben somewhere in the ingredient list.

Parabens are preservatives. They've been used in cosmetics since the 1950s to prevent bacteria and mould from growing in your lotions and creams.

## Why people are worried

The alarm bells started in 2004 when a UK study found traces of parabens in breast tumour tissue. Headlines screamed that parabens cause cancer. Social media ran with it. "Paraben-free" became the hottest marketing claim in beauty.

But here's what that study actually showed: parabens were present in the tissue. It did NOT show that parabens caused the cancer. Correlation is not causation.

## What regulators say

The European Scientific Committee on Consumer Safety (SCCS) reviewed the evidence extensively. Their conclusion:
- Methylparaben and ethylparaben are safe at current use levels
- Propylparaben and butylparaben: safe below 0.19% concentration
- Isopropylparaben and isobutylparaben: insufficient safety data, best avoided

FSSAI in India follows similar guidelines. Most products use parabens at concentrations of 0.01–0.3%, well within safe limits.

## The bottom line

If you have sensitive skin or prefer to avoid them out of caution, go ahead — there are good paraben-free options. But don't panic if you see them on a label. The science does not support avoiding them entirely.''',

  'static-3': '''India has one of the highest rates of diabetes in the world — over 100 million diabetics and counting. Yet somehow, we're eating more "health foods" than ever. Something doesn't add up.

The problem isn't just mithai and soft drinks. The hidden sugar problem runs through foods we consider healthy.

## The usual suspects

**Packaged fruit juices**: A 200ml tetra pack of "100% fruit juice" can contain 20–25 grams of sugar. That's more sugar than a can of cola per 200ml. The fibre that slows sugar absorption in whole fruit is gone. What remains is essentially sugar water with vitamins.

**Flavoured yoghurt**: Plain dahi is one of the healthiest foods you can eat. Flavoured yoghurt brands add 15–25g of sugar per 100g serving. Check the label — sugar is often the second ingredient.

**Multigrain bread**: The word "multigrain" just means multiple grains. It doesn't mean whole grain, low-GI, or low-sugar. Many multigrain breads in India contain added sugar and refined flour as the primary ingredient.

**Breakfast cereals**: Some popular cereals marketed to children contain over 30% sugar by weight. They're cereal-flavoured candy, essentially.

## How sugar hides in ingredient lists

Manufacturers use many names for sugar to make it less obvious:
- Dextrose, fructose, sucrose, maltose
- Corn syrup, glucose syrup, high fructose corn syrup
- Fruit juice concentrate
- Cane juice, coconut sugar, jaggery
- Maltodextrin (acts like sugar in the body)

## What to do

Look at the nutritional information, not just the ingredients. Check "Total Sugars" per 100g. As a rule of thumb: under 5g per 100g = low sugar; 5–15g = moderate; over 15g = high sugar.

Real healthy eating in India doesn't need to be complicated. Dal, sabzi, roti, curd, fruits — traditional Indian food is naturally low in added sugar.''',

  'static-4': '''We put moisturiser on our face every single day. Which makes the ingredients in it especially important — because daily exposure to even small amounts of harmful chemicals adds up over time.

Here are five ingredients to watch for in your face cream.

## 1. Sodium Lauryl Sulphate (SLS)

SLS is a detergent that creates foam and lather. It's cheap, effective at cleaning, and harsh. In face creams, it can strip your skin's natural moisture barrier, cause irritation, and worsen conditions like rosacea and eczema.

## 2. Synthetic Fragrances (Parfum)

"Parfum" or "Fragrance" on an ingredient list is a legal black box. A single fragrance ingredient can contain up to 200 individual chemicals — and manufacturers don't have to disclose them. Synthetic fragrances are the number one cause of cosmetic allergic reactions.

## 3. Mineral Oil (Paraffinum Liquidum)

Derived from petroleum, mineral oil forms an occlusive layer on skin that traps moisture but also clogs pores. For oily or acne-prone skin, this can be problematic.

## 4. Oxybenzone (in SPF moisturisers)

If your daily moisturiser has SPF, check if oxybenzone is listed. This chemical UV filter has been detected in human blood, urine, and breast milk after topical application. The FDA has flagged it as needing more safety data.

## 5. Formaldehyde-releasing preservatives

DMDM Hydantoin, Imidazolidinyl Urea, Diazolidinyl Urea, and Quaternium-15 all release small amounts of formaldehyde over time. Formaldehyde is a known carcinogen and allergen. These are still legal and widely used in India.

## What to do

Start by checking the products you use on your face daily. Use Parkho to check any ingredient you're unsure about. Switching to cleaner formulations doesn't have to be expensive.''',

  'static-5': '''You've seen them on every packet of processed food: E102, E211, E621. These codes look technical and mysterious. But they're just a standardised numbering system for food additives approved for use in food production.

Not all E-numbers are harmful. Many are derived from natural sources. Here's how to make sense of them.

## How E-numbers are categorised

- E100–E199: Colours
- E200–E299: Preservatives
- E300–E399: Antioxidants
- E400–E499: Thickeners, stabilisers, emulsifiers
- E500–E599: Acidity regulators
- E600–E699: Flavour enhancers
- E900+: Sweeteners, glazing agents, others

## Commonly used and generally safe

**E300 (Vitamin C / Ascorbic acid)**: An antioxidant derived from vitamin C. Completely safe. Used to prevent oxidation and preserve colour.

**E322 (Lecithin)**: Usually derived from soy or sunflower. An emulsifier found in chocolate. Generally safe and occurs naturally in eggs.

**E330 (Citric acid)**: Found naturally in citrus fruits. Used as a preservative and flavour enhancer. Very safe.

**E440 (Pectin)**: Derived from fruit peels. Used as a gelling agent in jams. Completely natural and safe.

## Ones to be cautious about

**E102 (Tartrazine)**: A synthetic yellow dye. Linked to hyperactivity in children in some studies. Banned in Norway and Austria. Used widely in Indian snacks, drinks, and confectionery.

**E110 (Sunset Yellow)**: Another synthetic dye. Associated with allergic reactions, particularly in people sensitive to aspirin.

**E211 (Sodium Benzoate)**: A preservative. When combined with Vitamin C (E300) in acidic drinks, it can form benzene — a known carcinogen.

**E621 (MSG / Monosodium Glutamate)**: Generally considered safe by regulatory bodies, but some people report sensitivity symptoms.

## The simple rule

Numbers in the 100s (colours) and 200s (preservatives) deserve the most scrutiny. Numbers in the 300s and 400s are usually harmless or naturally derived.''',

  'static-6': '''Aqua. Glycerin. Niacinamide. Cetearyl Alcohol. If you've tried reading the back of a moisturiser and given up — you're not alone. Cosmetic ingredient lists (written in INCI format) look like a chemistry textbook.

But here's the secret: you only need to understand a few basics to become a smarter cosmetics consumer.

## What is INCI?

INCI stands for International Nomenclature of Cosmetic Ingredients. It's a standardised system used globally to name cosmetic ingredients. The same ingredient will have the same INCI name on a product sold in India, Europe, or the US.

## Rule 1: Order matters

Ingredients are listed in descending order by concentration. The first ingredient is present in the highest amount. Usually the first 1–5 ingredients make up 80–90% of the product.

If water (Aqua) is first — it's mostly water. If a "vitamin C serum" lists sodium ascorbyl phosphate 10th — there's very little actual vitamin C in it.

## Rule 2: The 1% threshold

After a certain point in the list, concentrations drop below 1%. Ingredients after this point can be listed in any order. This is where you'll often find preservatives, fragrances, and actives present in tiny amounts.

## Key ingredient categories to know

- **Humectants** (attract moisture): Glycerin, Hyaluronic Acid, Sodium PCA
- **Emollients** (soften skin): Squalane, Jojoba Oil, Cetearyl Alcohol
- **Occlusives** (seal in moisture): Petrolatum, Dimethicone, Beeswax
- **Actives** (target skin concerns): Niacinamide, Retinol, Salicylic Acid
- **Preservatives**: Phenoxyethanol, Parabens, DMDM Hydantoin

## Your cheat sheet

Next time you pick up a skincare product: check the first 5 ingredients, look for your target active and where it appears in the list, check for fragrance and known irritants, and use Parkho to look up anything unfamiliar.''',

  'static-7': '''In October 2015, the International Agency for Research on Cancer (IARC) released a report that made headlines worldwide. Processed meats were classified as Group 1 carcinogens.

The internet had a panic. But most of the coverage missed a critical distinction that changes everything.

## What "Group 1 carcinogen" actually means

Group 1 simply means there is sufficient evidence that the substance causes cancer in humans. It says nothing about how much cancer risk is involved. This is where the cigarette comparison breaks down completely.

Tobacco smoking causes approximately 19% of all cancers globally. Processed meat consumption at current average intake levels is associated with approximately a 17–18% relative increase in colorectal cancer risk — which translates to an absolute increase of about 1% in lifetime colorectal cancer risk.

## What counts as processed meat?

The WHO defines processed meat as meat that has been transformed through salting, curing, fermentation, smoking or other processes. This includes:
- Sausages, frankfurters, hot dogs
- Ham, bacon, salami, pepperoni
- Corned beef and canned meat
- Biltong and beef jerky

## Why does processed meat raise cancer risk?

Three main mechanisms: N-nitrosamines formed during processing, haem iron in red meat, and heterocyclic amines (HCAs) from high-temperature cooking.

## The dose matters enormously

The IARC analysis found that eating 50g of processed meat per day — roughly two slices of bacon or one sausage — was associated with an 18% increase in relative risk of colorectal cancer.

People who eat processed meat occasionally, as a small component of an otherwise vegetable and fibre-rich diet, are at significantly lower risk than daily consumers.''',

  'static-8': '''For decades, artificial sweeteners seemed like the perfect solution: all the sweetness of sugar, none of the calories, no blood glucose spike. Then 2023 arrived with research findings that complicated the picture considerably.

## The WHO advisory of 2023

In May 2023, the World Health Organisation released a guideline recommending against the use of non-sugar sweeteners for weight control. The WHO reviewed 283 studies and concluded that using sweeteners does not help with long-term weight management.

## What happened with aspartame

In July 2023, IARC classified aspartame as "possibly carcinogenic to humans" (Group 2B). Simultaneously, the WHO's JECFA committee maintained the acceptable daily intake of 40 mg/kg body weight as safe — meaning a 70 kg person would need to consume 9–14 cans of diet soda daily to approach the limit.

Both are simultaneously true because IARC evaluates whether a substance can cause cancer at any dose, while JECFA evaluates harm at typical intake levels.

## The sucralose finding that surprised researchers

A 2023 paper found that sucralose-6-acetate — a metabolite in commercial sucralose — is genotoxic in vitro, causing DNA strand breaks in human cells. EFSA and FDA have not changed safety classifications for sucralose in response.

## Stevia: the cleanest profile

Stevia (steviol glycosides, E960) continues to have the most favourable safety profile. FDA GRAS; no gut microbiome disruption in short-term human studies; some data suggesting modest blood pressure-lowering effects.

## What should you use?

Based on current evidence: stevia is the best-evidenced choice; erythritol at moderate amounts is likely fine; aspartame at moderate intake (1–2 diet drinks/day) is probably safe. The bigger principle: no sweetener is superior to gradually reducing overall sweetness preference.''',

  'static-9': '''"Processed food is bad." You've heard it. But it is an oversimplification that creates more confusion than clarity. Yoghurt is processed. Cheese is processed. Frozen vegetables are processed. So is bread.

The problem is that we have been lumping all processed food together. A food classification system called NOVA has been changing how nutrition scientists think about this.

## What is NOVA?

Developed by Carlos Monteiro and colleagues at the University of Sao Paulo, NOVA classifies food into four groups based on the extent and purpose of processing.

- **Group 1**: Unprocessed or minimally processed foods — fresh fruit, vegetables, plain meat, eggs, milk, plain pulses, nuts, seeds.
- **Group 2**: Processed culinary ingredients — oils, butter, ghee, salt, sugar, flour. Not meant to be eaten alone.
- **Group 3**: Processed foods — tinned tomatoes, cheese, cured meats, pickles, freshly baked bread. Processing serves to preserve food or enhance taste.
- **Group 4**: Ultra-processed foods (UPF) — industrial formulations made from extracted or synthesised substances. Designed for hyperpalatability — engineered to make you eat more.

Common UPF in India: instant noodles, packaged biscuits and chips, carbonated beverages, flavoured milk drinks, packaged breakfast cereals, processed cheese slices.

## The clinical evidence

A landmark 2019 randomised controlled trial at the US National Institutes of Health found that on an ultra-processed diet, participants consumed an average of 508 additional calories per day compared to the unprocessed diet — and gained approximately 0.9 kg.

## What this means for India

India is undergoing one of the fastest nutritional transitions in the world. Urban Indians are rapidly shifting from traditional Group 1/2/3 diets (dal, sabzi, roti, rice, curd) to ultra-processed food as primary sources of calories.

NOVA gives us a more useful question than "is this food healthy?" Ask instead: "Is this food recognisable as something that came from nature, or is it an industrial product engineered from food substances?"''',

  'static-10': '''If you had to pick one skincare ingredient with the strongest clinical evidence for anti-ageing, it would be retinol — a derivative of Vitamin A that has been studied continuously since the 1970s.

## What retinol actually does

Retinol belongs to a class of compounds called retinoids. When applied to skin, retinol undergoes a two-step conversion: Retinol → Retinaldehyde → Retinoic acid (the biologically active form).

Retinoic acid triggers changes in gene expression that produce four measurable effects: increased cell turnover, stimulation of collagen synthesis, normalisation of follicular keratinisation, and inhibition of melanin synthesis.

## The clinical evidence

A 1993 trial published in the New England Journal of Medicine demonstrated that 0.1% tretinoin significantly reduced fine wrinkles, mottled pigmentation, and skin roughness versus placebo over 48 weeks — with histological evidence of new collagen formation.

A 2007 study showed that even 0.4% retinol — the over-the-counter concentration — significantly increased collagen production and improved skin thickness.

## The retinoid hierarchy

From weakest to strongest: Retinyl palmitate → Retinol → Retinaldehyde (retinal) → Tretinoin (retinoic acid).

Tretinoin is the prescription form. Retinol is the most common OTC option. At 0.1–0.5%, it produces measurable clinical results over 6–12 months of consistent use.

## The retinoid reaction: why people give up too soon

The most common reason people abandon retinol: they experience redness, flaking, dryness in the first 4–8 weeks and assume the product is damaging their skin. The "retinoid reaction" is normal — skin fully acclimatises within 8–12 weeks.

## Who must avoid retinol

This is critical. All retinoids are contraindicated in pregnancy. Pregnant women and women trying to conceive should avoid all topical retinoids as a precaution.''',

  'static-11': '''Sunscreen is the single most evidence-backed anti-ageing skincare product that exists. But the debate about chemical versus mineral sunscreen has intensified over the past five years, driven by real regulatory action.

## The fundamental difference

**Chemical UV filters** — oxybenzone, octinoxate, avobenzone, octocrylene, homosalate — work by absorbing UV photons and converting them to heat.

**Mineral UV filters** — zinc oxide and titanium dioxide — work by scattering and reflecting UV photons. They are photostable, provide broad-spectrum UVA and UVB coverage, and leave a white cast.

## What the FDA found

In 2019, the FDA released a proposed rule. Only zinc oxide and titanium dioxide had sufficient safety data to be classified as "generally recognised as safe and effective" (GRASE). Four chemical filters — oxybenzone, octinoxate, homosalate, and octisalate — were classified as "not GRASE" due to insufficient systemic absorption safety data.

A subsequent 2020 FDA clinical study found that blood levels of oxybenzone, octinoxate, octocrylene, and homosalate exceeded the FDA's safety threshold after a single day of whole-body application.

## Specific concerns with key chemical filters

- **Oxybenzone**: Significantly absorbed through skin — detected in blood, urine, and breast milk. Animal studies show oestrogenic activity. Banned in Hawaii and Palau.
- **Octinoxate**: Weak oestrogen and anti-androgen activity in animal studies. Banned in Hawaii.
- **Octocrylene**: Increasingly recognised as a significant contact allergen.

## The case for mineral sunscreens

Zinc oxide and titanium dioxide: not systemically absorbed, photostable, provide broad-spectrum protection, no endocrine disruption concerns, and are not toxic to coral reefs.

## What this means for Indian skin

For everyday facial use: a zinc oxide-based mineral sunscreen provides the most complete safety profile. For children: mineral sunscreens are strongly preferred.

The non-negotiable rule: wear sunscreen every day.''',

  'static-12': '''Walk into any dermatologist's office with a skin complaint and the first question is almost never "which serum should I try?" It is almost always about your cleansing routine or how many active ingredients you are using at once.

No active ingredient, however well-formulated, works optimally on a compromised skin barrier.

## What the skin barrier actually is

The skin barrier refers primarily to the outermost layer of the epidermis: the stratum corneum. It is described using a "brick and mortar" analogy — dead skin cells (corneocytes, the bricks) held together by a lipid matrix (the mortar) composed of ceramides (approximately 50%), cholesterol (25%), and free fatty acids (15%).

This structure prevents water loss, acts as a physical barrier to pathogens and allergens, and maintains an acidic pH of approximately 4.5–5.5 (the "acid mantle").

## What is silently damaging your skin barrier

**Over-cleansing**: Soaps and many foaming cleansers are alkaline (pH 9–11) — far above the skin's natural pH of 4.5–5.5. A single wash with an alkaline cleanser disrupts the acid mantle for 1.5–3 hours.

Signs of over-cleansing: skin feels "squeaky clean" after washing, persistent tightness, increased oiliness as the skin overcompensates.

**Over-exfoliation**: AHAs, BHAs, physical scrubs, and retinoids all accelerate cell turnover. Used too aggressively in combination, they thin the stratum corneum faster than it can regenerate.

**Alcohol-heavy toners**: SD alcohol and alcohol denat disrupt ceramide synthesis and increase water loss with repeated use.

**Hard water**: Delhi, Mumbai, and much of urban India have hard tap water. Hard water forms insoluble deposits on skin, disrupts pH, and depletes natural moisturising factors.

## The ceramide research

Ceramides are the most critical components of the skin barrier. A 2020 systematic review found ceramide-containing moisturisers significantly reduced water loss and improved skin hydration in eczema patients.

## A barrier-first approach

Before adding any active ingredient — retinol, vitamin C, AHA, BHA — ask whether your barrier is intact. If you have new sensitivities, persistent redness, or skin that feels tight after cleansing: gentle cleanser, ceramide-based moisturiser, SPF, and nothing else for 4–6 weeks. Let your barrier repair.

The most expensive skincare routine cannot work effectively on a broken barrier.''',
};

const _staticMeta = {
  'static-1':  (title: 'Why You Should Read Food Labels Before Buying Packaged Snacks in India', category: 'Food',      author: 'Parkho Editorial', date: 'Jan 2026', cover: 'https://images.unsplash.com/photo-1606787366850-de6330128bfc?w=800&q=70'),
  'static-2':  (title: 'Parabens in Indian Skincare: Should You Really Be Worried?',            category: 'Cosmetics',  author: 'Parkho Editorial', date: 'Jan 2026', cover: 'https://images.unsplash.com/photo-1556228578-8c89e6adf883?w=800&q=70'),
  'static-3':  (title: 'Hidden Sugar in "Healthy" Indian Foods — What Brands Don\'t Tell You',  category: 'Food',       author: 'Parkho Editorial', date: 'Jan 2026', cover: 'https://images.unsplash.com/photo-1490645935967-10de6ba17061?w=800&q=70'),
  'static-4':  (title: '5 Harmful Ingredients Hiding in Your Daily Face Cream',                 category: 'Cosmetics',  author: 'Parkho Editorial', date: 'Jan 2026', cover: 'https://images.unsplash.com/photo-1598440947619-2c35fc9aa908?w=800&q=70'),
  'static-5':  (title: 'E-Numbers in Indian Food: Which Are Safe and Which to Avoid',           category: 'Food',       author: 'Parkho Editorial', date: 'Feb 2026', cover: 'https://images.unsplash.com/photo-1567306226416-28f0efdc88ce?w=800&q=70'),
  'static-6':  (title: 'How to Read a Cosmetic Ingredient List Like an Expert',                 category: 'Cosmetics',  author: 'Parkho Editorial', date: 'Feb 2026', cover: 'https://images.unsplash.com/photo-1596755389378-c31d21fd1273?w=800&q=70'),
  'static-7':  (title: 'Processed Meats and Cancer: What the WHO Classification Actually Means',category: 'Food',       author: 'Parkho Editorial', date: 'Feb 2026', cover: 'https://images.unsplash.com/photo-1504674900247-0877df9cc836?w=800&q=70'),
  'static-8':  (title: 'Aspartame, Sucralose or Stevia? What 2023 Research Changed About Artificial Sweeteners', category: 'Food', author: 'Parkho Editorial', date: 'Mar 2026', cover: 'https://images.unsplash.com/photo-1548636581-eb82ef43c3ec?w=800&q=70'),
  'static-9':  (title: 'The Ultra-Processed Food Trap: Why the NOVA Classification Is Changing Nutrition Science', category: 'Food', author: 'Parkho Editorial', date: 'Mar 2026', cover: 'https://images.unsplash.com/photo-1565299624946-b28f40a0ae38?w=800&q=70'),
  'static-10': (title: 'Retinol: The Science Behind the Most Clinically Proven Anti-Ageing Skincare Ingredient',  category: 'Cosmetics', author: 'Parkho Editorial', date: 'Mar 2026', cover: 'https://images.unsplash.com/photo-1620916566398-39f1143ab7be?w=800&q=70'),
  'static-11': (title: 'Chemical vs Mineral Sunscreen: What the Science Actually Says in 2024', category: 'Cosmetics',  author: 'Parkho Editorial', date: 'Apr 2026', cover: 'https://images.unsplash.com/photo-1526947425960-945c6e72858f?w=800&q=70'),
  'static-12': (title: 'Your Skin Barrier: The Science Behind Why It Matters More Than Any Serum', category: 'Cosmetics', author: 'Parkho Editorial', date: 'Apr 2026', cover: 'https://images.unsplash.com/photo-1631729371254-42c2892f0e6e?w=800&q=70'),
};

class BlogPostScreen extends StatefulWidget {
  final String slug;
  final bool isDynamic;
  const BlogPostScreen({super.key, required this.slug, this.isDynamic = false});

  @override
  State<BlogPostScreen> createState() => _BlogPostScreenState();
}

class _BlogPostScreenState extends State<BlogPostScreen> {
  Map<String, dynamic>? _post;
  bool   _loading = true;
  String? _error;

  @override
  void initState() {
    super.initState();
    _load();
  }

  Future<void> _load() async {
    if (!widget.isDynamic && _staticContent.containsKey(widget.slug)) {
      setState(() => _loading = false);
      return;
    }
    try {
      final dio = Dio();
      final res = await dio.get(
        '$supabaseUrl/rest/v1/blogs',
        queryParameters: {'or': '(slug.eq.${widget.slug},id.eq.${widget.slug})', 'status': 'eq.approved', 'limit': '1'},
        options: Options(headers: {'apikey': supabaseAnonKey}),
      );
      final list = res.data as List;
      if (mounted) setState(() { _post = list.isNotEmpty ? list.first as Map<String, dynamic> : null; _loading = false; });
    } catch (e) {
      if (mounted) setState(() { _error = 'Could not load this post. Please try again.'; _loading = false; });
    }
  }

  @override
  Widget build(BuildContext context) {
    if (_loading) return const Scaffold(body: Center(child: CircularProgressIndicator(color: AppColors.brandOrange)));
    if (_error != null) return Scaffold(appBar: AppBar(), body: Center(child: Text(_error!, style: const TextStyle(color: AppColors.textMuted))));

    final isStatic = _staticContent.containsKey(widget.slug) && !widget.isDynamic;
    final meta     = isStatic ? _staticMeta[widget.slug] : null;
    final content  = isStatic ? (_staticContent[widget.slug] ?? '') : (_post?['content'] as String? ?? '');

    final title    = meta?.title    ?? (_post?['title']       as String? ?? '');
    final author   = meta?.author   ?? (_post?['author_name'] as String? ?? 'Contributor');
    final category = meta?.category ?? (_post?['category']    as String? ?? '');
    final date     = meta?.date     ?? ((_post?['created_at'] as String? ?? '').substring(0, 10));
    final cover    = meta?.cover    ?? (_post?['cover_image'] as String?);

    return Scaffold(
      backgroundColor: Colors.white,
      body: CustomScrollView(
        slivers: [
          SliverAppBar(
            backgroundColor: AppColors.textPrimary,
            foregroundColor: Colors.white,
            pinned: true,
            expandedHeight: cover != null ? 220 : 0,
            flexibleSpace: cover != null
                ? FlexibleSpaceBar(background: Image.network(cover, fit: BoxFit.cover, errorBuilder: (_, __, ___) => const SizedBox()))
                : null,
          ),
          SliverToBoxAdapter(
            child: Padding(
              padding: const EdgeInsets.fromLTRB(20, 20, 20, 48),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  if (category.isNotEmpty)
                    Container(
                      padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 5),
                      decoration: BoxDecoration(color: const Color(0xFFFFF7ED), borderRadius: BorderRadius.circular(20)),
                      child: Text(category, style: const TextStyle(fontSize: 11, fontWeight: FontWeight.w700, color: AppColors.brandOrange)),
                    ),
                  const SizedBox(height: 10),
                  Text(title, style: const TextStyle(fontSize: 22, fontWeight: FontWeight.w900, color: AppColors.textPrimary, fontFamily: 'Poppins', height: 1.3)),
                  const SizedBox(height: 10),
                  Row(children: [
                    const Icon(Icons.person_outline, size: 14, color: AppColors.textMuted),
                    const SizedBox(width: 4),
                    Text(author, style: const TextStyle(fontSize: 12, color: AppColors.textMuted)),
                    if (date.isNotEmpty) ...[
                      const SizedBox(width: 12),
                      const Icon(Icons.calendar_today_outlined, size: 12, color: AppColors.textMuted),
                      const SizedBox(width: 4),
                      Text(date, style: const TextStyle(fontSize: 12, color: AppColors.textMuted)),
                    ],
                  ]),
                  const SizedBox(height: 20),
                  const Divider(),
                  const SizedBox(height: 20),
                  _SimpleMarkdown(content),
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }
}

// ── Lightweight markdown renderer ─────────────────────────────────────────────

class _SimpleMarkdown extends StatelessWidget {
  final String text;
  const _SimpleMarkdown(this.text);

  @override
  Widget build(BuildContext context) {
    final lines = text.split('\n');
    final widgets = <Widget>[];

    for (int i = 0; i < lines.length; i++) {
      final line = lines[i];
      if (line.startsWith('## ')) {
        widgets.add(Padding(
          padding: const EdgeInsets.only(top: 22, bottom: 8),
          child: Text(line.substring(3), style: const TextStyle(fontSize: 18, fontWeight: FontWeight.w800, color: AppColors.textPrimary, fontFamily: 'Poppins')),
        ));
      } else if (line.startsWith('### ')) {
        widgets.add(Padding(
          padding: const EdgeInsets.only(top: 14, bottom: 4),
          child: Text(line.substring(4), style: const TextStyle(fontSize: 15, fontWeight: FontWeight.w700, color: AppColors.textPrimary)),
        ));
      } else if (line.startsWith('- ')) {
        widgets.add(Padding(
          padding: const EdgeInsets.only(bottom: 6, left: 4),
          child: Row(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              const Padding(
                padding: EdgeInsets.only(top: 7),
                child: CircleAvatar(radius: 3, backgroundColor: AppColors.brandOrange),
              ),
              const SizedBox(width: 10),
              Expanded(child: _InlineText(line.substring(2))),
            ],
          ),
        ));
      } else if (line.isEmpty) {
        widgets.add(const SizedBox(height: 10));
      } else {
        widgets.add(Padding(
          padding: const EdgeInsets.only(bottom: 4),
          child: _InlineText(line),
        ));
      }
    }

    return Column(crossAxisAlignment: CrossAxisAlignment.start, children: widgets);
  }
}

class _InlineText extends StatelessWidget {
  final String text;
  const _InlineText(this.text);

  @override
  Widget build(BuildContext context) {
    final spans = <TextSpan>[];
    final pattern = RegExp(r'\*\*(.+?)\*\*');
    int last = 0;
    for (final m in pattern.allMatches(text)) {
      if (m.start > last) spans.add(TextSpan(text: text.substring(last, m.start)));
      spans.add(TextSpan(text: m.group(1), style: const TextStyle(fontWeight: FontWeight.w700, color: AppColors.textPrimary)));
      last = m.end;
    }
    if (last < text.length) spans.add(TextSpan(text: text.substring(last)));
    return RichText(
      text: TextSpan(
        style: const TextStyle(fontSize: 14, color: Color(0xFF374151), height: 1.8, fontFamily: 'Poppins'),
        children: spans,
      ),
    );
  }
}
