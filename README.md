# Domain Name Generator

A Python script to generate and score domain names for information retrieval/AI companies. Generates names based on themes (science, computer science, machine learning, math, information retrieval, scale) and checks domain availability. Supports multiple theme selection and cross-theme name generation.

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
# Option 1: Use the runner script (recommended)
python3 run.py

# Option 2: Run directly from src directory
python3 src/generate_themed_names.py
```

The script will **interactively prompt you** for:

1. **Theme Selection**: Choose from 6 themes (can select multiple):
   - 1. science
   - 2. computer_science
   - 3. machine_learning
   - 4. math
   - 5. information_retrieval
   - 6. scale (big, large, deep, vast, magnitude)
   
   You can select multiple themes by entering comma-separated numbers (e.g., `1,3,6`). When multiple themes are selected, the script generates names for each theme individually AND creates cross-theme combinations (e.g., combining "math" and "scale" words).

2. **Number of Names to Generate**: How many names to generate (recommended: 10,000-100,000, max: 500,000)
   - More names = more variety
   - Generation, scoring, and sorting are fast - this won't take long
   - When multiple themes are selected, names are divided across themes plus cross-theme combinations

2b. **Name Length Constraints**: Minimum and maximum character length
   - Enter minimum length (default: 4)
   - Enter maximum length (default: 8)
   - Recommended: 4-8 characters (shorter is better for domains)

3. **Domain Availability Check** (default: yes): Check if domains are available using whois
   - Select TLD(s): .ai only, .com only, or both
   - How many available domains to find before stopping (recommended: 50-150, default: 100)
   - Note: Checking takes ~1 second per domain
   - **Cache**: The script automatically caches taken and available domains in `cache/`
     - Domains found to be taken/available are saved and skipped in future runs
     - Cache is updated incrementally (saved even if script is interrupted)
     - This speeds up subsequent checks significantly

The script will:
- Generate names based on the selected theme(s)
- Score each name across multiple dimensions
- Output results to `output/themed_names_{theme}_{num}.txt`
- Optionally check domain availability and save to `output/available_{theme}_{tld}_{num}_domains.txt`

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

## Project Structure

```
name_generator/
├── src/                          # Source code
│   ├── generate_themed_names.py  # Main script for themed name generation
│   ├── generate_domain_names.py  # Core scoring functions and utilities
│   └── add_definitions.py        # Definitions for common domain names
├── cache/                        # Cache files (auto-created)
│   ├── taken_domains_cache.txt   # Cache of known taken domains
│   └── available_domains_cache.txt  # Cache of known available domains
├── output/                       # Output files (auto-created)
│   ├── themed_names_{theme}_{num}.txt  # All generated names with scores
│   └── available_{theme}_{tld}_{num}_domains.txt  # Available domains
├── run.py                        # Runner script (recommended way to run)
├── README.md                     # This file
└── .gitignore                    # Git ignore rules
```

**Essential files (required to run):**
- `src/generate_themed_names.py` - Main script for themed name generation
- `src/generate_domain_names.py` - Core scoring functions and utilities
- `src/add_definitions.py` - Definitions for common domain names

**Optional files:**
- `cache/taken_domains_cache.txt` - Cache of known taken domains (speeds up future checks)
- `cache/available_domains_cache.txt` - Cache of known available domains
- `README.md` - This file

**Output files (generated when you run the script):**
- `output/themed_names_{theme}_{num}.txt` - All generated names with scores
- `output/available_{theme}_{tld}_{num}_domains.txt` - Available domains with scores and definitions

## Installation

1. Clone or download this repository
2. Ensure Python 3.6+ is installed
3. (Optional) Install `whois` for domain availability checking

That's it! No additional dependencies needed.

## Example Usage

```bash
python3 run.py
```

Then follow the interactive prompts to:
1. Select theme(s) (1-6, comma-separated for multiple)
2. Choose how many names to generate (recommended: 10,000-100,000)
3. Set name length constraints
4. Optionally check domain availability and select TLD(s) (.ai, .com, or both)
