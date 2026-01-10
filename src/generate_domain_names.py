#!/usr/bin/env python3
"""
Interactive domain name generator for information retrieval/AI company.
Collects user context and preferences to generate tailored suggestions.
"""

import random
import subprocess
import time
import re
from itertools import product
from typing import Dict, List, Set, Tuple

# Try to import dictionary for English word checking
try:
    import enchant
    DICT_AVAILABLE = True
    english_dict = enchant.Dict("en_US")
except ImportError:
    DICT_AVAILABLE = False
    # Fallback: large English word list
    # We'll use a simple check for common words
    english_dict = None


# ============================================================================
# KEYWORD CATEGORIES
# ============================================================================

# Short, simple keywords - prioritized for easy spelling and memory
SHORT_IR_KEYWORDS = [
    'ask', 'find', 'seek', 'get', 'grab', 'pull', 'fetch',
    'scan', 'dig', 'mine', 'map', 'track', 'trace', 'probe'
]

# Medium length keywords
MEDIUM_IR_KEYWORDS = [
    'query', 'search', 'fetch', 'retrieve', 'discover', 'explore',
    'extract', 'parse', 'index', 'crawl', 'navigate'
]

# Short AI/Tech keywords
SHORT_TECH_KEYWORDS = [
    'ai', 'ml', 'deep', 'smart', 'wise', 'quick', 'fast', 'real',
    'live', 'pure', 'true', 'clear', 'sharp', 'bright'
]

# Technical/academic terms (like "Jaccard" - references technical concepts)
TECHNICAL_TERMS = [
    'jaccard', 'cosine', 'euclid', 'manhattan', 'hamming', 'levenshtein',
    'tfidf', 'bm25', 'vector', 'embed', 'semantic', 'neural', 'cortex',
    'synapse', 'nexus', 'matrix', 'tensor', 'gradient', 'entropy', 'kl',
    'f1', 'roc', 'auc', 'precision', 'recall', 'rank', 'score', 'metric'
]

# Abstract/systemic names (like "Omos" - platform-scale, systemic)
ABSTRACT_NAMES = [
    'omos', 'nexus', 'prism', 'lens', 'scope', 'vault', 'forge', 'forge',
    'core', 'base', 'hub', 'node', 'link', 'mesh', 'grid', 'flow', 'wave',
    'pulse', 'spark', 'beam', 'ray', 'arc', 'edge', 'peak', 'zenith'
]

# Literal/grounded names (like "Landy" - physical-world foundation)
LITERAL_NAMES = [
    'landy', 'ground', 'base', 'root', 'found', 'solid', 'firm', 'steady',
    'anchor', 'pillar', 'corner', 'stone', 'rock', 'clay', 'earth', 'field'
]

# Action words (very short)
ACTION_KEYWORDS = [
    'get', 'go', 'try', 'use', 'ask', 'find', 'seek', 'grab', 'pull'
]

# Simple suffixes that are easy to spell
SIMPLE_SUFFIXES = [
    'ai', 'ly', 'fy', 'er', 'io'
]

# Short prefixes
PREFIXES = [
    'get', 'go', 'try', 'use', 'ask', 'find', 'seek'
]

# Funded company style patterns (from analysis of 640+ companies)
FUNDED_PREFIXES = [
    'pro', 'con', 'ali', 'tra', 'cas', 'arc', 'ins', 'mon', 'ope',
    'lum', 'bro', 'met', 'ten', 'par', 'cha', 'lan', 'opt', 'syn',
    'dat', 'alt', 'ver', 'pre', 'gen', 'neo', 'ult', 'max', 'min',
    'sup', 'inf', 'mic', 'mac', 'uni', 'mul', 'tri', 'qua', 'hex'
]

FUNDED_SUFFIXES = [
    'ion', 'ive', 'ble', 'are', 'ght', 'tai', 'cal', 'yer', 'one',
    'ove', 'nce', 'ter', 'ium', 'ero', 'ent', 'low', 'oop', 'nai',
    'nal', 'tal', 'ral', 'mal', 'pal', 'sal', 'val', 'wal', 'yal'
]

FUNDED_BIGRAMS = [
    'ai', 'er', 'ar', 'en', 'in', 'on', 're', 'ra', 'le', 'al',
    'or', 'ro', 'ta', 'nt', 'ca', 'an', 'li', 'ti', 'te', 'lo',
    'el', 'st', 'ed', 'nd', 'ng', 'th', 'he', 'at', 'it', 'is'
]

# Common vowel patterns from funded companies
CONSONANTS = 'bcdfghjklmnpqrstvwxyz'
VOWELS = 'aeiou'


# ============================================================================
# USER PREFERENCE STRUCTURE
# ============================================================================

class NamePreferences:
    """Stores user preferences for name generation."""
    def __init__(self):
        self.target_audience = 'both'  # 'technical', 'non-technical', 'both'
        self.brand_personality = 'balanced'  # 'academic', 'warm', 'balanced'
        self.name_style = 'mixed'  # 'technical', 'abstract', 'literal', 'mixed', 'funded-style'
        self.opinionated = True  # True = narrow/specific, False = flexible/broad
        self.include_tech_concepts = True  # Include references like "Jaccard"
        self.use_funded_style = False  # Use patterns from funded AI companies
        self.max_length = 10  # Maximum name length
        self.min_length = 4  # Minimum name length


# ============================================================================
# INTERACTIVE QUESTIONNAIRE
# ============================================================================

def collect_preferences() -> NamePreferences:
    """Interactive questionnaire to collect user preferences."""
    prefs = NamePreferences()
    
    print("\n" + "=" * 70)
    print("DOMAIN NAME GENERATOR - Preference Questionnaire")
    print("=" * 70)
    print("\nThis will help generate names tailored to your needs.\n")
    
    # Target Audience
    print("1. TARGET AUDIENCE")
    print("   Who is your primary customer?")
    print("   [1] Technical (engineers, data scientists, ML teams)")
    print("   [2] Non-technical (executives, operators, general users)")
    print("   [3] Both (need to appeal to technical and non-technical)")
    choice = input("   Your choice (1-3, default: 3): ").strip() or "3"
    if choice == "1":
        prefs.target_audience = 'technical'
    elif choice == "2":
        prefs.target_audience = 'non-technical'
    else:
        prefs.target_audience = 'both'
    
    # Brand Personality
    print("\n2. BRAND PERSONALITY")
    print("   What personality should the name convey?")
    print("   [1] Academic/Precise (like 'Jaccard' - signals rigor, technical authority)")
    print("   [2] Warm/Accessible (friendly, approachable, not intimidating)")
    print("   [3] Balanced (credible but approachable)")
    choice = input("   Your choice (1-3, default: 3): ").strip() or "3"
    if choice == "1":
        prefs.brand_personality = 'academic'
    elif choice == "2":
        prefs.brand_personality = 'warm'
    else:
        prefs.brand_personality = 'balanced'
    
    # Name Style
    print("\n3. NAME STYLE")
    print("   What style of name do you prefer?")
    print("   [1] Technical terms (like 'Jaccard' - references ML/stats concepts)")
    print("   [2] Abstract/Systemic (like 'Omos' - platform-scale, systemic)")
    print("   [3] Literal/Grounded (like 'Landy' - physical-world foundation)")
    print("   [4] Funded company style (patterns from 640+ funded AI companies)")
    print("   [5] Mixed (variety of styles)")
    choice = input("   Your choice (1-5, default: 5): ").strip() or "5"
    if choice == "1":
        prefs.name_style = 'technical'
    elif choice == "2":
        prefs.name_style = 'abstract'
    elif choice == "3":
        prefs.name_style = 'literal'
    elif choice == "4":
        prefs.name_style = 'funded-style'
        prefs.use_funded_style = True
    else:
        prefs.name_style = 'mixed'
    
    # Ask about funded style patterns if not already selected
    if prefs.name_style != 'funded-style':
        print("\n3b. INCORPORATE FUNDED COMPANY PATTERNS")
        print("   Also use naming patterns from funded AI companies?")
        print("   [1] Yes (adds patterns from 640+ funded companies)")
        print("   [2] No")
        choice = input("   Your choice (1-2, default: 1): ").strip() or "1"
        prefs.use_funded_style = (choice == "1")
    
    # Opinionated vs Flexible
    print("\n4. NAME SPECIFICITY")
    print("   Do you want an 'opinionated' name (narrow, specific signal) or")
    print("   a flexible name (broad, can stretch across different products)?")
    print("   [1] Opinionated (strong, narrow signal - like 'Jaccard' for similarity)")
    print("   [2] Flexible (broad, adaptable - works for many use cases)")
    choice = input("   Your choice (1-2, default: 2): ").strip() or "2"
    prefs.opinionated = (choice == "1")
    
    # Technical Concept References
    print("\n5. TECHNICAL CONCEPT REFERENCES")
    print("   Include names that reference technical concepts (e.g., 'Jaccard', 'Cosine')?")
    print("   [1] Yes (signals technical depth, appeals to technical audience)")
    print("   [2] No (more accessible, less intimidating)")
    choice = input("   Your choice (1-2, default: 1): ").strip() or "1"
    prefs.include_tech_concepts = (choice == "1")
    
    # Length preferences
    print("\n6. NAME LENGTH")
    print("   Preferred name length?")
    print("   [1] Very short (4-6 characters)")
    print("   [2] Short (4-8 characters)")
    print("   [3] Medium (6-10 characters)")
    print("   [4] Flexible (4-12 characters)")
    choice = input("   Your choice (1-4, default: 2): ").strip() or "2"
    if choice == "1":
        prefs.min_length, prefs.max_length = 4, 6
    elif choice == "2":
        prefs.min_length, prefs.max_length = 4, 8
    elif choice == "3":
        prefs.min_length, prefs.max_length = 6, 10
    else:
        prefs.min_length, prefs.max_length = 4, 12
    
    return prefs


# ============================================================================
# NAME GENERATION FUNCTIONS
# ============================================================================

def generate_technical_names(prefs: NamePreferences) -> Set[str]:
    """Generate names using technical terms and concepts."""
    names = set()
    
    if not prefs.include_tech_concepts:
        return names
    
    # Technical terms as-is or with simple suffixes
    for term in TECHNICAL_TERMS:
        if prefs.min_length <= len(term) <= prefs.max_length:
            names.add(term)
        
        # Add simple suffixes
        for suffix in SIMPLE_SUFFIXES:
            combined = f"{term}{suffix}"
            if prefs.min_length <= len(combined) <= prefs.max_length:
                names.add(combined)
    
    # Shorten technical terms creatively
    for term in TECHNICAL_TERMS:
        if len(term) > 6:
            # Take first 4-6 chars
            shortened = term[:min(6, len(term)-1)]
            if prefs.min_length <= len(shortened) <= prefs.max_length:
                names.add(shortened)
    
    return names


def generate_abstract_names(prefs: NamePreferences) -> Set[str]:
    """Generate abstract/systemic names."""
    names = set()
    
    # Abstract names as-is
    for name in ABSTRACT_NAMES:
        if prefs.min_length <= len(name) <= prefs.max_length:
            names.add(name)
    
    # Abstract + simple suffix
    for abstract in ABSTRACT_NAMES:
        for suffix in SIMPLE_SUFFIXES:
            combined = f"{abstract}{suffix}"
            if prefs.min_length <= len(combined) <= prefs.max_length:
                names.add(combined)
    
    # Short prefix + abstract
    for prefix in PREFIXES:
        for abstract in ABSTRACT_NAMES:
            combined = f"{prefix}{abstract}"
            if prefs.min_length <= len(combined) <= prefs.max_length:
                names.add(combined)
    
    return names


def generate_literal_names(prefs: NamePreferences) -> Set[str]:
    """Generate literal/grounded names."""
    names = set()
    
    # Literal names as-is
    for name in LITERAL_NAMES:
        if prefs.min_length <= len(name) <= prefs.max_length:
            names.add(name)
    
    # Literal + simple suffix
    for literal in LITERAL_NAMES:
        for suffix in SIMPLE_SUFFIXES:
            combined = f"{literal}{suffix}"
            if prefs.min_length <= len(combined) <= prefs.max_length:
                names.add(combined)
    
    return names


def generate_short_combinations(prefs: NamePreferences) -> Set[str]:
    """Generate short, simple combinations."""
    names = set()
    
    # Short keyword + simple suffix
    for keyword in SHORT_IR_KEYWORDS + SHORT_TECH_KEYWORDS:
        for suffix in SIMPLE_SUFFIXES:
            if keyword != suffix:
                combined = f"{keyword}{suffix}"
                if prefs.min_length <= len(combined) <= prefs.max_length:
                    names.add(combined)
    
    # Prefix + short keyword
    for prefix in PREFIXES:
        for keyword in SHORT_IR_KEYWORDS + SHORT_TECH_KEYWORDS:
            combined = f"{prefix}{keyword}"
            if prefs.min_length <= len(combined) <= prefs.max_length:
                names.add(combined)
    
    # Two short words - expanded
    all_short = SHORT_IR_KEYWORDS + SHORT_TECH_KEYWORDS + MEDIUM_IR_KEYWORDS[:5]
    for word1 in all_short:
        for word2 in all_short:
            if word1 != word2:
                combined = f"{word1}{word2}"
                if prefs.min_length <= len(combined) <= prefs.max_length:
                    names.add(combined)
                combined = f"{word2}{word1}"
                if prefs.min_length <= len(combined) <= prefs.max_length:
                    names.add(combined)
    
    # Three word combinations
    for word1 in SHORT_IR_KEYWORDS[:10]:
        for word2 in SHORT_TECH_KEYWORDS[:10]:
            for word3 in SIMPLE_SUFFIXES:
                combined = f"{word1}{word2}{word3}"
                if prefs.min_length <= len(combined) <= prefs.max_length:
                    names.add(combined)
    
    return names


def generate_medium_combinations(prefs: NamePreferences) -> Set[str]:
    """Generate medium-length combinations."""
    names = set()
    
    # Medium keyword + simple suffix
    for keyword in MEDIUM_IR_KEYWORDS:
        for suffix in SIMPLE_SUFFIXES:
            combined = f"{keyword}{suffix}"
            if prefs.min_length <= len(combined) <= prefs.max_length:
                names.add(combined)
    
    # Short prefix + medium keyword
    for prefix in PREFIXES:
        for keyword in MEDIUM_IR_KEYWORDS:
            combined = f"{prefix}{keyword}"
            if prefs.min_length <= len(combined) <= prefs.max_length:
                names.add(combined)
    
    # Short + medium combinations
    for short_word in SHORT_IR_KEYWORDS + SHORT_TECH_KEYWORDS:
        for medium_word in MEDIUM_IR_KEYWORDS:
            combined = f"{short_word}{medium_word}"
            if prefs.min_length <= len(combined) <= prefs.max_length:
                names.add(combined)
            combined = f"{medium_word}{short_word}"
            if prefs.min_length <= len(combined) <= prefs.max_length:
                names.add(combined)
    
    return names


def generate_funded_style_names(prefs: NamePreferences) -> Set[str]:
    """Generate names using patterns from funded AI companies."""
    names = set()
    
    # Use funded prefixes and suffixes
    for prefix in FUNDED_PREFIXES:
        for suffix in FUNDED_SUFFIXES:
            combined = prefix + suffix
            if prefs.min_length <= len(combined) <= prefs.max_length:
                names.add(combined)
    
    # Prefix + bigram + suffix (expanded)
    for prefix in FUNDED_PREFIXES:  # All prefixes
        for bigram in FUNDED_BIGRAMS:  # All bigrams
            for suffix in FUNDED_SUFFIXES:  # All suffixes
                combined = prefix + bigram + suffix
                if 6 <= len(combined) <= prefs.max_length:
                    names.add(combined)
    
    # Two bigrams (common pattern) - expanded
    for bigram1 in FUNDED_BIGRAMS:
        for bigram2 in FUNDED_BIGRAMS:
            combined = bigram1 + bigram2
            if prefs.min_length <= len(combined) <= prefs.max_length:
                names.add(combined)
    
    # Three bigrams - expanded
    for bigram1 in FUNDED_BIGRAMS[:30]:
        for bigram2 in FUNDED_BIGRAMS[:30]:
            for bigram3 in FUNDED_BIGRAMS[:30]:
                combined = bigram1 + bigram2 + bigram3
                if 6 <= len(combined) <= prefs.max_length:
                    names.add(combined)
    
    # Four bigrams for longer names
    for bigram1 in FUNDED_BIGRAMS[:20]:
        for bigram2 in FUNDED_BIGRAMS[:20]:
            for bigram3 in FUNDED_BIGRAMS[:20]:
                for bigram4 in FUNDED_BIGRAMS[:20]:
                    combined = bigram1 + bigram2 + bigram3 + bigram4
                    if 8 <= len(combined) <= prefs.max_length:
                        names.add(combined)
    
    # Pattern-based generation (CVCCVC, CVCV, CVCVC are most common)
    # Expanded for 2M+ generation
    patterns = ['CVCCVC', 'CVCV', 'CVCVC', 'CVVC', 'CVCC', 'CVCVCVC', 'CVCCVCV', 
                'CVCCV', 'CVCVCV', 'CVCCVV', 'CVVCV', 'CVVCC', 'CCVCC', 'CCVCV']
    for pattern in patterns:
        for _ in range(5000):  # Increased from 100 to 5000
            name = generate_from_pattern(pattern)
            if prefs.min_length <= len(name) <= prefs.max_length:
                names.add(name)
    
    # Distinctive made-up names (like Voio, Kaaj, Luminal) - expanded
    starts = ['v', 'k', 'l', 'r', 'm', 'n', 'p', 't', 's', 'c', 'd', 'g', 'h', 'j', 'w', 'b', 'f', 'z', 'x', 'y']
    for start in starts:
        for v1 in VOWELS:
            for v2 in VOWELS:
                # VCV pattern (4-5 chars)
                name = start + v1 + v2
                if 4 <= len(name) <= 5:
                    names.add(name)
                # VCV + ending
                for end in ['o', 'io', 'ai', 'al', 'el', 'il', 'ol', 'ul', 'ly', 'fy', 'er', 'or', 'ex', 'ix', 'ox', 'ux']:
                    name = start + v1 + v2 + end
                    if 5 <= len(name) <= 7:
                        names.add(name)
    
    # 6-7 char names with CVCVC pattern - expanded
    consonants_mid = ['l', 'm', 'n', 'r', 't', 's', 'c', 'd', 'g', 'p', 'b', 'f', 'v', 'h', 'j', 'k', 'w', 'x', 'y', 'z']
    consonants_end = ['l', 'm', 'n', 'r', 't', 's', 'c', 'd', 'g', 'p', 'b', 'f', 'v', 'h', 'j', 'k']
    for c1 in starts:
        for v1 in VOWELS:
            for c2 in consonants_mid:
                for v2 in VOWELS:
                    for c3 in consonants_end:
                        name = c1 + v1 + c2 + v2 + c3
                        if 5 <= len(name) <= 6:
                            names.add(name)
                        # Add ending
                        for end in ['al', 'el', 'il', 'ol', 'ul', 'ix', 'ex', 'ly', 'fy', 'er', 'or', 'ai', 'io']:
                            full_name = name + end
                            if 7 <= len(full_name) <= 10:
                                names.add(full_name)
    
    # Additional patterns for longer names
    for c1 in starts[:15]:
        for v1 in VOWELS:
            for c2 in consonants_mid[:15]:
                for v2 in VOWELS:
                    for c3 in consonants_mid[:15]:
                        for v3 in VOWELS:
                            for c4 in consonants_end[:10]:
                                name = c1 + v1 + c2 + v2 + c3 + v3 + c4
                                if 7 <= len(name) <= 10:
                                    names.add(name)
    
    return names


def generate_from_pattern(pattern: str) -> str:
    """Generate a name from a vowel pattern (C=consonant, V=vowel)."""
    name = ''
    for char in pattern:
        if char == 'C':
            name += random.choice(CONSONANTS)
        elif char == 'V':
            name += random.choice(VOWELS)
    return name


def run_whois(domain: str, timeout: int = 7, retries: int = 1) -> Tuple[bool, str]:
    """
    Run whois command for a domain with timeout and retry logic.
    Returns (is_available, status_message)
    
    Args:
        domain: Domain name to check
        timeout: Timeout in seconds (default: 7, reduced from 10 for faster failure)
        retries: Number of retry attempts (default: 1)
    """
    for attempt in range(retries + 1):
        try:
            # Run whois command with timeout
            result = subprocess.run(
                ['whois', domain],
                capture_output=True,
                text=True,
                timeout=timeout
            )
            
            output = result.stdout.lower()
            error_output = result.stderr.lower()
            
            # Extract domain name (without TLD) for more specific matching
            domain_name_only = domain.split('.')[0].lower()
            
            # Check for common "not found" or "available" indicators
            not_found_patterns = [
                r'no match',
                r'not found',
                r'no entries found',
                r'no data found',
                r'status:\s*available',
                r'domain status:\s*available',
                r'no whois server',
                r'query status:\s*noobjectfound',
            ]
            
            # STRONG indicators that domain is registered (domain-specific, not TLD info)
            # These must appear in context of the actual domain name
            strong_registered_patterns = [
                rf'domain name:\s*{re.escape(domain_name_only)}',  # "Domain Name: disco" for disco.ai
                rf'registry domain id:.*{re.escape(domain_name_only)}',  # Registry ID for this domain
                rf'registrar:.*{re.escape(domain_name_only)}',  # Registrar info for this domain
            ]
            
            # Check for "registered" indicators (domain-specific patterns)
            # These patterns indicate a domain is registered/taken, but only if
            # they appear after or in context of the domain name
            registered_patterns = [
                r'domain status:\s*clienttransferprohibited',
                r'domain status:\s*clienthold',
                r'domain status:\s*ok',  # .ai domains
                r'registrar whois server:',  # .ai domains (appears for registered domains)
                r'registry domain id:',  # .ai domains (appears for registered domains)
                r'registry expiry date:',  # .ai domains (appears for registered domains)
                r'registrant name:',  # .ai domains (appears for registered domains)
                r'registrant organization:',  # .ai domains (appears for registered domains)
            ]
            
            # Check for STRONG registered indicators FIRST (most reliable)
            # These are domain-specific and won't match TLD information
            for pattern in strong_registered_patterns:
                if re.search(pattern, output):
                    return False, "Registered"
            
            # Check if "Domain Name: <domain>" appears (definitive registered indicator)
            # This appears for registered domains but not for available ones
            domain_name_pattern = rf'domain name:\s*{re.escape(domain_name_only)}\.'
            if re.search(domain_name_pattern, output):
                return False, "Registered"
            
            # Check for other registered indicators (but be more careful)
            # Look for patterns that appear AFTER the domain name or in domain-specific context
            # We'll check if registrar/registry info appears, which indicates registration
            if re.search(r'registrar whois server:', output) or re.search(r'registry domain id:', output):
                # These only appear for registered domains, not TLD info
                return False, "Registered"
            
            # Check for registrant info (only appears for registered domains)
            if re.search(r'registrant (name|organization):', output):
                return False, "Registered"
            
            # Check output for availability indicators (only if not registered)
            for pattern in not_found_patterns:
                if re.search(pattern, output):
                    return True, "Available (not found in whois)"
            
            # If output is very short or contains specific error messages, might be available
            if len(output.strip()) < 100:
                if 'not found' in output or 'no match' in output:
                    return True, "Possibly available (minimal whois response)"
            
            # Default: assume registered if we can't determine
            return False, "Unknown (check manually)"
            
        except subprocess.TimeoutExpired:
            # If this is not the last attempt, retry
            if attempt < retries:
                time.sleep(0.5)  # Brief delay before retry
                continue
            # Mark as timeout after all retries exhausted
            return None, f"Timeout (after {timeout}s)"
        except FileNotFoundError:
            return None, "whois command not found. Install whois: brew install whois (macOS)"
        except Exception as e:
            # If this is not the last attempt, retry
            if attempt < retries:
                time.sleep(0.5)
                continue
            return None, f"Error: {str(e)}"
    
    # Should not reach here, but just in case
    return None, "Timeout"


# ============================================================================
# FILTERING AND SCORING
# ============================================================================

def is_easy_to_spell(name: str, prefs: NamePreferences) -> bool:
    """Check if a name is easy to spell and remember."""
    name = name.lower()
    
    # Length check
    if len(name) < prefs.min_length or len(name) > prefs.max_length:
        return False
    
    # Avoid too many consecutive consonants
    max_consonants = 0
    current_consonants = 0
    for char in name:
        if char in 'bcdfghjklmnpqrstvwxyz':
            current_consonants += 1
            max_consonants = max(max_consonants, current_consonants)
        else:
            current_consonants = 0
    
    if max_consonants > 3:
        return False
    
    # Avoid too many consecutive vowels
    max_vowels = 0
    current_vowels = 0
    for char in name:
        if char in 'aeiou':
            current_vowels += 1
            max_vowels = max(max_vowels, current_vowels)
        else:
            current_vowels = 0
    
    if max_vowels > 3:
        return False
    
    # Avoid complex letter combinations
    hard_combos = ['xq', 'qx', 'zx', 'xz', 'qj', 'jq', 'zq', 'qz']
    for combo in hard_combos:
        if combo in name:
            return False
    
    # Vowel/consonant balance
    vowel_count = sum(1 for c in name if c in 'aeiou')
    consonant_count = len(name) - vowel_count
    
    if vowel_count == 0:
        return False
    
    if consonant_count > vowel_count * 2.5:
        return False
    
    return True


def score_investor_appeal(name: str) -> float:
    """
    Score name for investor appeal.
    Investors value: professional, credible, scalable, memorable, brandable.
    """
    score = 0.0
    name_lower = name.lower()
    
    # English words are highly valued by investors (memorable, brandable)
    english_score = score_english_word_like(name_lower)
    if english_score >= 100:  # Perfect English word
        score += 30  # Big boost for real English words
    elif english_score >= 80:  # Very English-like
        score += 20
    elif english_score >= 50:  # Somewhat English-like
        score += 10
    
    # Professional length (5-7 chars is ideal for brandability)
    if 5 <= len(name_lower) <= 7:
        score += 20
    elif 4 <= len(name_lower) <= 8:
        score += 10
    
    # Memorable and brandable (distinctive but not too weird)
    # Prefer names that sound like real words or have clear structure
    if any(prefix in name_lower for prefix in ['pro', 'con', 'arc', 'tra', 'mon', 'ins']):
        score += 15  # Professional-sounding prefixes
    
    # Avoid names that sound too generic or too obscure
    generic_words = ['data', 'tech', 'cloud', 'stack', 'base', 'core']
    if name_lower in generic_words:
        score -= 30
    
    # Prefer names that suggest scale/growth
    scale_words = ['nexus', 'prism', 'scope', 'vault', 'forge', 'hub', 'mesh', 'grid']
    if any(word in name_lower for word in scale_words):
        score += 15
    
    # Professional endings (suggest established companies)
    professional_endings = ['ion', 'ive', 'ble', 'are', 'nce', 'ter', 'ium']
    if any(name_lower.endswith(ending) for ending in professional_endings):
        score += 10
    
    # Easy to pronounce = easier to remember and share
    vowel_count = sum(1 for c in name_lower if c in VOWELS)
    consonant_count = len(name_lower) - vowel_count
    if 0.3 <= vowel_count / len(name_lower) <= 0.5:  # Good vowel/consonant balance
        score += 10
    
    # Avoid difficult letters (harder to spell/share)
    difficult_count = sum(1 for c in name_lower if c in 'xzq')
    if difficult_count == 0:
        score += 10
    elif difficult_count == 1:
        score += 5
    else:
        score -= 10
    
    # Prefer names starting with strong consonants (memorable)
    if name_lower[0] in 'bcdfghjklmnprstv':
        score += 5
    
    # Cap at 100
    return min(score, 100.0)


def score_engineer_appeal(name: str) -> float:
    """
    Score name for ML/search engineer appeal.
    ML engineers value: search/retrieval concepts, ranking, similarity, embeddings, vectors.
    """
    score = 0.0
    name_lower = name.lower()
    
    # Technical proper names (Pascal, Turing, Euler, Gauss) - HIGH PRIORITY
    technical_proper_names = ['pascal', 'turing', 'euler', 'gauss', 'newton', 'darwin', 'einstein']
    if name_lower in technical_proper_names:
        score += 50  # Technical proper names are highly valued by engineers
    
    # Core IR/CS terms (parse, extract, index, search) - HIGH PRIORITY
    core_ir_terms = ['parse', 'extract', 'index', 'search', 'query', 'rank', 'score']
    if name_lower in core_ir_terms:
        score += 45  # Core IR terms are essential
    elif any(term in name_lower for term in core_ir_terms):
        score += 35  # Contains core IR term
    
    # Search/retrieval specific terms (removed duplicates)
    search_terms = ['retrieve', 'vector', 'embed', 'similarity', 'match', 
                   'find', 'seek', 'fetch', 'metric', 'distance', 'cluster']
    if any(term in name_lower for term in search_terms):
        score += 30  # Boosted for search engineering
    
    # ML/AI relevant terms (especially for search)
    ml_terms = ['neural', 'semantic', 'tensor', 'matrix', 'gradient', 'entropy',
                'embedding', 'similarity', 'ranking', 'retrieval']
    if any(term in name_lower for term in ml_terms):
        score += 25  # Boosted
    
    # Technical terms signal sophistication
    if any(term in name_lower for term in TECHNICAL_TERMS):
        score += 25
    
    # Technical prefixes that signal depth
    tech_prefixes = ['neural', 'deep', 'vector', 'semantic', 'tensor', 'quantum']
    if any(name_lower.startswith(prefix) for prefix in tech_prefixes):
        score += 20  # Boosted
    
    # Abstract/systemic names (suggest platform thinking)
    if any(term in name_lower for term in ABSTRACT_NAMES):
        score += 15
    
    # Avoid overly marketing-y names
    marketing_words = ['super', 'mega', 'ultra', 'hyper', 'turbo', 'pro']
    if any(word in name_lower for word in marketing_words):
        score -= 10
    
    # Prefer names that suggest precision/rigor
    precision_words = ['exact', 'precise', 'sharp', 'clear', 'pure', 'true']
    if any(word in name_lower for word in precision_words):
        score += 12  # Boosted
    
    # Technical suffixes
    tech_suffixes = ['ix', 'ex', 'ox', 'ux', 'ai', 'io']
    if any(name_lower.endswith(suffix) for suffix in tech_suffixes):
        score += 10  # Boosted
    
    # Cap at 100
    return min(score, 100.0)


def score_executive_appeal(name: str) -> float:
    """
    Score name for executive/non-technical customer appeal.
    Executives value: professional, easy to understand, business value signals.
    """
    score = 0.0
    name_lower = name.lower()
    
    # English words are highly accessible to executives
    english_score = score_english_word_like(name_lower)
    if english_score >= 100:  # Perfect English word
        score += 35  # Big boost for real English words (most accessible)
    elif english_score >= 80:  # Very English-like
        score += 25
    elif english_score >= 50:  # Somewhat English-like
        score += 15
    
    # Easy to understand and pronounce
    # Simple, clear structure
    if len(name_lower) <= 7:
        score += 15
    
    # Common, accessible words
    accessible_words = ['ask', 'find', 'seek', 'get', 'go', 'try', 'use', 
                       'fetch', 'query', 'search', 'discover', 'explore']
    if any(word in name_lower for word in accessible_words):
        score += 20
    
    # Professional but not intimidating
    professional_words = ['core', 'base', 'hub', 'link', 'flow', 'wave', 'pulse']
    if any(word in name_lower for word in professional_words):
        score += 15
    
    # Avoid overly technical jargon
    if any(term in name_lower for term in ['jaccard', 'cosine', 'euclid', 'levenshtein', 'tfidf']):
        score -= 15  # Too technical/opaque
    
    # Business value signals
    value_words = ['smart', 'wise', 'quick', 'fast', 'real', 'live', 'clear', 'bright']
    if any(word in name_lower for word in value_words):
        score += 12
    
    # Easy to spell and remember
    if len(name_lower) <= 6:
        score += 10
    
    # Avoid difficult letter combinations
    if not any(combo in name_lower for combo in ['xq', 'qx', 'zx', 'xz', 'qj']):
        score += 8
    
    # Prefer names ending in vowels (easier to pronounce)
    if name_lower[-1] in 'aeiouy':
        score += 5
    
    # Cap at 100
    return min(score, 100.0)


def score_technical_depth(name: str) -> float:
    """
    Score name for technical depth (shows sophistication without being opaque).
    FIXED: Now rewards foundational operations (parse, compile) over model buzzwords (rerank).
    
    Parse is: compiler theory, NLP, syntax trees, IR pipelines, structured understanding.
    Rerank is: a specific ML operation, less foundational, more narrow.
    """
    score = 0.0
    name_lower = name.lower()
    
    # Tier 1: Foundational CS/Math operations (+40-50) - HIGHEST PRIORITY
    # These are core operations that appear across multiple domains
    foundational_operations = [
        'parse', 'compile', 'execute', 'compute', 'transform',  # Compiler/CS theory
        'rank', 'index', 'query', 'search', 'match',  # IR primitives
        'vector', 'tensor', 'matrix', 'graph', 'field', 'kernel',  # Math/ML primitives
        'impute', 'latent', 'metric'  # Statistical/ML primitives
    ]
    
    if name_lower in foundational_operations:
        score += 50  # Maximum score for foundational operations
    
    # Tier 2: Core algorithms/concepts (+30-35)
    core_algorithms = [
        'sort', 'hash', 'cache', 'filter', 'extract', 'retrieve',
        'encode', 'decode', 'compress', 'expand', 'merge', 'join',
        'map', 'reduce', 'fold', 'scan', 'trace', 'track'
    ]
    
    if name_lower in core_algorithms:
        score += 35  # Strong technical depth
    
    # Tier 3: ML-specific but foundational (+25-30)
    ml_foundational = [
        'embed', 'cluster', 'classify', 'regress', 'predict',
        'vector', 'tensor', 'metric', 'similarity'
    ]
    
    if name_lower in ml_foundational:
        score += 30  # ML foundational concepts
    
    # Technical proper names (Pascal, Turing, etc.) signal depth
    technical_proper_names = ['pascal', 'turing', 'euler', 'gauss', 'newton', 'darwin', 'einstein']
    if name_lower in technical_proper_names:
        score += 40  # Technical proper names signal depth
    
    # Tier 4: Model-specific terms (+10-15) - LOWER PRIORITY
    # These are narrower and age badly
    model_specific = ['rerank', 'reranked', 'bert', 'gpt', 'transformer']
    if any(term in name_lower for term in model_specific):
        score += 15  # Much lower than foundational operations
    
    # Direct technical references (algorithm/metric names) - but lower than primitives
    if any(term in name_lower for term in TECHNICAL_TERMS):
        # Only add if not already a foundational operation
        if name_lower not in foundational_operations:
            score += 25  # Algorithm/metric references show depth
    
    # Technical concepts embedded (more sophisticated than basic terms)
    advanced_tech_concepts = ['neural', 'semantic', 'tensor', 'matrix', 'gradient', 
                            'entropy', 'embedding', 'similarity', 'clustering']
    if any(concept in name_lower for concept in advanced_tech_concepts):
        # Only add if not already a foundational operation
        if name_lower not in foundational_operations:
            score += 20  # Advanced concepts show depth
    
    # Abstract/systemic suggests platform thinking
    if any(term in name_lower for term in ABSTRACT_NAMES):
        score += 15
    
    # Technical suffixes
    if any(name_lower.endswith(suffix) for suffix in ['ix', 'ex', 'ox', 'ux']):
        score += 10
    
    # But not too obscure (balance)
    obscure_terms = ['jaccard', 'levenshtein', 'manhattan', 'hamming']
    obscure_count = sum(1 for term in obscure_terms if term in name_lower)
    if obscure_count > 1:
        score -= 10  # Too niche
    
    # Cap at 100
    return min(score, 100.0)


def score_english_word_like(name: str) -> float:
    """
    Score name for being an English word or sounding like one.
    English words are more memorable and accessible.
    Returns score 0-100, where 100 = perfect English word match.
    """
    score = 0.0
    name_lower = name.lower()
    
    # Common English words (full matches) - PRIORITIZED LIST
    # Action words (like "seek", "find", "index")
    action_words = [
        'ask', 'find', 'seek', 'get', 'go', 'try', 'use', 'fetch', 'query', 'search',
        'rank', 'score', 'match', 'link', 'index', 'parse', 'extract', 'retrieve',
        'discover', 'explore', 'navigate', 'trace', 'track', 'scan', 'probe', 'dig'
    ]
    
    # Technical English words (like "index", "vector", "matrix")
    technical_english_words = [
        'index', 'vector', 'matrix', 'tensor', 'rank', 'score', 'metric', 'query',
        'search', 'match', 'link', 'node', 'edge', 'graph', 'tree', 'list', 'map',
        'set', 'hash', 'key', 'value', 'data', 'field', 'record', 'table', 'row',
        'column', 'pascal', 'turing', 'euler', 'gauss', 'newton', 'darwin'
    ]
    
    # Common descriptive words
    descriptive_words = [
        'core', 'base', 'hub', 'flow', 'wave', 'pulse', 'beam', 'ray', 'arc',
        'edge', 'peak', 'mesh', 'grid', 'smart', 'wise', 'quick', 'fast', 'real',
        'live', 'pure', 'true', 'clear', 'bright', 'sharp', 'deep', 'wide', 'vast',
        'exact', 'precise', 'rapid', 'instant', 'swift', 'fresh', 'new', 'next'
    ]
    
    all_english_words = action_words + technical_english_words + descriptive_words
    
    # Full English word match - AUTOMATIC 100 (perfect English word)
    if name_lower in action_words:
        return 100.0  # Action words are perfect English words
    elif name_lower in technical_english_words:
        return 100.0  # Technical English words are perfect English words
    elif name_lower in descriptive_words:
        return 100.0  # Descriptive words are perfect English words
    
    # If not a full match, score based on how English-like it is
    
    # Check if name contains English words
    for word in all_english_words:
        if word in name_lower and len(word) >= 3:
            if word in action_words:
                score += 25  # Action words in name
            elif word in technical_english_words:
                score += 20  # Technical words in name
            else:
                score += 15  # Other English words
    
    # Proper names with technical heritage (like Pascal)
    technical_proper_names = ['pascal', 'turing', 'euler', 'gauss', 'newton', 'darwin', 'einstein']
    if name_lower in technical_proper_names:
        score += 30  # Technical proper names get boost
    
    # Check if name sounds like an English word (common patterns)
    english_suffixes = ['ly', 'er', 'or', 'ed', 'ing', 'ion', 'ive', 'al', 'ic', 'ous']
    if any(name_lower.endswith(suffix) for suffix in english_suffixes):
        score += 15
    
    # Common English word patterns
    vowel_count = sum(1 for c in name_lower if c in VOWELS)
    consonant_count = len(name_lower) - vowel_count
    
    if 0.25 <= vowel_count / len(name_lower) <= 0.5:
        score += 10
    
    # Common English letter combinations
    english_bigrams = ['th', 'he', 'in', 'er', 'an', 're', 'ed', 'nd', 'on', 'en',
                      'at', 'ou', 'it', 'is', 'or', 'ti', 'as', 'to', 'of', 'ar']
    for bigram in english_bigrams:
        if bigram in name_lower:
            score += 5
    
    # Names that start with common English word starts
    english_starts = ['pr', 'co', 're', 'un', 'in', 'ex', 'de', 'en', 'be', 'se',
                     'ac', 'ad', 'al', 'an', 'ap', 'ar', 'as', 'at', 'au', 'av']
    if any(name_lower.startswith(start) for start in english_starts):
        score += 8
    
    # Cap at 100 and return
    return min(score, 100.0)


def score_broader_appeal(name: str) -> float:
    """
    Score name for broader appeal (works for both technical and non-technical).
    Focuses on universal accessibility and balance.
    """
    score = 0.0
    name_lower = name.lower()
    
    # English words have universal appeal
    english_score = score_english_word_like(name_lower)
    if english_score >= 100:  # Perfect English word
        score += 30  # Real English words have broad appeal
    elif english_score >= 80:  # Very English-like
        score += 20
    elif english_score >= 50:  # Somewhat English-like
        score += 10
    
    # Names that hint at capability without being opaque
    # Abstract but accessible
    accessible_abstract = ['nexus', 'prism', 'lens', 'scope', 'core', 'base', 
                          'hub', 'flow', 'wave', 'pulse', 'beam', 'ray']
    if any(word in name_lower for word in accessible_abstract):
        score += 20
    
    # Simple action words (universally understood)
    action_words = ['ask', 'find', 'seek', 'get', 'fetch', 'query', 'search']
    if any(word in name_lower for word in action_words):
        score += 18
    
    # Professional but not intimidating
    if 5 <= len(name_lower) <= 7:
        score += 15
    
    # Easy to pronounce (good vowel/consonant balance)
    vowel_count = sum(1 for c in name_lower if c in VOWELS)
    if 0.25 <= vowel_count / len(name_lower) <= 0.5:
        score += 12
    
    # Not too technical, not too generic (balance is key)
    if not any(term in name_lower for term in ['jaccard', 'cosine', 'euclid', 'levenshtein']):
        score += 10  # Not too technical
    
    if name_lower not in ['data', 'tech', 'cloud', 'stack']:
        score += 10  # Not too generic
    
    # Memorable structure
    if len(name_lower) == 6:  # Sweet spot
        score += 10
    
    # Professional endings
    if any(name_lower.endswith(ending) for ending in ['ly', 'fy', 'er', 'io', 'ai']):
        score += 8
    
    # Cap at 100
    return min(score, 100.0)


def score_primitive_bonus(name: str) -> float:
    """
    Score name for being a primitive (foundational word) used in math/CS/science.
    Based on feedback: parse, impute, field, kernel are primitives that deserve maximum bonus.
    
    Primitives are:
    - Single words (not compound)
    - Verbs or nouns already used in math/CS/science
    - Not invented via suffixing
    - Foundational operations
    
    Returns score 0-100, where 100 = perfect primitive.
    """
    name_lower = name.lower()
    
    # Must be a single word (not compound)
    if ' ' in name_lower or '-' in name_lower:
        return 0.0
    
    # Tier 1: Perfect Primitives (+50 points) - foundational CS/math/science words
    tier1_primitives = [
        # CS/IR primitives
        'parse', 'impute', 'field', 'kernel', 'vector', 'tensor', 'graph', 'metric', 'latent',
        'rank', 'index', 'query', 'search', 'match', 'filter', 'extract', 'retrieve',
        # Math primitives
        'matrix', 'scalar', 'norm', 'span', 'basis', 'eigen', 'trace', 'det',
        # Statistical primitives
        'mean', 'median', 'mode', 'variance', 'covariance', 'correlation',
        # System primitives
        'map', 'reduce', 'fold', 'scan', 'trace', 'track', 'probe', 'mine'
    ]
    
    if name_lower in tier1_primitives:
        return 100.0  # Perfect primitive - maximum score
    
    # Tier 2: Strong Primitives (+40 points) - core operations
    tier2_primitives = [
        'find', 'seek', 'fetch', 'sort', 'link', 'merge', 'join', 'split',
        'slice', 'cut', 'trim', 'clean', 'transform', 'convert', 'encode',
        'decode', 'compress', 'expand', 'scale', 'shift', 'rotate', 'flip',
        'read', 'write', 'load', 'save', 'store', 'cache', 'get', 'set',
        'put', 'take', 'send', 'receive', 'push', 'pull', 'move', 'copy',
        'discover', 'explore', 'navigate', 'traverse', 'walk', 'visit'
    ]
    
    if name_lower in tier2_primitives:
        return 85.0  # Strong primitive
    
    # Tier 3: Good Primitives (+30 points) - still foundational
    tier3_primitives = [
        'build', 'create', 'make', 'generate', 'produce', 'construct', 'assemble',
        'compile', 'execute', 'run', 'start', 'stop', 'pause', 'resume', 'continue',
        'begin', 'end', 'finish', 'complete', 'close', 'open', 'lock', 'unlock',
        'bind', 'unbind', 'attach', 'detach', 'connect', 'disconnect'
    ]
    
    if name_lower in tier3_primitives:
        return 70.0  # Good primitive
    
    return 0.0


def score_primitive_verb_appeal(name: str) -> float:
    """
    Score name for being a primitive verb (core operation) that generalizes well.
    Based on feedback: parse.ai stands out because it's a true primitive that scales.
    
    Primitive verbs are foundational operations that don't box you in:
    - parse, rank, index, query, search, find, extract, match, link, etc.
    
    Returns score 0-100, where 100 = perfect primitive verb.
    """
    score = 0.0
    name_lower = name.lower()
    
    # Tier 1: Perfect primitive verbs (like parse, rank, index, query, search)
    # These are core operations that generalize extremely well
    tier1_primitives = [
        'parse', 'rank', 'index', 'query', 'search', 'find', 'seek', 'fetch',
        'extract', 'match', 'link', 'filter', 'sort', 'map', 'reduce', 'fold',
        'scan', 'trace', 'track', 'probe', 'dig', 'mine', 'discover', 'explore',
        'navigate', 'traverse', 'walk', 'visit', 'read', 'write', 'load', 'save',
        'store', 'cache', 'retrieve', 'get', 'set', 'put', 'take', 'give',
        'send', 'receive', 'push', 'pull', 'move', 'copy', 'merge', 'join',
        'split', 'slice', 'cut', 'trim', 'clean', 'transform', 'convert', 'encode',
        'decode', 'compress', 'expand', 'scale', 'shift', 'rotate', 'flip'
    ]
    
    if name_lower in tier1_primitives:
        return 100.0  # Perfect primitive verb - highest score
    
    # Tier 2: Strong primitive-like verbs (still foundational)
    tier2_primitives = [
        'build', 'create', 'make', 'generate', 'produce', 'construct', 'assemble',
        'compile', 'execute', 'run', 'start', 'stop', 'pause', 'resume', 'continue',
        'begin', 'end', 'finish', 'complete', 'close', 'open', 'lock', 'unlock',
        'bind', 'unbind', 'attach', 'detach', 'connect', 'disconnect', 'link', 'unlink'
    ]
    
    if name_lower in tier2_primitives:
        return 85.0  # Strong primitive verb
    
    # Check if name contains a primitive verb
    all_primitives = tier1_primitives + tier2_primitives
    for primitive in all_primitives:
        if primitive in name_lower and len(primitive) >= 4:
            if primitive in tier1_primitives:
                score += 40  # Contains tier 1 primitive
            else:
                score += 25  # Contains tier 2 primitive
    
    # Penalize metric/algorithm-specific names (too narrow, academic)
    # These are Kaggle leaderboard terms, not company names
    metric_names = [
        'smape', 'mape', 'mae', 'mse', 'rmse', 'f1', 'fbeta', 'auc', 'roc', 'pr',
        'ap', 'map', 'ndcg', 'mrr', 'dcg', 'idcg', 'err', 'rbp', 'iou', 'dice',
        'bleu', 'rouge', 'meteor', 'cider', 'spice', 'bertscore', 'mover',
        'listnet', 'ranknet', 'adrank', 'lambdamart', 'xendcg', 'pcascore',
        'tfidf', 'bm25', 'cosine', 'jaccard', 'euclidean', 'manhattan', 'hamming',
        'levenshtein', 'dtw', 'kl', 'js', 'wasserstein', 'bhattacharyya'
    ]
    
    if name_lower in metric_names:
        score -= 50  # Heavy penalty for metric names
    
    # Check if name contains metric terms (also penalize)
    for metric in metric_names:
        if metric in name_lower:
            score -= 30  # Penalty for containing metric terms
    
    # Penalize letter-swapped variants (gimmicky)
    # Patterns like: sscore, rscore, scorea, xscore, qscore, etc.
    base_words = ['score', 'rank', 'index', 'query', 'search', 'parse', 'match']
    for base in base_words:
        if len(name_lower) > len(base):
            # Check for single letter prefix/suffix swaps
            if name_lower.startswith(base) and len(name_lower) == len(base) + 1:
                # e.g., "scorea", "scorex"
                if name_lower[-1] in 'abcdefghijklmnopqrstuvwxyz':
                    score -= 40  # Heavy penalty for letter-swapped variants
            elif name_lower.endswith(base) and len(name_lower) == len(base) + 1:
                # e.g., "sscore", "xscore", "qscore"
                if name_lower[0] in 'abcdefghijklmnopqrstuvwxyz':
                    score -= 40  # Heavy penalty for letter-swapped variants
    
    # Boost short dictionary words (4-6 chars) that are clean
    if 4 <= len(name_lower) <= 6:
        english_score = score_english_word_like(name_lower)
        if english_score >= 100:  # Perfect English word
            score += 30  # Boost for short, clean dictionary words
        elif english_score >= 80:
            score += 15
    
    # Cap at 100 and return
    return min(max(score, 0.0), 100.0)


def is_english_word(word: str) -> bool:
    """
    Check if a word exists in English dictionary.
    Uses pyenchant if available, otherwise falls back to word list check.
    """
    word_lower = word.lower()
    
    if DICT_AVAILABLE and english_dict:
        return english_dict.check(word_lower)
    
    # Fallback: check against known English words
    # This is a subset - for full accuracy, install pyenchant
    known_english_words = {
        # Common words
        'the', 'be', 'to', 'of', 'and', 'a', 'in', 'that', 'have', 'i',
        'it', 'for', 'not', 'on', 'with', 'he', 'as', 'you', 'do', 'at',
        # Technical words we care about
        'parse', 'rank', 'index', 'query', 'search', 'filter', 'match', 'link',
        'ranker', 'parser', 'matcher', 'indexer', 'searcher', 'linker',
        'ranking', 'querying', 'indexing', 'linking', 'filtering', 'matching',
        'extract', 'retrieve', 'fetch', 'find', 'seek', 'discover', 'explore',
        'sort', 'merge', 'join', 'split', 'slice', 'cut', 'trim', 'clean',
        'read', 'write', 'load', 'save', 'store', 'cache', 'get', 'set',
        'vector', 'tensor', 'matrix', 'graph', 'field', 'kernel', 'metric',
        'impute', 'latent', 'compute', 'transform', 'encode', 'decode'
    }
    
    return word_lower in known_english_words


def has_morphology_penalty(name: str) -> bool:
    """
    Check if name has morphology penalty (suffix spam).
    Hard penalty for suffixes unless the resulting word exists in English dictionary.
    
    Returns True if name should be penalized (has suffix spam).
    """
    name_lower = name.lower()
    
    # Problematic suffixes that look auto-generated
    problematic_suffixes = [
        'ic', 'al', 'ed', 'er', 'ly', 'ive', 'ize', 'ify',
        'ion', 'tion', 'sion', 'est', 'ast', 'sem', 'able', 'ible',
        'ment', 'ance', 'ence'
    ]
    
    # Valid English words that end in these suffixes (whitelist)
    valid_words_with_suffixes = {
        'filter', 'finder', 'seeker', 'ranker', 'scorer', 'matcher', 'linker',
        'parser', 'extractor', 'retriever', 'searcher', 'indexer', 'sorter',
        'merger', 'joiner', 'splitter', 'slicer', 'cutter', 'trimmer', 'cleaner',
        'reader', 'writer', 'loader', 'saver', 'storer', 'fetcher', 'querier',
        'scanner', 'walker', 'visitor', 'tracer', 'tracker', 'prober', 'digger',
        'miner', 'discoverer', 'explorer', 'navigator', 'traverser', 'ranking',
        'querying', 'indexing', 'loading', 'joining', 'folding', 'triming', 'linking',
        'filtering', 'matching', 'sorting', 'merging', 'splitting', 'slicing',
        'cutting', 'trimming', 'cleaning', 'reading', 'writing', 'loading',
        'saving', 'storing', 'caching', 'getting', 'setting', 'putting',
        'sending', 'receiving', 'pushing', 'pulling', 'moving', 'copying'
    }
    
    # If it's a known valid word, no penalty
    if name_lower in valid_words_with_suffixes:
        return False
    
    # Check each problematic suffix
    for suffix in problematic_suffixes:
        if name_lower.endswith(suffix) and len(name_lower) >= 5:
            # Extract root
            root = name_lower[:-len(suffix)]
            
            # Check if the full word exists in English dictionary
            if is_english_word(name_lower):
                return False  # Valid English word, no penalty
            
            # Check if root is a common tech word (likely suffix spam)
            common_tech_roots = [
                'rank', 'data', 'node', 'term', 'loss', 'scan', 'fast', 'bias', 'join',
                'stem', 'plot', 'shot', 'wide', 'test', 'fold', 'zero', 'word', 'code',
                'byte', 'bit', 'file', 'path', 'link', 'edge', 'tree', 'list', 'map',
                'set', 'hash', 'key', 'val', 'pair', 'item', 'elem', 'cell', 'slot',
                'sort', 'search', 'find', 'seek', 'walk', 'visit', 'read',
                'write', 'load', 'save', 'store', 'fetch', 'query', 'index', 'match',
                'merge', 'split', 'slice', 'cut', 'trim', 'clean', 'adam', 'bert',
                'trace', 'track', 'mine', 'scale', 'parse', 'sparse', 'rerank', 'cache',
                'filter'
            ]
            
            if root in common_tech_roots:
                return True  # Suffix spam detected
    
    return False


def score_name(name: str, prefs: NamePreferences) -> float:
    """
    Comprehensive scoring function evaluating names across multiple dimensions:
    - Investor appeal
    - Engineer appeal  
    - Executive appeal
    - Technical depth
    - Broader appeal
    """
    name_lower = name.lower()
    
    # Get scores from each dimension
    investor_score = score_investor_appeal(name_lower)
    engineer_score = score_engineer_appeal(name_lower)
    executive_score = score_executive_appeal(name_lower)
    technical_score = score_technical_depth(name_lower)
    broader_score = score_broader_appeal(name_lower)
    
    # English word boost
    english_score = score_english_word_like(name_lower)
    
    # Primitive verb boost (prioritize foundational verbs like parse, rank, index)
    primitive_score = score_primitive_verb_appeal(name_lower)
    
    # NEW: Primitive bonus (explicit bonus for CS/math/science primitives)
    primitive_bonus_score = score_primitive_bonus(name_lower)
    
    # NEW: Morphology penalty (penalize suffix spam)
    morphology_penalty = -50.0 if has_morphology_penalty(name_lower) else 0.0
    
    # Weighted combination based on preferences
    total_score = 0.0
    
    # Base scores (always important)
    # Reduced investor weight, increased English word weight (based on Pascal/Seek/Index preference)
    total_score += investor_score * 0.15  # Reduced from 0.20
    total_score += broader_score * 0.15   # Broader appeal is valuable
    total_score += english_score * 0.30    # Increased from 0.25 - English words are highly valued
    total_score += primitive_score * 0.25   # Boost primitive verbs (parse, rank, index, etc.)
    total_score += primitive_bonus_score * 0.30  # NEW: Additional boost for primitives (parse, impute, field, kernel)
    total_score += morphology_penalty  # NEW: Penalty for suffix spam
    
    # Audience-specific weighting (boosted for ML/search engineers)
    if prefs.target_audience == 'technical':
        total_score += engineer_score * 0.35  # Increased for ML engineers
        total_score += technical_score * 0.15
        total_score += executive_score * 0.05
    elif prefs.target_audience == 'non-technical':
        total_score += executive_score * 0.30
        total_score += engineer_score * 0.10
        total_score += technical_score * 0.05
    else:  # both
        total_score += engineer_score * 0.25  # Increased for ML engineers
        total_score += executive_score * 0.15
        total_score += technical_score * 0.10
    
    # Brand personality adjustments
    if prefs.brand_personality == 'academic':
        total_score += technical_score * 0.10
        total_score += engineer_score * 0.05
    elif prefs.brand_personality == 'warm':
        total_score += executive_score * 0.10
        total_score += broader_score * 0.05
    
    # Name style adjustments
    if prefs.name_style == 'technical':
        total_score += technical_score * 0.15
        total_score += engineer_score * 0.10
    elif prefs.name_style == 'abstract':
        total_score += broader_score * 0.10
        total_score += investor_score * 0.05
    elif prefs.name_style == 'funded-style':
        # Funded companies balance all dimensions
        total_score += investor_score * 0.10
        total_score += broader_score * 0.10
    
    # Funded style patterns (if enabled)
    if prefs.use_funded_style:
        if any(prefix in name_lower for prefix in FUNDED_PREFIXES[:10]):
            total_score += 8
        if any(suffix in name_lower for suffix in FUNDED_SUFFIXES[:10]):
            total_score += 8
        if len(name_lower) == 6:  # Peak length in funded companies
            total_score += 10
    
    # Opinionated vs flexible
    if prefs.opinionated:
        total_score += technical_score * 0.05
    else:
        total_score += broader_score * 0.05
    
    # Basic quality checks
    # Length preference - BOOST SHORT ENGLISH WORDS (4-6 chars like Pascal, Seek, Index)
    if 4 <= len(name_lower) <= 6:
        total_score += 20  # Boosted for short names
        # Extra boost if it's an English word
        if score_english_word_like(name_lower) >= 50:
            total_score += 15  # Short English words are highly valued
    elif len(name_lower) == 7:
        total_score += 10
    elif 8 <= len(name_lower) <= 10:
        total_score += 5
    else:
        total_score -= 5  # Penalize very long or very short names
    
    # Easy to spell
    if name_lower[0] in 'abcdefghijklmnopqrst':
        total_score += 3
    
    # Penalize difficult letters
    difficult_count = sum(1 for c in name_lower if c in 'xzq')
    if difficult_count > 1:
        total_score -= 10
    
    return total_score


def get_score_breakdown(name: str, prefs: NamePreferences) -> Dict[str, float]:
    """Get detailed score breakdown for a name."""
    name_lower = name.lower()
    return {
        'investor': score_investor_appeal(name_lower),
        'engineer': score_engineer_appeal(name_lower),
        'executive': score_executive_appeal(name_lower),
        'technical': score_technical_depth(name_lower),
        'broader': score_broader_appeal(name_lower),
        'total': score_name(name_lower, prefs)
    }


def filter_and_score_names(names: Set[str], prefs: NamePreferences) -> List[tuple]:
    """Filter and score names based on preferences. Returns list of (name, score) tuples."""
    filtered = []
    
    for name in names:
        name_lower = name.lower()
        
        if not is_easy_to_spell(name_lower, prefs):
            continue
        
        score = score_name(name_lower, prefs)
        filtered.append((name_lower, score))
    
    # Sort by score (highest first), then by length (shortest first)
    filtered.sort(key=lambda x: (-x[1], len(x[0])))
    
    # Deduplicate
    seen = set()
    result = []
    for name, score in filtered:
        if name not in seen:
            seen.add(name)
            result.append((name, score))
    
    return result


# ============================================================================
# MAIN FUNCTION
# ============================================================================

def main():
    """Main interactive function."""
    # Collect preferences
    prefs = collect_preferences()
    
    print("\n" + "=" * 70)
    print("Generating names based on your preferences...")
    print("=" * 70)
    
    all_names = set()
    
    # Generate based on style preferences
    if prefs.name_style == 'funded-style':
        # Focus on funded-style patterns
        all_names.update(generate_funded_style_names(prefs))
    else:
        # Traditional style generation
        if prefs.name_style in ['technical', 'mixed']:
            all_names.update(generate_technical_names(prefs))
        
        if prefs.name_style in ['abstract', 'mixed']:
            all_names.update(generate_abstract_names(prefs))
        
        if prefs.name_style in ['literal', 'mixed']:
            all_names.update(generate_literal_names(prefs))
        
        # Always include short combinations (they're versatile)
        all_names.update(generate_short_combinations(prefs))
        all_names.update(generate_medium_combinations(prefs))
        
        # Add funded-style names if enabled
        if prefs.use_funded_style:
            all_names.update(generate_funded_style_names(prefs))
    
    # Filter and score
    filtered_names = filter_and_score_names(all_names, prefs)
    
    # Ask if user wants to check availability (takes ~16 minutes for 1000 domains)
    print(f"\n{'='*70}")
    print("AVAILABILITY CHECK")
    print(f"{'='*70}")
    print("Would you like to check the top 1000 names for availability?")
    print("This will take approximately 16 minutes (1 second delay between checks).")
    check_availability = input("Check availability? (yes/no, default: yes): ").strip().lower()
    
    available_domains = []
    
    if check_availability in ['yes', 'y', '']:
        # Check top 1000 with whois
        print(f"\nChecking top 1000 names for availability...")
        print("This may take a while (rate limiting to avoid being blocked)...")
        
        top_1000 = filtered_names[:1000]
        
        for i, (name, score) in enumerate(top_1000, 1):
            domain = f"{name}.ai"
            print(f"[{i}/1000] Checking {domain}...", end=' ', flush=True)
            
            is_available, status = run_whois(domain)
            
            if is_available is True:
                available_domains.append((name, score, status))
                print(f"✓ AVAILABLE")
            elif is_available is False:
                print(f"✗ TAKEN")
            else:
                print(f"? {status}")
            
            # Rate limiting
            if i < len(top_1000):
                time.sleep(1.0)  # 1 second delay between checks
        
        print(f"\n✓ Found {len(available_domains)} potentially available domains out of {len(top_1000)} checked")
    else:
        print("Skipping availability check. You can run check_domain_availability.py separately.")
    
    # Save to file
    output_file = 'domain_name_suggestions.txt'
    with open(output_file, 'w') as f:
        f.write("Generated .ai Domain Name Suggestions\n")
        f.write("=" * 70 + "\n\n")
        f.write("PREFERENCES:\n")
        f.write(f"  Target Audience: {prefs.target_audience}\n")
        f.write(f"  Brand Personality: {prefs.brand_personality}\n")
        f.write(f"  Name Style: {prefs.name_style}\n")
        f.write(f"  Opinionated: {prefs.opinionated}\n")
        f.write(f"  Include Tech Concepts: {prefs.include_tech_concepts}\n")
        f.write(f"  Use Funded Style Patterns: {prefs.use_funded_style}\n")
        f.write(f"  Length Range: {prefs.min_length}-{prefs.max_length} characters\n")
        f.write(f"\nTotal names generated: {len(filtered_names)}\n")
        f.write(f"Top 1000 checked for availability\n")
        f.write(f"Available domains found: {len(available_domains)}\n\n")
        f.write("Names sorted by comprehensive score (investor + engineer + executive + technical + broader appeal + English word boost)\n\n")
        
        # Available domains section (priority)
        if available_domains:
            f.write("=" * 70 + "\n")
            f.write("AVAILABLE DOMAINS (Priority Order)\n")
            f.write("=" * 70 + "\n\n")
            for i, (name, score, status) in enumerate(available_domains, 1):
                breakdown = get_score_breakdown(name, prefs)
                f.write(f"{i:3d}. {name}.ai (Score: {score:.1f}) - {status}\n")
                f.write(f"     Inv:{breakdown['investor']:5.1f} | Eng:{breakdown['engineer']:5.1f} | ")
                f.write(f"Exec:{breakdown['executive']:5.1f} | Tech:{breakdown['technical']:5.1f} | ")
                f.write(f"Broad:{breakdown['broader']:5.1f}\n\n")
        
        # Top names with score breakdowns (all names, not just available)
        f.write("\n" + "=" * 70 + "\n")
        f.write("TOP 50 NAMES WITH SCORE BREAKDOWNS (All Names)\n")
        f.write("=" * 70 + "\n")
        for i, (name, total_score) in enumerate(filtered_names[:50], 1):
            breakdown = get_score_breakdown(name, prefs)
            english_score = score_english_word_like(name)
            f.write(f"\n{i:2d}. {name}.ai (Total: {total_score:.1f}, English: {english_score:.1f})\n")
            f.write(f"    Investor: {breakdown['investor']:.1f} | Engineer: {breakdown['engineer']:.1f} | ")
            f.write(f"Executive: {breakdown['executive']:.1f} | Technical: {breakdown['technical']:.1f} | ")
            f.write(f"Broader: {breakdown['broader']:.1f}\n")
        
        # Group by length for remaining names
        f.write(f"\n\n--- ALL NAMES BY LENGTH ---\n")
        by_length = {}
        for name, score in filtered_names:
            length = len(name)
            if length not in by_length:
                by_length[length] = []
            by_length[length].append((name, score))
        
        for length in sorted(by_length.keys()):
            f.write(f"\n--- {length} characters ---\n")
            # Sort by score within each length group
            by_length[length].sort(key=lambda x: -x[1])
            for name, score in by_length[length][:100]:  # Top 100 per length
                f.write(f"{name}.ai\n")
    
    print(f"\n✓ Generated {len(filtered_names)} domain name suggestions")
    print(f"✓ Saved to {output_file}")
    
    if available_domains:
        print(f"\n{'='*80}")
        print(f"AVAILABLE DOMAINS (Top {len(available_domains)} - Priority Order)")
        print(f"{'='*80}")
        print("(Scores: Investor | Engineer | Executive | Technical | Broader | English)")
        print("-" * 80)
        for i, (name, total_score, status) in enumerate(available_domains[:20], 1):
            breakdown = get_score_breakdown(name, prefs)
            english_score = score_english_word_like(name)
            print(f"{i:2d}. {name}.ai (Total: {total_score:5.1f}, English: {english_score:5.1f}) - {status}")
            print(f"    Inv:{breakdown['investor']:5.1f} | Eng:{breakdown['engineer']:5.1f} | "
                  f"Exec:{breakdown['executive']:5.1f} | Tech:{breakdown['technical']:5.1f} | "
                  f"Broad:{breakdown['broader']:5.1f}")
        if len(available_domains) > 20:
            print(f"\n... and {len(available_domains) - 20} more available domains (see file for full list)")
    else:
        print("\n⚠ No available domains found in top 1000. Check the full list in the output file.")
    
    print(f"\nTop 20 overall suggestions (all names):")
    print("(Scores: Investor | Engineer | Executive | Technical | Broader | English)")
    print("-" * 80)
    for i, (name, total_score) in enumerate(filtered_names[:20], 1):
        breakdown = get_score_breakdown(name, prefs)
        english_score = score_english_word_like(name)
        print(f"{i:2d}. {name}.ai (Total: {total_score:5.1f}, English: {english_score:5.1f})")
        print(f"    Inv:{breakdown['investor']:5.1f} | Eng:{breakdown['engineer']:5.1f} | "
              f"Exec:{breakdown['executive']:5.1f} | Tech:{breakdown['technical']:5.1f} | "
              f"Broad:{breakdown['broader']:5.1f}")


if __name__ == '__main__':
    main()
