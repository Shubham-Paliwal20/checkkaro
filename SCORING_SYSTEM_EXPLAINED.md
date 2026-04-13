# CheckKaro Awareness Score Calculation

## Overview

The **Awareness Score** is a number from **0 to 100** that indicates how many ingredients in a product are subject to regulatory scrutiny, restrictions, or scientific debate.

- **Higher score (80-100)** = Most ingredients are generally recognised
- **Medium score (50-79)** = Some ingredients worth knowing about
- **Lower score (0-49)** = Several ingredients commonly questioned

---

## Calculation Method

### Starting Point
**Every product starts at 100 points**

### Step 1: Basic Classification Penalties

For **EACH ingredient** in the product, subtract points based on its classification:

| Classification | Points Deducted | Meaning |
|----------------|-----------------|---------|
| **Generally Recognised** | -0 points | No regulatory flags, no restrictions, no debates |
| **Worth Knowing** | -8 points | Has concentration limits OR usage restrictions OR discussed in research |
| **Commonly Questioned** | -20 points | Restricted/banned somewhere OR flagged by regulators OR subject to debate |

### Step 2: Additional Penalties (Cumulative)

For **EACH ingredient**, check ALL of these conditions and apply penalties that match:

| Condition | Points Deducted | Example |
|-----------|-----------------|---------|
| Banned in EU | -15 points | Titanium Dioxide (E171) |
| Banned in Canada | -15 points | Potassium Bromate |
| Restricted by WHO | -12 points | Trans fats |
| Has FSSAI concentration limits | -8 points | Sodium Benzoate |
| Linked to skin sensitization/allergies | -8 points | Fragrance, Parabens |
| Endocrine disruptor concerns | -15 points | Parabens, BPA |
| Flagged in carcinogenicity studies | -20 points | Certain food dyes |
| Banned in ANY other country | -10 points | Various additives |

**Important:** These penalties are **cumulative** - one ingredient can trigger multiple penalties!

### Step 3: Final Score

- **Minimum:** 0 (cannot go below zero)
- **Maximum:** 100 (starting point)

---

## Example Calculations

### Example 1: Simple Product (High Score)

**Product:** Plain Rice
**Ingredients:** Rice, Water, Salt

**Calculation:**
```
Starting score: 100

Ingredient 1: Rice
- Classification: Generally Recognised → -0 points
- No additional penalties → -0 points

Ingredient 2: Water
- Classification: Generally Recognised → -0 points
- No additional penalties → -0 points

Ingredient 3: Salt
- Classification: Generally Recognised → -0 points
- No additional penalties → -0 points

Final Score: 100 - 0 = 100
Verdict: "Generally recognised ingredients"
```

---

### Example 2: Moderate Product (Medium Score)

**Product:** Maggi Noodles
**Ingredients:** Wheat Flour, Palm Oil, Salt, Wheat Gluten, Guar Gum, Sodium Carbonate, Sodium Phosphate, Potassium Carbonate

**Calculation:**
```
Starting score: 100

Ingredient 1: Wheat Flour
- Classification: Generally Recognised → -0 points

Ingredient 2: Palm Oil
- Classification: Worth Knowing → -8 points
- (Environmental concerns, not health)

Ingredient 3: Salt
- Classification: Generally Recognised → -0 points

Ingredient 4: Wheat Gluten
- Classification: Worth Knowing → -8 points
- (Allergen concerns)
- Linked to allergies → -8 points

Ingredient 5: Guar Gum
- Classification: Generally Recognised → -0 points

Ingredient 6: Sodium Carbonate
- Classification: Worth Knowing → -8 points
- Has FSSAI limits → -8 points

Ingredient 7: Sodium Phosphate
- Classification: Worth Knowing → -8 points
- Has FSSAI limits → -8 points

Ingredient 8: Potassium Carbonate
- Classification: Worth Knowing → -8 points
- Has FSSAI limits → -8 points

Total deductions: 0 + 8 + 0 + 8 + 8 + 0 + 8 + 8 + 8 + 8 + 8 + 8 = 72

Final Score: 100 - 72 = 28
Verdict: "Many ingredients subject to restrictions"
```

---

### Example 3: Problematic Product (Low Score)

**Product:** Dove Soap (Hypothetical)
**Ingredients:** Sodium Lauroyl Isethionate, Stearic Acid, Sodium Tallowate, Lauric Acid, Sodium Isethionate, Water, Sodium Stearate, Cocamidopropyl Betaine, Fragrance, Sodium Dodecylbenzenesulfonate, Titanium Dioxide, Tetrasodium EDTA, Methylparaben, Propylparaben

**Calculation:**
```
Starting score: 100

Ingredients 1-7: Generally Recognised
- Total: -0 points

Ingredient 8: Cocamidopropyl Betaine
- Classification: Worth Knowing → -8 points
- Skin sensitization → -8 points

Ingredient 9: Fragrance
- Classification: Worth Knowing → -8 points
- Skin sensitization → -8 points
- Allergen concerns → -8 points

Ingredient 10: Sodium Dodecylbenzenesulfonate
- Classification: Worth Knowing → -8 points
- Has FSSAI limits → -8 points

Ingredient 11: Titanium Dioxide
- Classification: Commonly Questioned → -20 points
- Banned in EU (food use) → -15 points
- Subject to research → -0 (already counted)

Ingredient 12: Tetrasodium EDTA
- Classification: Worth Knowing → -8 points
- Has concentration limits → -8 points

Ingredient 13: Methylparaben
- Classification: Commonly Questioned → -20 points
- Endocrine disruptor concerns → -15 points
- Banned in some countries → -10 points

Ingredient 14: Propylparaben
- Classification: Commonly Questioned → -20 points
- Endocrine disruptor concerns → -15 points
- Banned in some countries → -10 points

Total deductions: 
0 + 8 + 8 + 8 + 8 + 8 + 8 + 20 + 15 + 8 + 8 + 20 + 15 + 10 + 20 + 15 + 10 = 189

But score cannot go below 0!

Final Score: 100 - 189 = 0 (capped at minimum)
Verdict: "Many ingredients subject to restrictions"
```

---

## Score Ranges & Verdicts

### 80-100: Generally Recognised Ingredients
- Most/all ingredients have no regulatory flags
- No restrictions in major jurisdictions
- No ongoing scientific debates
- **Example:** Plain rice, water, basic salt

### 60-79: Worth Knowing About Some Ingredients
- Some ingredients have concentration limits
- Minor restrictions in some countries
- Some ingredients discussed in research
- **Example:** Packaged bread, basic snacks

### 40-59: Several Ingredients Commonly Questioned
- Multiple ingredients with restrictions
- Some banned in certain countries
- Subject to regulatory scrutiny
- **Example:** Processed foods with preservatives

### 0-39: Many Ingredients Subject to Restrictions
- Many ingredients banned/restricted somewhere
- Multiple regulatory flags
- Significant scientific debate
- **Example:** Highly processed foods, some cosmetics

---

## Recommendations Based on Score

### Score 70-100
**Recommendation:** "Can be used with general awareness"
- Product has mostly recognised ingredients
- Minimal regulatory concerns
- Standard consumer awareness sufficient

### Score 50-69
**Recommendation:** "Use with awareness of flagged ingredients"
- Some ingredients worth knowing about
- Check specific ingredients if concerned
- Consider alternatives if sensitive

### Score 0-49
**Recommendation:** "Consider alternatives with fewer questioned ingredients"
- Multiple ingredients with concerns
- Significant regulatory flags
- May want to explore alternatives

---

## Classification Criteria

### Generally Recognised
**Criteria:** ALL of these must be true:
- ✅ ZERO regulatory flags in US, EU, India, Canada, Australia, Japan
- ✅ ZERO usage restrictions anywhere
- ✅ ZERO concentration limits
- ✅ ZERO scientific debates
- ✅ ZERO bans in any country

**Examples:**
- Water
- Salt (sodium chloride)
- Sugar (sucrose)
- Rice
- Wheat flour (plain)

### Worth Knowing
**Criteria:** ANY of these is true:
- ⚠️ Has concentration limits in ANY country
- ⚠️ Usage restrictions in ANY country
- ⚠️ Discussed in peer-reviewed research with concerns
- ⚠️ Allergen for some people
- ⚠️ Environmental concerns

**Examples:**
- Sodium Benzoate (preservative with limits)
- Palm Oil (environmental concerns)
- Wheat Gluten (allergen)
- Artificial colors (concentration limits)

### Commonly Questioned
**Criteria:** ANY of these is true:
- ❌ Restricted or banned in ANY country
- ❌ Flagged by ANY regulatory body (EU, FDA, Health Canada, FSSAI)
- ❌ Subject to scientific debate
- ❌ Endocrine disruptor concerns
- ❌ Carcinogenicity studies

**Examples:**
- Parabens (endocrine disruptor concerns)
- Titanium Dioxide (banned in EU food)
- Potassium Bromate (banned in many countries)
- Certain artificial colors (banned in some countries)

---

## Data Sources

The AI uses information from:

1. **FSSAI** (Food Safety and Standards Authority of India)
   - Indian food regulations
   - Permitted additives and limits
   - Labeling requirements

2. **WHO** (World Health Organization)
   - International health guidelines
   - Safety assessments
   - Recommended limits

3. **EFSA** (European Food Safety Authority)
   - EU regulations
   - Scientific opinions
   - Risk assessments

4. **FDA** (US Food and Drug Administration)
   - US regulations
   - GRAS (Generally Recognized as Safe) list
   - Banned substances

5. **Health Canada**
   - Canadian regulations
   - Permitted additives
   - Restricted substances

6. **Peer-reviewed Research**
   - Scientific studies
   - Toxicology reports
   - Clinical trials

---

## Important Notes

### 1. Not a Health Assessment
The awareness score is **NOT**:
- ❌ A health rating
- ❌ Medical advice
- ❌ A safety certification
- ❌ A recommendation to use or avoid

It **IS**:
- ✅ An awareness indicator
- ✅ Based on regulatory data
- ✅ Educational information
- ✅ A starting point for research

### 2. Context Matters
- Concentration matters (small amounts vs large amounts)
- Usage matters (food vs cosmetics vs industrial)
- Individual sensitivity varies
- Regulations change over time

### 3. Strict Scoring
The system is intentionally **very strict**:
- Even minor concerns reduce the score
- Multiple penalties can stack
- Errs on the side of caution
- Encourages consumer awareness

---

## Examples by Product Type

### High Score Products (80-100)
- Plain rice
- Fresh fruits and vegetables
- Plain water
- Basic salt
- Plain flour
- Unprocessed foods

### Medium Score Products (50-79)
- Packaged bread
- Basic snacks
- Simple beverages
- Lightly processed foods
- Products with few additives

### Low Score Products (0-49)
- Highly processed foods
- Products with many preservatives
- Artificial colors/flavors
- Some cosmetics
- Products with banned ingredients

---

## How to Interpret Your Product's Score

### Score: 85 (Example: Parle G Biscuits)
```
✅ Good Score
- Most ingredients generally recognised
- Few or no regulatory concerns
- Standard awareness sufficient
- Can be used with general awareness
```

### Score: 60 (Example: Packaged Juice)
```
⚠️ Moderate Score
- Some ingredients worth knowing about
- Minor regulatory concerns
- Check specific ingredients if concerned
- Use with awareness of flagged ingredients
```

### Score: 35 (Example: Highly Processed Snack)
```
❌ Low Score
- Many ingredients commonly questioned
- Multiple regulatory flags
- Significant concerns
- Consider alternatives with fewer questioned ingredients
```

---

## Frequently Asked Questions

### Q: Why did my product get a low score?
**A:** The score reflects regulatory flags and restrictions. Even one ingredient banned in a major country can significantly reduce the score.

### Q: Is a low score bad?
**A:** Not necessarily "bad" - it means the product has ingredients that are subject to regulatory scrutiny or debate. It's information for awareness, not a health verdict.

### Q: Can the score change?
**A:** Yes! As regulations change and new research emerges, classifications can change. We update based on latest data.

### Q: Why is the scoring so strict?
**A:** We err on the side of caution and transparency. We want users to be aware of ANY regulatory concerns, even minor ones.

### Q: What if I disagree with the score?
**A:** The score is based on regulatory data, not opinions. However, you can submit corrections if you have official documentation showing different information.

---

## Summary

The Awareness Score is calculated by:

1. **Starting at 100**
2. **Subtracting points** for each ingredient based on:
   - Classification (0, 8, or 20 points)
   - Additional penalties (up to 20 points each)
3. **Capping at 0 minimum**

The system is **intentionally strict** to encourage consumer awareness and transparency about ingredients that are subject to any regulatory scrutiny or scientific debate.

**Remember:** This is educational information, not medical advice. Always consult healthcare professionals for personal health decisions.
