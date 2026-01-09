# Domain Name Generator

A Python script to generate and score domain names for information retrieval/AI companies. Generates names based on themes (science, computer science, machine learning, math, information retrieval) and checks domain availability.

## Requirements

- Python 3.6+
- No external dependencies (uses only standard library)
- Optional: `whois` command for domain availability checking
  - macOS: `brew install whois`
  - Linux: Usually pre-installed
  - Windows: Install from [Sysinternals](https://docs.microsoft.com/en-us/sysinternals/downloads/whois) or use WSL

## Usage

Run the themed name generator:

```bash
python3 generate_themed_names.py
```

The script will **interactively prompt you** for:

1. **Theme Selection**: Choose from 5 themes:
   - science
   - computer_science
   - machine_learning
   - math
   - information_retrieval

2. **Number of Names to Generate**: How many names to generate (recommended: 500-2000)
   - More names = more variety, but takes longer to process

2b. **Name Length Constraints**: Minimum and maximum character length
   - Enter minimum length (default: 4)
   - Enter maximum length (default: 8)
   - Recommended: 4-8 characters (shorter is better for domains)

3. **Domain Availability Check** (optional): Check if domains are available using whois
   - How many available domains to find before stopping (recommended: 10-100)
   - Note: Checking takes ~1 second per domain (~2 minutes for 100 domains)
   - **Cache**: The script automatically caches taken domains in `taken_domains_cache.txt`
     - Domains found to be taken are saved and skipped in future runs
     - This speeds up subsequent checks significantly

The script will:
- Generate names based on the selected theme
- Score each name across multiple dimensions
- Output results to `themed_names_{theme}.txt`
- Optionally check domain availability and save to `available_{theme}_domains.txt`

## Output Format

The output file includes:
- **Theme**: Relevance to selected theme (0-100)
- **English**: How English-word-like (100 = perfect English word)
- **Base**: Overall quality score (combines all dimensions)
- **Total**: Final ranking score = Base + (Theme * 0.3)

**Breakdown dimensions:**
- **Inv**: Investor appeal
- **Eng**: Engineer appeal (ML/search terms)
- **Exec**: Executive appeal (accessible, professional)
- **Tech**: Technical depth (sophistication)
- **Broad**: Broader appeal (universal accessibility)

## Files

**Essential files (required to run):**
- `generate_themed_names.py` - Main script for themed name generation
- `generate_domain_names.py` - Core scoring functions and utilities
- `add_definitions.py` - Definitions for common domain names

**Optional files:**
- `taken_domains_cache.txt` - Cache of known taken domains (speeds up future checks)
- `README.md` - This file

**Output files (generated when you run the script):**
- `themed_names_{theme}.txt` - All generated names with scores
- `available_{theme}_domains.txt` - Available domains with scores and definitions

## Installation

1. Clone or download this repository
2. Ensure Python 3.6+ is installed
3. (Optional) Install `whois` for domain availability checking

That's it! No additional dependencies needed.

## Example Usage

```bash
python3 generate_themed_names.py
```

Then follow the interactive prompts to:
1. Select a theme
2. Choose how many names to generate
3. Set name length constraints
4. Optionally check domain availability
