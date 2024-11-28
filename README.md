# Tree-Property-Value-Analyzer

## Overview

The **Tree-Property-Value-Analyzer** project analyzes the correlation between tree heights and property values. The goal is to determine whether properties located on streets with tall trees are more expensive compared to those on streets with shorter trees. This project utilizes datasets containing information about tree heights and property prices.

## Code Challenge Description

Do more trees mean more money? Are houses more expensive on streets with tall trees compared to those with shorter trees? Let's find out!

### Datasets

We have two files: `dublin-trees.json` and `dublin-property.csv`:

- **dublin-trees.json** contains a list of street names categorized into `short` and `tall`, based on the median tree height as recorded by Dublin City Council.
  
- **dublin-property.csv** contains a subset of the Residential Property Price Register, listing property addresses, their street names, and sale prices in euro.

The street names in `dublin-trees.json` exactly match the `Street Name` column in `dublin-property.csv`.

### dublin-trees.json Structure

The structure of `dublin-trees.json` contains two top-level entries: `short` and `tall`. Street names are organized in an arbitrarily nested structure, where only the entries with heights are relevant.

Example structure:
```json
{
    "short": {
        "drive": {
            "abbey": {
                "abbey drive": 0
            },
            "coolrua": {
                "coolrua drive": 10
            },
            "coultry": {
                "coultry drive": 5
            }
        }
    },
    "tall": {
        "gardens": {
            "temple": {
                "temple gardens": 20
            }
        },
        "bramblings": {
            "the": {
                "the bramblings": 20
            }
        }
    }
}
```

The "short tree" street names in this example are:
- **abbey drive**
- **coolrua drive**
- **coultry drive**

and the "tall tree" street names are:
- **temple gardens**
- **the bramblings**

## Your Task

Write a program that takes these files and outputs the average cost of a property:
- on a street with tall trees
- on a street with short trees

We might want to run this program as part of some larger system, so your code should not require any user input or any user interaction once it starts.

We expect this task to take you about 1 hour, though there is no time limit.

We recommend you write your answer in the language you're most comfortable working in. You can use open source libraries, tools in the standard library, search Google, StackOverflow, etc. -- anything you might do in a real day-to-day production programming task.

### We'd like:
- Your code to be as close to "production ready" as possible
- A minimal set of unit tests (does not need to be comprehensive, we'd like you to stay close to 1 hour in total)
- A README with the basic instructions you'd give another developer to run your code

Please package your code in a single zip file.

If you have any questions, please let us know.


## Evaluation

These points are used by the engineering team to evaluate submissions.

- The exercise is packaged as a single zip file.
- There is a README (text or markdown) at the top-level of the zip with all of the instructions required to build, run and test.
- There are unit tests.
- Variable and functions are well named, with no generic names - e.g. parse_price() not process().
- Code is well structured, generally functions only do one thing (and do it well):
  - Tests can cover individual steps of the exercise, rather than tests that need to execute everything end-to-end.
  - This is a short, well-contained problem. The architecture should be similarly straight-forward with minimal complexity.
  - Error handling is appropriate for use as a library - could someone re-use portions of this codebase and be confident in the correctness of the answers produced?
- Logic is implemented in an appropriate place for production-ready code. E.g. if this is Ruby code, it's not appropriate for all the processing logic to be implemented in SQLite calls.
- Dependencies are appropriate for production-ready code.
- Only code related to the question is reviewed. Fancy HTML presentation, container configuration, etc. must be ignored - it's not part of the question.

## Original Datasets

Please use the files we've supplied for this exercise, as we've tweaked them slightly to make things easier. The original datasets come from:

- Dublin City Council's tree data: https://data.smartdublin.ie/dataset/tree-dcc
- Ireland's Residential Property Price Register: https://www.propertypriceregister.ie/



## Instructions

1. Download the provided data files:
   - `dublin-trees.json`: Contains tree height data for Dublin streets
   - `dublin-property.csv`: Contains property price data

2. Place the data files in the `data/` directory of the project.

## Installation

1. Ensure you have Python 3.12+ installed:

```bash
python --version
```

2. Install Poetry (dependency management):

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

3. Install dependencies:

```bash
poetry install
```

## Usage
1. Run the analysis:

```bash
poetry run python brightbeam_analysis/main.py
```

2. Run tests:
```bash
poetry run pytest
```

## Project Structure
tree-property-value-analyzer/
│
├── pyproject.toml        # Project configuration, dependencies
├── README.md             # Project documentation
│
├── brightbeam_analysis/  # Main package
│   ├── __init__.py
│   │
│   ├── main.py           # Entry point, orchestrates the analysis
│   ├── analysis_service.py # Coordinates the analysis pipeline
│   ├── price_analyzer.py  # Business logic for price analysis
│   ├── utils.py          # Utility functions (result printing)
│   ├── exceptions.py     # Custom exception definitions
│   ├── models.py         # Pydantic models for data validation
│   │
│   ├── parsers/          # Data parsing modules
│   │   ├── __init__.py
│   │   ├── trees_parser.py     # JSON tree data parser
│   │   └── properties_parser.py # CSV property data parser
│   │
│   └── tests/            # Test suite
│       ├── __init__.py
│       ├── test_analysis_service.py
│       ├── test_models.py
│       ├── test_properties_parser.py
│       └── test_trees_parser.py
│
└── data/                 # Input data files
    ├── dublin-trees.json
    └── dublin-property.csv


## Error Handling

The analyzer handles several error cases:
- Missing or invalid input files
- Malformed JSON/CSV data
- Invalid tree heights
- Invalid property prices
- Insufficient data for analysis

## Development

### Code Style
The project uses:
- Ruff for linting

Format code:

2. Run tests:
```bash
ruff check . --fix
```