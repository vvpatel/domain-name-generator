#!/usr/bin/env python3
"""
Add short definitions to domain names.
"""

import re

# Dictionary of definitions for common terms
DEFINITIONS = {
    # Core IR/CS/ML terms
    'search': 'to look for information in a database or system',
    'vector': 'a mathematical object with magnitude and direction, used in ML and linear algebra',
    'tensor': 'a multidimensional array used in machine learning and physics',
    'matrix': 'a rectangular array of numbers used in mathematics and computer science',
    'index': 'a data structure for fast lookup and retrieval of information',
    'rank': 'to order items by relevance, importance, or quality',
    'query': 'a request for information from a database or search system',
    'parse': 'to analyze and break down into parts',
    'extract': 'to pull out or obtain',
    'filter': 'to remove or separate items',
    'match': 'to correspond or be equal',
    'token': 'a unit or symbol',
    'corpus': 'a collection of texts',
    'cluster': 'a group of similar items',
    'cache': 'a temporary storage for quick access',
    'database': 'an organized collection of data',
    'dataset': 'a collection of data',
    'document': 'a file or record containing information',
    'encode': 'to convert into a coded form',
    'decode': 'to convert from a coded form',
    'research': 'systematic investigation to establish facts or principles',
    'ranker': 'a system or algorithm that orders items by relevance',
    'ranked': 'ordered by relevance, importance, or quality',
    'pascal': 'Blaise Pascal, French mathematician and physicist, or the Pascal programming language',
    'newton': 'Isaac Newton, English mathematician and physicist who formulated laws of motion',
    'turing': 'Alan Turing, British mathematician and computer scientist, father of computer science',
    'darwin': 'Charles Darwin, English naturalist who developed theory of evolution',
    'euler': 'Leonhard Euler, Swiss mathematician who made contributions to many fields',
    'gauss': 'Carl Friedrich Gauss, German mathematician known as the prince of mathematicians',
    'field': 'a mathematical structure or a data field in computing',
    'exact': 'precise, accurate, without error',
    'wave': 'a disturbance that transfers energy, or a signal pattern',
    'pure': 'unmixed, uncontaminated, or purely functional in programming',
    'theory': 'a system of ideas explaining observations or phenomena',
    'discover': 'to find or identify something previously unknown',
    'explore': 'to investigate or examine systematically',
    'matter': 'physical substance, or to be of importance',
    'precise': 'exact, accurate, clearly defined',
    'prove': 'to demonstrate truth or validity',
    'locate': 'to find the position of something',
    'lookup': 'to search for information',
    'hash': 'a function that maps data to a fixed-size value',
    'sort': 'to arrange in order',
    'join': 'to combine or connect',
    'merge': 'to combine into one',
    'split': 'to divide into parts',
    'slice': 'to cut or extract a portion',
    'transform': 'to change the form or structure',
    'normalize': 'to standardize or adjust to a common scale',
    'optimize': 'to make as effective as possible',
    'train': 'to teach or prepare through practice',
    'learn': 'to gain knowledge or skill',
    'model': 'a representation or simulation',
    'predict': 'to forecast or estimate',
    'classify': 'to categorize or organize',
    'embed': 'to incorporate or represent',
    'similarity': 'the state of being similar',
    'distance': 'a measure of separation',
    'metric': 'a standard of measurement',
    'accuracy': 'the degree of correctness',
    'precision': 'the quality of being exact',
    'recall': 'the ability to retrieve information',
    'relevance': 'the quality of being pertinent',
}

def get_definition(name: str) -> str:
    """Get definition for a domain name."""
    name_lower = name.lower()
    
    # Direct lookup
    if name_lower in DEFINITIONS:
        return DEFINITIONS[name_lower]
    
    # Check for common suffixes and try base word
    suffixes = ['er', 'or', 'ed', 'ing', 'ion', 'ive', 'al', 'ic', 'ous', 'est', 'ly']
    for suffix in suffixes:
        if name_lower.endswith(suffix):
            base = name_lower[:-len(suffix)]
            if base in DEFINITIONS:
                base_def = DEFINITIONS[base]
                return f'variant of {base}, {base_def}'
    
    # Check for compound words (two words combined)
    # Try to split at common boundaries
    for i in range(3, len(name_lower) - 2):
        part1 = name_lower[:i]
        part2 = name_lower[i:]
        if part1 in DEFINITIONS and part2 in DEFINITIONS:
            def1 = DEFINITIONS[part1]
            def2 = DEFINITIONS[part2]
            return f'combines {part1} ({def1}) and {part2} ({def2})'
    
    # No definition found
    return ''
