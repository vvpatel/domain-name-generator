# Scoring System Improvement Plan

Based on detailed feedback analysis, this document outlines the systematic improvements needed to align the name generator with what actually makes great company names.

## Executive Summary

**Current Problem**: The system generates too many names (1000s) but most are weak due to:
1. Suffix inflation (rankic, parseer, queryive)
2. Over-valued theme relevance (too literal, locks you in)
3. Mis-scored technical depth (parse gets 0, reranked gets 35)
4. No distinction between company vs product names

**Goal**: Generate 3-5 primitive-tier names that are actually worth debating.

---

## 1. Add Morphology Penalty

### Problem
Names like `rankic`, `parseer`, `queryive`, `linktion` look algorithmic, not intentional. They signal "this was generated, not named."

### Solution
**Hard penalty** for suffixes unless the resulting word exists in English dictionary:
- `-ic` (rankic, parseic)
- `-al` (parseal, rankal)
- `-ed` (ranked, parsed) - unless it's a valid past tense
- `-er` (parseer, ranker) - unless it's a valid word like "ranker", "parser"
- `-ion` (linktion, ranktion)
- `-ize` (rankize, indexize)
- `-ify` (rankify, queryify)
- `-ive` (linkive, rankive)
- `-est` (linkest, rankest)
- `-ast` (linkast, rankast)
- `-sem` (linksem, ranksem)
- `-sion` (linksion, ranksion)

### Implementation
1. Create `has_morphology_penalty()` function
2. Check if word exists in English dictionary (use `pyenchant` or word list)
3. If suffix added and word doesn't exist → apply penalty (-50 points)
4. Whitelist valid English words (ranker, parser, matcher, etc.)

---

## 2. Add Primitive Bonus

### Problem
Primitive words (parse, impute, field, kernel) are foundational and don't need explanation. They should score much higher.

### Solution
**Large bonus** (+40-50 points) for names that are:
- Single words (not compound)
- Verbs or nouns already used in math/CS/science
- Not invented via suffixing
- Foundational operations

### Primitive Word List
**Tier 1 (Perfect Primitives - +50 points)**:
- parse, impute, field, kernel, vector, tensor, graph, metric, latent
- rank, index, query, search, match, filter, extract, retrieve
- map, reduce, fold, scan, trace, track, probe, mine

**Tier 2 (Strong Primitives - +40 points)**:
- compute, transform, encode, decode, compress, expand
- merge, join, split, slice, cut, trim, clean
- load, save, store, cache, fetch, get, set

### Implementation
1. Create `score_primitive_bonus()` function
2. Check if name is in primitive list
3. Verify it's a single word (not compound)
4. Apply bonus in final scoring

---

## 3. Fix Technical Depth Scoring

### Problem
`parse.ai` gets Tech: 0, but `reranked.ai` gets Tech: 35. This is backwards.

**Parse is:**
- Compiler theory
- NLP
- Syntax trees
- IR pipelines
- Structured understanding

**Rerank is:**
- A specific ML operation
- Less foundational
- More narrow

### Solution
Reward **foundational operations** over **model buzzwords**.

### New Technical Depth Logic
1. **Foundational CS/Math operations** (+40-50):
   - parse, compile, execute, compute, transform
   - rank, index, query, search, match
   - vector, tensor, matrix, graph, field, kernel

2. **Core algorithms/concepts** (+30-35):
   - sort, search, hash, cache, filter
   - encode, decode, compress, expand

3. **ML-specific but foundational** (+25-30):
   - embed, cluster, classify, regress
   - vector, tensor, metric

4. **Model-specific terms** (+10-15):
   - rerank, reranked (narrower, less foundational)
   - bert, gpt, transformer (too specific, ages badly)

### Implementation
1. Update `score_technical_depth()` function
2. Add foundational operations list
3. Prioritize primitives over model terms
4. Test: parse should get Tech: 40-50, not 0

---

## 4. Reduce Theme Relevance Weighting

### Problem
Theme relevance is overvalued, producing too-literal names:
- rankio, rankig, reranked, rankive
- These lock you into ranking, feel like features not platforms

### Solution
**Reduce theme weight from 0.3 to 0.1-0.15**

Great companies start abstract, then specialize. Theme relevance should be a tie-breaker, not the primary driver.

### Implementation
1. In `generate_themed_names.py`, change:
   ```python
   combined_score = score + (theme_score * 0.3) + ...
   ```
   to:
   ```python
   combined_score = score + (theme_score * 0.1) + ...
   ```

2. Prioritize: Primitive > English > Base > Theme

---

## 5. Add Company vs Product Distinction

### Problem
Everything is mixed. Company names need abstraction/longevity. Product names can be literal.

### Solution
Add a **name_type** parameter:
- `company`: Abstract, timeless, platform-thinking
- `product`: Can be literal, feature-specific

### Company Name Criteria
- Single word preferred
- Abstract/primitive preferred
- No suffixes unless valid English word
- Broader appeal

### Product Name Criteria
- Can be compound (rerank, indexer)
- Can be literal (rankio, queryive)
- Feature-specific OK

### Implementation
1. Add `name_type` to `NamePreferences`
2. Adjust scoring weights based on type
3. For company names: heavily penalize suffixes, boost primitives
4. For product names: allow more flexibility

---

## 6. Enhance English Word Detection

### Problem
Current system uses pattern matching, not actual dictionary check.

### Solution
Use actual English dictionary check:
- Option 1: `pyenchant` library
- Option 2: Large word list (100k+ words)
- Option 3: NLTK wordnet

### Implementation
1. Add dictionary check function
2. Update `score_english_word_like()` to use dictionary
3. Morphology penalty should check dictionary before applying

---

## 7. Update Scoring Weights

### Current Weights (in `generate_themed_names.py`)
```python
combined_score = score + (theme_score * 0.3) + (english_score * 0.4) + (primitive_score * 0.5)
```

### New Weights (Proposed)
```python
# Base score (already includes primitive bonus)
base_score = score_name(name, prefs)  # Includes primitive bonus

# Morphology penalty (if applicable)
morphology_penalty = -50 if has_morphology_penalty(name) else 0

# Primitive bonus (additional boost for primitives)
primitive_bonus = score_primitive_bonus(name) * 0.3  # +15-20 points for primitives

# Theme relevance (reduced weight)
theme_weight = 0.1  # Reduced from 0.3

# English word boost
english_weight = 0.3  # Keep high

combined_score = base_score + primitive_bonus + (theme_score * theme_weight) + (english_score * english_weight) + morphology_penalty
```

### Sort Order
1. Primitive score (highest first)
2. English score
3. Base score
4. Theme score (lowest priority)

---

## 8. Implementation Priority

### Phase 1: Critical Fixes (Do First)
1. ✅ Fix Technical Depth scoring (parse should get high score)
2. ✅ Add Morphology Penalty
3. ✅ Reduce Theme Relevance weight
4. ✅ Enhance Primitive Bonus

### Phase 2: Enhancements
5. Add Company vs Product distinction
6. Enhance English word detection (dictionary check)
7. Update scoring weights in main function

### Phase 3: Polish
8. Add primitive word list expansion
9. Fine-tune weights based on test results
10. Add configuration options

---

## 9. Expected Outcomes

### Before
- 1000s of names generated
- Most are weak (rankic, parseer, queryive)
- parse.ai wins despite system, not because of it

### After
- 100-200 high-quality names generated
- Most are primitive-tier (parse, impute, field, kernel)
- parse.ai wins because system rewards primitives
- Top 10 names are all worth debating

---

## 10. Testing Checklist

After implementation, verify:
- [ ] parse.ai gets Tech: 40-50 (not 0)
- [ ] parse.ai ranks #1 or #2
- [ ] rankic, parseer, queryive are filtered or heavily penalized
- [ ] impute, field, kernel rank high if in word list
- [ ] Theme relevance doesn't dominate scoring
- [ ] Primitive bonus applies correctly
- [ ] Morphology penalty catches suffix spam

---

## Notes

- Focus on **quality over quantity**: 3-5 great names > 1000 mediocre ones
- **Primitives win**: Single-word foundational operations beat compound/suffixed names
- **Abstract > Literal**: Company names should be abstract, products can be literal
- **Dictionary check**: Use real English dictionary, not pattern matching
