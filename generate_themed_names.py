#!/usr/bin/env python3
"""
Generate domain names with theme support (science, CS, ML, math, information retrieval).
Prioritizes English words relevant to the selected theme.
"""

import random
import sys
sys.path.insert(0, '.')

from generate_domain_names import (
    score_name,
    score_english_word_like,
    NamePreferences,
    is_easy_to_spell,
    CONSONANTS,
    VOWELS
)

# Theme-specific word lists
THEME_WORDS = {
    'science': [
        # Scientific concepts (removed chemistry/bio/energy terms)
        'wave', 'field', 'force', 'matter', 'mass', 'charge', 'spin', 'phase', 'state',
        'theory', 'hypothesis', 'experiment', 'observe', 'measure', 'analyze', 'test',
        'prove', 'verify', 'validate', 'discover', 'explore', 'investigate', 'study',
        'research', 'system',
        # Scientific properties
        'pure', 'precise', 'exact', 'accurate', 'rigorous', 'systematic', 'empirical',
        # Scientists (removed newton, faraday, curie)
        'darwin', 'einstein', 'tesla', 'planck', 'bohr', 'maxwell',
        'edison', 'bell', 'watt', 'euler', 'gauss', 'pascal', 'turing',
    ],
    
    'computer_science': [
        # CS concepts
        'algorithm', 'data', 'structure', 'tree', 'graph', 'node', 'edge', 'path',
        'queue', 'stack', 'heap', 'hash', 'map', 'set', 'list', 'array', 'vector',
        'matrix', 'tensor', 'bit', 'byte', 'word', 'cache', 'memory', 'register',
        'process', 'thread', 'task', 'job', 'queue', 'pool', 'buffer', 'stream',
        'parse', 'compile', 'execute', 'run', 'load', 'save', 'store', 'fetch',
        'read', 'write', 'query', 'search', 'index', 'rank', 'sort', 'filter',
        'match', 'link', 'merge', 'join', 'split', 'slice', 'extract', 'transform',
        # CS properties
        'fast', 'quick', 'efficient', 'optimal', 'scalable', 'parallel', 'concurrent',
        'async', 'sync', 'atomic', 'consistent', 'reliable', 'robust', 'secure',
        # Data science/ML training terms (CS overlap)
        'dataset', 'frame', 'series', 'pipeline', 'workflow', 'experiment', 'track',
        'version', 'reproduce', 'baseline', 'benchmark', 'evaluate', 'compare',
    ],
    
    'machine_learning': [
        # ML core concepts
        'model', 'train', 'learn', 'predict', 'infer', 'classify', 'cluster', 'regress',
        'embed', 'encode', 'decode', 'transform', 'normalize', 'standardize', 'scale',
        'feature', 'label', 'sample', 'batch', 'epoch', 'loss', 'error', 'metric',
        'accuracy', 'precision', 'recall', 'f1', 'score', 'rank', 'vector', 'tensor',
        'matrix', 'gradient', 'optimize', 'minimize', 'maximize', 'converge', 'diverge',
        'neural', 'network', 'layer', 'node', 'weight', 'bias', 'activation', 'output',
        'input', 'hidden', 'deep', 'shallow', 'wide', 'narrow', 'dense', 'sparse',
        # ML algorithms
        'svm', 'knn', 'kmeans', 'pca', 'rnn', 'cnn', 'lstm', 'transformer', 'bert',
        # ML properties
        'intelligent', 'adaptive', 'learned', 'trained', 'optimized', 'tuned',
        # Training ML terms
        'training', 'validate', 'test', 'split', 'fold', 'cross', 'validation',
        'overfit', 'underfit', 'regularize', 'dropout', 'early', 'stop',
        'backprop', 'forward', 'propagate', 'gradient', 'descent', 'adam', 'sgd',
        'momentum', 'learning', 'rate', 'decay', 'schedule', 'warmup',
        'pretrain', 'finetune', 'transfer', 'domain', 'adapt', 'fewshot',
        'zero', 'shot', 'prompt', 'incontext', 'instruction', 'tune',
        # Data science terms
        'dataset', 'data', 'frame', 'series', 'column', 'row', 'feature', 'target',
        'explore', 'exploratory', 'analysis', 'eda', 'visualize', 'plot', 'chart',
        'correlate', 'correlation', 'covariance', 'variance', 'std', 'dev',
        'outlier', 'anomaly', 'detect', 'clean', 'preprocess', 'impute', 'handle',
        'missing', 'encode', 'categorical', 'numerical', 'discrete', 'continuous',
        'engineer', 'selection', 'extract', 'reduce', 'dimension', 'project',
        'pipeline', 'workflow', 'experiment', 'track', 'version', 'reproduce',
        'baseline', 'benchmark', 'evaluate', 'assess', 'compare', 'ablate',
        'hyperparam', 'tune', 'grid', 'search', 'random', 'bayesian', 'opt',
        'ensemble', 'bag', 'boost', 'stack', 'blend', 'vote', 'average',
    ],
    
    'math': [
        # Math concepts
        'number', 'digit', 'integer', 'real', 'rational', 'irrational', 'complex',
        'prime', 'factor', 'multiple', 'divisor', 'quotient', 'remainder', 'modulo',
        'sum', 'product', 'difference', 'ratio', 'proportion', 'percent', 'fraction',
        'decimal', 'binary', 'hex', 'octal', 'base', 'exponent', 'power', 'root',
        'square', 'cube', 'log', 'ln', 'sin', 'cos', 'tan', 'angle', 'degree',
        'radian', 'pi', 'euler', 'infinity', 'limit', 'derivative', 'integral',
        'function', 'variable', 'constant', 'coefficient', 'term', 'expression',
        'equation', 'inequality', 'solve', 'compute', 'calculate', 'evaluate',
        'vector', 'matrix', 'tensor', 'scalar', 'dot', 'cross', 'norm', 'magnitude',
        'distance', 'metric', 'measure', 'space', 'dimension', 'point', 'line',
        'plane', 'curve', 'surface', 'volume', 'area', 'perimeter', 'circumference',
        # Math properties
        'exact', 'precise', 'accurate', 'rigorous', 'proof', 'theorem', 'lemma',
        'corollary', 'axiom', 'postulate', 'conjecture', 'hypothesis',
        # Mathematicians
        'euler', 'gauss', 'newton', 'leibniz', 'pascal', 'fourier', 'laplace',
        'riemann', 'hilbert', 'turing', 'godel', 'einstein',
    ],
    
    'information_retrieval': [
        # IR core concepts
        'search', 'query', 'index', 'rank', 'score', 'match', 'retrieve', 'fetch',
        'find', 'seek', 'locate', 'discover', 'extract', 'parse', 'tokenize',
        'stem', 'lemmatize', 'normalize', 'filter', 'sort', 'order', 'arrange',
        'organize', 'categorize', 'classify', 'cluster', 'group', 'segment',
        'document', 'text', 'term', 'word', 'phrase', 'sentence', 'paragraph',
        'corpus', 'collection', 'dataset', 'repository', 'archive', 'library',
        'catalog', 'directory', 'registry', 'database', 'store', 'cache',
        # IR metrics
        'precision', 'recall', 'f1', 'map', 'ndcg', 'mrr', 'accuracy', 'relevance',
        # IR techniques
        'tfidf', 'bm25', 'cosine', 'jaccard', 'euclidean', 'manhattan', 'hamming',
        'levenshtein', 'edit', 'distance', 'similarity', 'dissimilarity',
        'vector', 'embedding', 'semantic', 'syntactic', 'lexical',
        # IR properties
        'relevant', 'precise', 'accurate', 'fast', 'efficient', 'scalable',
        'comprehensive', 'complete', 'exhaustive', 'thorough',
        # Additional IR terms
        'lookup', 'scan', 'browse', 'navigate', 'traverse', 'iterate', 'enumerate',
        'aggregate', 'merge', 'join', 'union', 'intersect', 'diff', 'subtract',
        'transform', 'map', 'reduce', 'fold', 'unfold', 'flatten', 'nest',
        'encode', 'decode', 'compress', 'decompress', 'serialize', 'deserialize',
        'hash', 'digest', 'checksum', 'fingerprint', 'signature', 'token',
        'prefix', 'suffix', 'substring', 'subsequence', 'ngram', 'bigram', 'trigram',
        'inverted', 'forward', 'backward', 'bidirectional', 'multilingual',
        'relevance', 'ranking', 'scoring', 'weighting', 'boosting', 'penalizing',
        'rerank', 'refine', 'optimize', 'tune', 'calibrate', 'adjust',
        'retrieval', 'retrieval', 'retrieval', 'retrieval', 'retrieval',
    ],
}

# Base English words (always included)
BASE_WORDS = [
    'seek', 'find', 'index', 'rank', 'score', 'match', 'link', 'fetch', 'query', 'search',
    'trace', 'track', 'scan', 'probe', 'dig', 'mine', 'map', 'parse', 'extract', 'retrieve',
    'discover', 'explore', 'navigate', 'filter', 'sort', 'merge', 'join', 'split', 'slice',
    'vector', 'matrix', 'tensor', 'graph', 'tree', 'node', 'edge', 'path', 'route',
    'core', 'base', 'hub', 'mesh', 'grid', 'net', 'web', 'flow', 'wave', 'pulse',
    'beam', 'ray', 'arc', 'peak', 'ridge', 'valley', 'point', 'line', 'plane',
    'field', 'range', 'scope', 'span', 'width', 'depth', 'height', 'scale',
    'smart', 'wise', 'quick', 'fast', 'rapid', 'swift', 'instant', 'real', 'live',
    'pure', 'true', 'clear', 'bright', 'sharp', 'deep', 'wide', 'vast', 'exact',
    'precise', 'pascal', 'turing', 'euler', 'gauss', 'darwin', 'einstein',
]

def has_awkward_vowel_ending(name: str) -> bool:
    """Check if name ends with awkward vowel-vowel patterns like eive, eing, eed, eest."""
    name_lower = name.lower()
    if len(name_lower) < 4:
        return False
    
    # Pattern 1: Ends with 'ed' where the character before is 'e' (like scoreed, rankeed)
    # This creates awkward "e + ed" pattern
    if len(name_lower) >= 3:
        if name_lower.endswith('ed'):
            # Check if character before 'ed' is 'e' (like scoreed, rankeed)
            if len(name_lower) >= 3 and name_lower[-3] == 'e':
                return True
    
    # Pattern 1b: Ends with 'est' where the character before is 'e' (like scoreest, rankeest)
    # This creates awkward "e + est" pattern
    if len(name_lower) >= 4:
        if name_lower.endswith('est'):
            # Check if character before 'est' is 'e' (like scoreest, rankeest)
            if name_lower[-4] == 'e':
                return True
    
    # Pattern 2: Ends with 'ive' or 'ing' where the character before is a vowel
    # Examples: eive, aive, oive, uive, eing, aing, oing, uing
    if len(name_lower) >= 4:
        if name_lower.endswith('ive'):
            # Check if character before 'ive' is a vowel (like eive, aive, oive, uive)
            if name_lower[-4] in VOWELS:
                return True
            # Also check if there's a vowel-vowel sequence in the last 5 chars
            last_5 = name_lower[-5:] if len(name_lower) >= 5 else name_lower
            for i in range(len(last_5) - 1):
                if last_5[i] in VOWELS and last_5[i+1] in VOWELS:
                    return True
        if name_lower.endswith('ing'):
            # Check if character before 'ing' is a vowel (like eing, aing, oing, uing)
            if name_lower[-4] in VOWELS:
                return True
            # Also check if there's a vowel-vowel sequence in the last 5 chars
            last_5 = name_lower[-5:] if len(name_lower) >= 5 else name_lower
            for i in range(len(last_5) - 1):
                if last_5[i] in VOWELS and last_5[i+1] in VOWELS:
                    return True
    
    # Pattern 3: Vowel-vowel-vowel endings (3+ consecutive vowels at end)
    if len(name_lower) >= 3:
        last_3 = name_lower[-3:]
        if all(c in VOWELS for c in last_3):
            return True
    
    # Pattern 4: Vowel-vowel-consonant-vowel at end (like eive, aive)
    # This catches cases where two vowels are followed by consonant then vowel
    if len(name_lower) >= 4:
        last_4 = name_lower[-4:]
        # Pattern: V V C V (vowel, vowel, consonant, vowel ending)
        if (last_4[0] in VOWELS and last_4[1] in VOWELS and 
            last_4[2] in CONSONANTS and last_4[3] in VOWELS):
            return True
    
    return False

def get_theme_words(theme: str) -> list:
    """Get words for a specific theme."""
    theme_lower = theme.lower()
    words = BASE_WORDS.copy()
    
    if theme_lower in THEME_WORDS:
        words.extend(THEME_WORDS[theme_lower])
    
    # Filter by length and remove awkward vowel endings (length filtering happens in generate_themed_names)
    words = [w for w in words if not has_awkward_vowel_ending(w)]
    return list(set(words))  # Remove duplicates

def score_theme_relevance(name: str, theme: str) -> float:
    """Score how relevant a name is to the selected theme."""
    score = 0.0
    name_lower = name.lower()
    theme_lower = theme.lower()
    
    if theme_lower not in THEME_WORDS:
        return 0.0
    
    theme_words = THEME_WORDS[theme_lower]
    
    # PENALIZE chemistry/bio/energy sounding names (rank lower) - STRONG PENALTY
    chemistry_bio_energy_patterns = [
        'atom', 'molecule', 'particle', 'protein', 'gene', 'cell', 'tissue', 'organ',
        'enzyme', 'catalyst', 'reaction', 'compound', 'element', 'ion', 'bond',
        'energy', 'power', 'fuel', 'battery', 'charge', 'current', 'voltage',
        'chem', 'organic', 'inorganic', 'synthetic', 'polymer', 'crystal',
    ]
    
    for pattern in chemistry_bio_energy_patterns:
        if pattern in name_lower:
            score -= 80  # Strong penalty for chemistry/bio/energy (was 40)
            break
    
    # BOOST math/CS/ML/IR sounding names (rank higher) - STRONG BOOST
    math_cs_ml_ir_patterns = [
        # Math
        'calc', 'compute', 'solve', 'vector', 'matrix', 'tensor', 'prime', 'factor',
        'metric', 'function', 'variable', 'constant', 'equation', 'formula', 'theorem',
        # CS
        'code', 'data', 'algo', 'struct', 'tree', 'graph', 'node', 'hash', 'cache',
        'stack', 'queue', 'heap', 'list', 'set', 'map', 'array', 'bit', 'byte',
        # ML
        'learn', 'train', 'model', 'neural', 'embed', 'predict', 'classify', 'cluster',
        'gradient', 'optimize', 'loss', 'error', 'feature', 'label',
        # IR
        'search', 'query', 'index', 'rank', 'retrieve', 'match', 'score', 'parse',
        'extract', 'filter', 'sort', 'token', 'term', 'document', 'corpus',
    ]
    
    for pattern in math_cs_ml_ir_patterns:
        if pattern in name_lower:
            score += 100  # Strong boost for math/CS/ML/IR (was 50)
            break
    
    # Full match with theme word (but check if it's chemistry/bio first)
    if name_lower in theme_words:
        # Check if it's a chemistry/bio word - if so, reduce the boost
        is_chemistry_bio = any(pattern in name_lower for pattern in chemistry_bio_energy_patterns)
        if is_chemistry_bio:
            score += 20  # Reduced boost for chemistry/bio words
        else:
            score += 100  # Full boost for other theme words
    
    # Contains theme word
    for word in theme_words:
        if len(word) >= 4 and word in name_lower:
            score += 50
            break  # Only count one major match
    
    # Check for theme-specific patterns
    if theme_lower == 'machine_learning':
        ml_patterns = ['learn', 'train', 'model', 'neural', 'embed', 'vector', 'tensor']
        for pattern in ml_patterns:
            if pattern in name_lower:
                score += 30
    
    elif theme_lower == 'information_retrieval':
        ir_patterns = ['search', 'query', 'index', 'rank', 'retrieve', 'match', 'score']
        for pattern in ir_patterns:
            if pattern in name_lower:
                score += 30
    
    elif theme_lower == 'math':
        math_patterns = ['calc', 'compute', 'solve', 'vector', 'matrix', 'tensor', 'prime']
        for pattern in math_patterns:
            if pattern in name_lower:
                score += 30
    
    elif theme_lower == 'computer_science':
        cs_patterns = ['code', 'data', 'algo', 'struct', 'tree', 'graph', 'node', 'hash']
        for pattern in cs_patterns:
            if pattern in name_lower:
                score += 30
    
    elif theme_lower == 'science':
        # For science theme, prioritize math/CS/ML/IR over chemistry/bio
        math_cs_patterns = ['theory', 'compute', 'solve', 'vector', 'matrix', 'tensor', 
                           'code', 'data', 'search', 'query', 'index', 'rank']
        for pattern in math_cs_patterns:
            if pattern in name_lower:
                score += 40  # Higher boost for math/CS in science theme
        
        # Lower boost for general science patterns
        science_patterns = ['quantum', 'experiment', 'lab']
        for pattern in science_patterns:
            if pattern in name_lower:
                score += 20  # Lower boost
    
    return max(0, score)  # Don't return negative scores

def create_word_variation(word: str) -> str:
    """Create natural variations of an English word."""
    if len(word) >= 4:
        pos = random.randint(0, len(word) - 1)
        if word[pos] in CONSONANTS:
            similar = [c for c in 'bcdfghjklmnpqrstvwxyz' if c != word[pos]]
            new_char = random.choice(similar)
            variant = word[:pos] + new_char + word[pos+1:]
            return variant
        elif word[pos] in VOWELS:
            other_vowels = [v for v in VOWELS if v != word[pos]]
            if other_vowels:
                variant = word[:pos] + random.choice(other_vowels) + word[pos+1:]
                return variant
    return word

def generate_themed_names(count: int = 500, theme: str = 'information_retrieval', min_length: int = 4, max_length: int = 8) -> list:
    """Generate names prioritizing words relevant to the selected theme."""
    names = set()
    
    print(f"Generating {count} names with theme: {theme}...")
    
    # Get theme-specific words
    theme_words = get_theme_words(theme)
    print(f"  - Using {len(theme_words)} theme-relevant words")
    
    # Method 1: Use actual theme words directly
    print("  - Using actual theme words...")
    for word in theme_words:
        if min_length <= len(word) <= max_length:
            names.add(word.lower())
    
    # Method 2: Create variations of theme words
    print("  - Creating variations of theme words...")
    for word in theme_words:
        if len(word) <= max_length - 1:
            for _ in range(random.randint(2, 3)):
                variant = create_word_variation(word)
                if min_length <= len(variant) <= max_length and variant != word:
                    names.add(variant.lower())
    
    # Method 3: Combine short theme words
    print("  - Combining theme words...")
    short_theme_words = [w for w in theme_words if 3 <= len(w) <= 5]
    for _ in range(count // 4):
        if len(short_theme_words) >= 2:
            word1 = random.choice(short_theme_words)
            word2 = random.choice(short_theme_words)
            combined = word1 + word2
            if min_length <= len(combined) <= max_length:
                names.add(combined.lower())
    
    # Method 4: Add common English suffixes to theme words
    print("  - Adding suffixes to theme words...")
    suffixes = ['ly', 'er', 'ed', 'ing', 'ive', 'al', 'ic', 'est']
    base_theme_words = [w for w in theme_words if 3 <= len(w) <= max_length - 2]
    for word in base_theme_words:
        for suffix in suffixes:
            suffixed = word + suffix
            if min_length <= len(suffixed) <= max_length and not has_awkward_vowel_ending(suffixed):
                names.add(suffixed.lower())
    
    # Convert to list and limit
    name_list = list(names)
    return name_list[:count]

def main():
    """Generate and score themed names."""
    print("=" * 80)
    print("THEMED DOMAIN NAME GENERATOR")
    print("=" * 80)
    
    # Get theme from user
    print("\nSTEP 1: Select Theme")
    print("-" * 80)
    print("Available themes:")
    print("  1. science")
    print("  2. computer_science")
    print("  3. machine_learning")
    print("  4. math")
    print("  5. information_retrieval")
    
    theme_choice = input("\nSelect theme (1-5, or enter theme name): ").strip()
    
    theme_map = {
        '1': 'science',
        '2': 'computer_science',
        '3': 'machine_learning',
        '4': 'math',
        '5': 'information_retrieval',
    }
    
    theme = theme_map.get(theme_choice, theme_choice.lower())
    
    if theme not in THEME_WORDS and theme not in ['science', 'computer_science', 'machine_learning', 'math', 'information_retrieval']:
        print(f"Unknown theme: {theme}. Using 'information_retrieval' as default.")
        theme = 'information_retrieval'
    
    print(f"\n✓ Selected theme: {theme}")
    
    # Get number of names to generate
    print("\nSTEP 2: Number of Names to Generate")
    print("-" * 80)
    print("How many names should we generate?")
    print("  (More names = more variety, but takes longer to process)")
    print("  Recommended: 500-2000")
    
    while True:
        try:
            num_names_input = input("\nEnter number of names to generate (default: 1000): ").strip()
            if not num_names_input:
                num_names = 1000
            else:
                num_names = int(num_names_input)
                if num_names < 10:
                    print("  ⚠️  Please enter at least 10 names")
                    continue
                if num_names > 10000:
                    print("  ⚠️  That's a lot! Consider a smaller number (max 10000)")
                    continue
            break
        except ValueError:
            print("  ⚠️  Please enter a valid number")
    
    print(f"\n✓ Will generate up to {num_names} names")
    
    # Get name length constraints
    print("\nSTEP 2b: Name Length Constraints")
    print("-" * 80)
    print("What length should the names be?")
    print("  Recommended: 4-8 characters (shorter is better for domains)")
    
    while True:
        try:
            min_length_input = input("\nEnter minimum length (default: 4): ").strip()
            if not min_length_input:
                min_length = 4
            else:
                min_length = int(min_length_input)
                if min_length < 2:
                    print("  ⚠️  Minimum length must be at least 2")
                    continue
                if min_length > 15:
                    print("  ⚠️  Minimum length should be 15 or less")
                    continue
            break
        except ValueError:
            print("  ⚠️  Please enter a valid number")
    
    while True:
        try:
            max_length_input = input("Enter maximum length (default: 8): ").strip()
            if not max_length_input:
                max_length = 8
            else:
                max_length = int(max_length_input)
                if max_length < min_length:
                    print(f"  ⚠️  Maximum length must be at least {min_length}")
                    continue
                if max_length > 20:
                    print("  ⚠️  Maximum length should be 20 or less")
                    continue
            break
        except ValueError:
            print("  ⚠️  Please enter a valid number")
    
    print(f"\n✓ Name length: {min_length}-{max_length} characters")
    
    # Generate names
    names = generate_themed_names(num_names, theme, min_length, max_length)
    print(f"\n✓ Generated {len(names)} unique names")
    
    # Score them
    print("Scoring names (theme relevance + English word score)...")
    prefs = NamePreferences()
    prefs.target_audience = 'technical'
    prefs.brand_personality = 'balanced'
    prefs.name_style = 'mixed'
    prefs.opinionated = True
    prefs.include_tech_concepts = True
    prefs.use_funded_style = True
    prefs.min_length = 4
    prefs.max_length = 8
    
    scored_names = []
    for name in names:
        # Filter out awkward vowel endings
        if has_awkward_vowel_ending(name):
            continue
        
        if is_easy_to_spell(name, prefs):
            score = score_name(name, prefs)
            english_score = score_english_word_like(name)
            theme_score = score_theme_relevance(name, theme)
            
            # Combine scores (theme relevance is important)
            combined_score = score + (theme_score * 0.3)  # Weight theme relevance
            
            scored_names.append((name, combined_score, english_score, theme_score))
    
    # Sort by combined score (theme + English + total)
    scored_names.sort(key=lambda x: (-x[3], -x[1], -x[2]))  # Theme first, then total, then English
    
    # Find max values for normalization
    max_theme = max(ts for _, _, _, ts in scored_names) if scored_names else 280
    max_english = max(es for _, _, es, _ in scored_names) if scored_names else 175
    max_base = max(score_name(n, prefs) for n, _, _, _ in scored_names) if scored_names else 200
    max_total = max(ts for _, ts, _, _ in scored_names) if scored_names else 250
    
    # Get max values for breakdown dimensions (calculate from actual scores)
    from generate_domain_names import (
        score_investor_appeal,
        score_engineer_appeal,
        score_executive_appeal,
        score_technical_depth,
        score_broader_appeal
    )
    
    # Calculate actual max values from the dataset (all scores are now capped at 100)
    max_investor = 100
    max_engineer = 100
    max_executive = 100
    max_technical = 100
    max_broader = 100
    
    # Save to file with normalized scores (0-100, integers)
    output_file = f'themed_names_{theme}.txt'
    with open(output_file, 'w') as f:
        f.write(f"Themed Domain Name Suggestions: {theme}\n")
        f.write("Prioritizing theme-relevant English words\n")
        f.write("=" * 80 + "\n\n")
        f.write("SCORE DEFINITIONS:\n")
        f.write("-" * 80 + "\n")
        f.write("Theme:    How relevant the name is to the selected theme (0-100)\n")
        f.write("English:  How English-word-like the name is (100 = perfect English word)\n")
        f.write("Base:     Overall name quality score combining all dimensions (Investor + Engineer + \n")
        f.write("          Executive + Technical + Broader appeal), WITHOUT theme boost\n")
        f.write("Total:    Final ranking score = Base + (Theme * 0.3). This is what determines\n")
        f.write("          the final order (names sorted by Theme first, then Total)\n")
        f.write("\n")
        f.write("Breakdown: Individual dimension scores that make up the Base score:\n")
        f.write("  Inv:    Investor appeal (professional, credible, scalable, memorable)\n")
        f.write("  Eng:    Engineer appeal (ML/search terms, technical depth signals)\n")
        f.write("  Exec:   Executive appeal (accessible, professional, not too technical)\n")
        f.write("  Tech:   Technical depth (sophistication, algorithm relevance)\n")
        f.write("  Broad:  Broader appeal (works for both technical and non-technical audiences)\n")
        f.write("\n")
        f.write("=" * 80 + "\n\n")
        f.write(f"Total names: {len(scored_names)}\n\n")
        f.write("Names sorted by theme relevance, then total score\n")
        f.write("Scores normalized to 0-100 (integers): Theme | English | Base | Total\n")
        f.write("Breakdown: Inv | Eng | Exec | Tech | Broad\n\n")
        
        for i, (name, total_score, english_score, theme_score) in enumerate(scored_names, 1):
            # Get base score (without theme boost)
            base_score = score_name(name, prefs)
            
            # Get individual dimension scores
            investor = score_investor_appeal(name)
            engineer = score_engineer_appeal(name)
            executive = score_executive_appeal(name)
            technical = score_technical_depth(name)
            broader = score_broader_appeal(name)
            
            # Normalize to 0-100 and convert to integers
            theme_norm = int((theme_score / max_theme) * 100) if max_theme > 0 else 0
            english_norm = int((english_score / max_english) * 100) if max_english > 0 else 0
            base_norm = int((base_score / max_base) * 100) if max_base > 0 else 0
            total_norm = int((total_score / max_total) * 100) if max_total > 0 else 0
            
            investor_norm = int((investor / max_investor) * 100) if max_investor > 0 else 0
            engineer_norm = int((engineer / max_engineer) * 100) if max_engineer > 0 else 0
            executive_norm = int((executive / max_executive) * 100) if max_executive > 0 else 0
            technical_norm = int((technical / max_technical) * 100) if max_technical > 0 else 0
            broader_norm = int((broader / max_broader) * 100) if max_broader > 0 else 0
            
            theme_star = "⭐" if theme_score >= 50 else " "
            f.write(f"{i:3d}. {theme_star} {name}.ai\n")
            f.write(f"     Scores: Theme:{theme_norm:3d} | English:{english_norm:3d} | ")
            f.write(f"Base:{base_norm:3d} | Total:{total_norm:3d}\n")
            f.write(f"     Breakdown: Inv:{investor_norm:3d} Eng:{engineer_norm:3d} Exec:{executive_norm:3d} ")
            f.write(f"Tech:{technical_norm:3d} Broad:{broader_norm:3d}\n\n")
    
    print(f"\n✓ Saved {len(scored_names)} names to {output_file}")
    print(f"  📄 Output file: {output_file}")
    print("\nTop 30 names (prioritizing theme relevance):")
    for i, (name, total_score, english_score, theme_score) in enumerate(scored_names[:30], 1):
        theme_star = "⭐" if theme_score >= 50 else " "
        print(f"  {i:2d}. {theme_star} {name}.ai (Total: {total_score:.1f}, Theme: {theme_score:.1f})")
    
    # Optional: Check domain availability
    print("\n" + "=" * 80)
    print("STEP 3: Domain Availability Check (Optional)")
    print("-" * 80)
    print("Would you like to check domain availability using whois?")
    print("  Note: This can take a while (~1 second per domain)")
    print("  Example: Checking 100 domains takes ~2 minutes")
    
    check_availability = input("\nCheck domain availability? (yes/no, default: no): ").strip().lower()
    
    if check_availability in ['yes', 'y']:
        print("\nHow many available domains should we find before stopping?")
        print("  (We'll check names in priority order until we find this many)")
        print("  Recommended: 10-100")
        
        while True:
            try:
                num_available_input = input("\nEnter number of available domains to find (default: 50): ").strip()
                if not num_available_input:
                    num_available = 50
                else:
                    num_available = int(num_available_input)
                    if num_available < 1:
                        print("  ⚠️  Please enter at least 1")
                        continue
                    if num_available > 500:
                        print("  ⚠️  That's a lot! Consider a smaller number (max 500)")
                        continue
                break
            except ValueError:
                print("  ⚠️  Please enter a valid number")
        
        print(f"\n✓ Will check domains until we find {num_available} available ones")
        print(f"  (This may check up to {min(len(scored_names), num_available * 10)} domains)")
        print("\nStarting domain availability check...")
        print("  (This may take a while - checking ~1 domain per second)")
        
        # Import whois function
        from generate_domain_names import run_whois
        import time
        import os
        
        # Load cache of taken domains
        cache_file = 'taken_domains_cache.txt'
        taken_domains_cache = set()
        
        if os.path.exists(cache_file):
            try:
                with open(cache_file, 'r') as f:
                    taken_domains_cache = {line.strip().lower() for line in f if line.strip()}
                print(f"  📋 Loaded {len(taken_domains_cache)} taken domains from cache")
            except Exception as e:
                print(f"  ⚠️  Could not load cache: {e}")
        
        available_domains = []
        checked = 0
        skipped = 0
        newly_taken = []
        max_to_check = min(len(scored_names), num_available * 10)  # Check up to 10x the target
        
        # Create a lookup for scores by name
        name_to_scores = {}
        for name, total_score, english_score, theme_score in scored_names:
            base_score = score_name(name, prefs)
            name_to_scores[name] = {
                'total': total_score,
                'english': english_score,
                'theme': theme_score,
                'base': base_score
            }
        
        for name, total_score, english_score, theme_score in scored_names:
            if len(available_domains) >= num_available:
                break
            if checked >= max_to_check:
                print(f"\n  ⚠️  Reached maximum check limit ({max_to_check}). Found {len(available_domains)} available domains.")
                break
            
            domain = f"{name}.ai"
            domain_lower = domain.lower()
            
            # Check cache first
            if domain_lower in taken_domains_cache:
                skipped += 1
                print(f"  [{checked + skipped}/{max_to_check}] {domain}... (cached - taken)")
                continue
            
            checked += 1
            print(f"  [{checked}/{max_to_check}] Checking {domain}...", end=' ', flush=True)
            
            is_available, status = run_whois(domain)
            
            if is_available:
                # Get scores for this name
                scores = name_to_scores.get(name, {})
                available_domains.append((name, domain, status, scores))
                print(f"✓ AVAILABLE ({len(available_domains)}/{num_available})")
            elif is_available is False:
                # Add to cache
                taken_domains_cache.add(domain_lower)
                newly_taken.append(domain_lower)
                print("✗ Taken")
            else:
                print(f"? {status}")
            
            # Rate limiting
            time.sleep(1)
        
        # Save updated cache
        if newly_taken:
            try:
                with open(cache_file, 'a') as f:
                    for domain in newly_taken:
                        f.write(f"{domain}\n")
                print(f"\n  💾 Saved {len(newly_taken)} newly found taken domains to cache")
            except Exception as e:
                print(f"\n  ⚠️  Could not save cache: {e}")
        
        if skipped > 0:
            print(f"\n  ⚡ Skipped {skipped} domains (already in cache as taken)")
        
        # Save available domains with scores and definitions
        if available_domains:
            # Import definition function
            try:
                from add_definitions import get_definition
            except ImportError:
                # Simple fallback if add_definitions.py not available
                def get_definition(name: str) -> str:
                    """Simple definition lookup."""
                    name_lower = name.lower()
                    definitions = {
                        'search': 'to look for or find information',
                        'index': 'a list or catalog for reference',
                        'query': 'a question or request for information',
                        'rank': 'to arrange in order of importance',
                        'score': 'a numerical value or rating',
                        'parse': 'to analyze and break down into parts',
                        'extract': 'to pull out or obtain',
                        'vector': 'a quantity with direction and magnitude',
                        'tensor': 'a mathematical object generalizing vectors',
                        'cache': 'a temporary storage for quick access',
                        'filter': 'to remove or separate items',
                        'match': 'to correspond or be equal',
                        'token': 'a unit or symbol',
                        'corpus': 'a collection of texts',
                        'cluster': 'a group of similar items',
                    }
                    if name_lower in definitions:
                        return definitions[name_lower]
                    return ''
            
            available_file = f'available_{theme}_domains.txt'
            with open(available_file, 'w') as f:
                f.write(f"Available {theme} domains (found {len(available_domains)})\n")
                f.write("=" * 80 + "\n\n")
                f.write(f"Checked: {checked} domains\n")
                if skipped > 0:
                    f.write(f"Skipped (cached): {skipped} domains\n")
                f.write("\n")
                f.write("SCORE DEFINITIONS:\n")
                f.write("-" * 80 + "\n")
                f.write("Theme:    How relevant the name is to the selected theme (0-100)\n")
                f.write("English:  How English-word-like the name is (100 = perfect English word)\n")
                f.write("Base:     Overall name quality score (combines all dimensions)\n")
                f.write("Total:    Final ranking score = Base + (Theme * 0.3)\n")
                f.write("\nBreakdown: Inv | Eng | Exec | Tech | Broad\n")
                f.write("  Inv:    Investor appeal\n")
                f.write("  Eng:    Engineer appeal (ML/search terms)\n")
                f.write("  Exec:   Executive appeal (accessible, professional)\n")
                f.write("  Tech:   Technical depth (sophistication)\n")
                f.write("  Broad:  Broader appeal (universal accessibility)\n")
                f.write("\n" + "=" * 80 + "\n\n")
                
                for i, item in enumerate(available_domains, 1):
                    if len(item) == 4:
                        name, domain, status, scores = item
                    else:
                        # Backward compatibility
                        name, domain, status = item
                        scores = name_to_scores.get(name, {})
                    
                    # Get scores
                    total_score = scores.get('total', 0)
                    english_score = scores.get('english', 0)
                    theme_score = scores.get('theme', 0)
                    base_score = scores.get('base', 0)
                    
                    # Get breakdown scores
                    investor = score_investor_appeal(name)
                    engineer = score_engineer_appeal(name)
                    executive = score_executive_appeal(name)
                    technical = score_technical_depth(name)
                    broader = score_broader_appeal(name)
                    
                    # Normalize scores
                    max_theme = 280
                    max_english = 175
                    max_base = 200
                    max_total = 250
                    max_investor = 100
                    max_engineer = 100
                    max_executive = 100
                    max_technical = 100
                    max_broader = 100
                    
                    theme_norm = int((theme_score / max_theme) * 100) if max_theme > 0 else 0
                    english_norm = int((english_score / max_english) * 100) if max_english > 0 else 0
                    base_norm = int((base_score / max_base) * 100) if max_base > 0 else 0
                    total_norm = int((total_score / max_total) * 100) if max_total > 0 else 0
                    
                    investor_norm = int((investor / max_investor) * 100) if max_investor > 0 else 0
                    engineer_norm = int((engineer / max_engineer) * 100) if max_engineer > 0 else 0
                    executive_norm = int((executive / max_executive) * 100) if max_executive > 0 else 0
                    technical_norm = int((technical / max_technical) * 100) if max_technical > 0 else 0
                    broader_norm = int((broader / max_broader) * 100) if max_broader > 0 else 0
                    
                    # Get definition
                    definition = get_definition(name)
                    
                    # Write domain with scores
                    f.write(f"{i:3d}. {domain}\n")
                    if definition:
                        f.write(f"     Definition: {definition}\n")
                    f.write(f"     Scores: Theme:{theme_norm:3d} | English:{english_norm:3d} | ")
                    f.write(f"Base:{base_norm:3d} | Total:{total_norm:3d}\n")
                    f.write(f"     Breakdown: Inv:{investor_norm:3d} Eng:{engineer_norm:3d} Exec:{executive_norm:3d} ")
                    f.write(f"Tech:{technical_norm:3d} Broad:{broader_norm:3d}\n")
                    f.write(f"     Status: {status}\n\n")
            
            print(f"\n✓ Found {len(available_domains)} available domains!")
            print(f"  📄 Available domains file: {available_file}")
        else:
            print("\n⚠️  No available domains found in the checked names.")
    
    else:
        print("\n✓ Skipping domain availability check")
        print("  You can check domains manually or use a separate script later")
    
    # Final summary
    print("\n" + "=" * 80)
    print("FILES CREATED")
    print("=" * 80)
    print(f"📄 Generated names: {output_file}")
    if check_availability in ['yes', 'y'] and 'available_domains' in locals() and available_domains:
        print(f"📄 Available domains: {available_file}")
    print(f"\n💡 Tip: Check {output_file} for all generated names with detailed scores")

if __name__ == '__main__':
    main()
