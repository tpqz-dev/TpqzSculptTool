# Fantastic Four Wikipedia Agent

## Description

This agent fetches information about the Fantastic Four superheroes from Wikipedia and creates a JSON file with their superhero names, secret identities, and superpowers.

## Usage

```bash
python3 fantastic_four_agent.py
```

This will create a `fantastic_four.json` file containing information about all four members:
- Mister Fantastic (Reed Richards)
- Invisible Woman (Susan Storm-Richards)
- Human Torch (Johnny Storm)
- The Thing (Ben Grimm)

## Output Format

The generated JSON file contains:
- Team name (in English and French)
- List of members with:
  - Superhero name
  - Secret identity
  - Superpower description

## Requirements

- Python 3.x
- requests library (for Wikipedia API access)

## Note

The script includes fallback data in case Wikipedia is not accessible, ensuring it always produces valid output.
