class Product {
  final String id;
  final String name;
  final String? brand;
  final String? category;
  final String grade;
  final String? imageUrl;
  final String? staticKey;
  final String? summary;
  final String? verdict;
  final String? recommendation;
  final List<Ingredient> ingredients;
  final String? ingredientsRaw;
  final String? fssaiNote;

  const Product({
    required this.id,
    required this.name,
    this.brand,
    this.category,
    required this.grade,
    this.imageUrl,
    this.staticKey,
    this.summary,
    this.verdict,
    this.recommendation,
    this.ingredients = const [],
    this.ingredientsRaw,
    this.fssaiNote,
  });

  factory Product.fromJson(Map<String, dynamic> j) => Product(
        id: j['id'] ?? '',
        name: j['name'] ?? '',
        brand: j['brand'],
        category: j['category'],
        grade: j['grade'] ?? 'D',
        imageUrl: j['image_url'],
        staticKey: j['static_key'],
        summary: j['summary'],
        verdict: j['verdict'],
        recommendation: j['recommendation'],
        ingredientsRaw: j['ingredients_raw'],
        fssaiNote: j['fssai_note'],
        ingredients: (j['ingredients'] as List<dynamic>? ?? [])
            .map((i) => Ingredient.fromJson(i as Map<String, dynamic>))
            .toList(),
      );
}

class Ingredient {
  final String name;
  final String classification;
  final String? concern;
  final String? regulatoryNote;
  final String? healthEffects;

  const Ingredient({
    required this.name,
    required this.classification,
    this.concern,
    this.regulatoryNote,
    this.healthEffects,
  });

  factory Ingredient.fromJson(Map<String, dynamic> j) => Ingredient(
        name: j['name'] ?? '',
        classification: j['classification'] ?? 'generally_recognised',
        concern: j['one_line_note'] ?? j['concern'],
        regulatoryNote: j['regulatory_note'],
        healthEffects: j['health_effects'],
      );

  bool get isQuestioned => classification == 'commonly_questioned';
  bool get isWorthKnowing => classification == 'worth_knowing';
  bool get isSafe => classification == 'generally_recognised';
}

class IngredientDetail {
  final String name;
  final String classification;
  final String? whatItIs;
  final String? oneLineNote;
  final String? regulatoryNote;
  final String? fssaiPosition;
  final String? commonlyFoundIn;
  final String? recommendation;
  final List<String> countriesRestricted;
  final Map<String, dynamic>? healthEffects;
  final List<Map<String, dynamic>> relatedIngredients;

  const IngredientDetail({
    required this.name,
    required this.classification,
    this.whatItIs,
    this.oneLineNote,
    this.regulatoryNote,
    this.fssaiPosition,
    this.commonlyFoundIn,
    this.recommendation,
    this.countriesRestricted = const [],
    this.healthEffects,
    this.relatedIngredients = const [],
  });

  factory IngredientDetail.fromJson(Map<String, dynamic> j) => IngredientDetail(
        name: j['name'] ?? '',
        classification: j['classification'] ?? 'generally_recognised',
        whatItIs: j['what_it_is'],
        oneLineNote: j['one_line_note'],
        regulatoryNote: j['regulatory_note'],
        fssaiPosition: j['fssai_position'],
        commonlyFoundIn: j['commonly_found_in'],
        recommendation: j['recommendation'],
        countriesRestricted:
            (j['countries_restricted'] as List<dynamic>? ?? []).cast<String>(),
        healthEffects: j['health_effects'] as Map<String, dynamic>?,
        relatedIngredients:
            (j['related_ingredients'] as List<dynamic>? ?? [])
                .cast<Map<String, dynamic>>(),
      );

  bool get isQuestioned => classification == 'commonly_questioned';
  bool get isWorthKnowing => classification == 'worth_knowing';
  bool get isSafe => classification == 'generally_recognised';
}
