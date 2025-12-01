# BOQ Tagging Challenge

## Background: Construction Procurement

When building a large construction project (apartment complex, office building, etc.), the work is divided among many specialized **subcontractors**:

- **Groundworks contractors** handle excavation, foundations, drainage
- **Concrete contractors** pour slabs, walls, and structural elements
- **Electrical contractors** install wiring, panels, and fixtures
- **Plumbing contractors** handle pipes, water systems, sanitation
- And many more: roofing, painting, steelwork, landscaping, etc.

### The Problem: Organizing Work Packages

Before construction begins, the **preconstruction team** creates a **Bill of Quantities (BOQ)** - a detailed spreadsheet listing every work item needed:

| Description                                 | QTY | Unit |
| ------------------------------------------- | --- | ---- |
| Excavate foundation trenches to 600mm depth | 150 | m³  |
| Supply and install 100mm copper pipes       | 200 | m    |
| Paint interior walls, 2 coats emulsion      | 500 | m²  |

Each of these items must be assigned to the right **trade package** so the procurement team knows which subcontractors to send quotes to. For example:

- "Excavate foundation trenches" → **Groundworks**
- "Supply and install copper pipes" → **Mechanical** (or **Plumbing**)
- "Paint interior walls" → **Painting**

This assignment is currently done manually by quantity surveyors, reviewing hundreds or thousands of line items per project. It's time-consuming and error-prone.

### Your Task

**Build an AI system that automatically assigns BOQ items to trade packages.**

You'll work with real (anonymized) BOQ Excel files from construction projects. Your goal is to:

1. Parse the Excel files to extract work items (rows with quantities)
2. Build a classifier each item into the appropriate trade package
3. Output your predictions in the required JSON format

## Data

### Input Files

> **Note:** The BOQ data files are provided separately via Google Drive. Download them to `data/boq_files/` before starting.

`data/boq_files/` contains several BOQ Excel workbooks. Each workbook may have:

- Multiple sheets (tabs)
- Various columns including descriptions, quantities, units, rates, etc.
- Different formatting and structure per file

### Key Columns

Most BOQ files have columns like:

- **DESCRIPTION**: What work needs to be done
- **QTY**: The quantity (items with quantities are actual work items)
- **TAG**: Trade package assignment
- Various pricing/costing columns

Explore the files to understand the structure.

### Output Format

Your solution **must** output a JSON file named `predictions.json` with this exact format:

```json
[
  {
    "file": "project_a.xlsx",
    "sheet": "BOQ",
    "row": 15,
    "item": "excavate foundation trenches to 600mm depth",
    "predicted_tag": "Groundworks"
  },
  {
    "file": "project_a.xlsx",
    "sheet": "BOQ",
    "row": 16,
    "item": "concrete to foundations 300mm thick",
    "predicted_tag": "Concrete + Formwork"
  }
]
```

**Required fields:**

- `file`: The Excel filename (string)
- `sheet`: The sheet/tab name (string)
- `row`: The 1-indexed row number in the Excel file (integer)
- `item`: The description text from that row (string)
- `predicted_tag`: Your predicted trade package (string)

### Evaluation

We will run your solution on **held-out Excel files** (files you haven't seen) and measure accuracy of your trade package predictions against our ground truth.

## Constraints

- **Time:** ~4 hours (please don't spend significantly more)
- **API:** OpenAI API key provided (GPT-4o-mini or GPT-4o)
- **Language:** Python

## Submission

1. **Fork this repository** to your own GitHub account
2. Clone your fork and complete the challenge:
3. Push your completed work to your forked repository
4. Invite `Gregory-PublishAI` as a collaborator to your forked repository
5. Email us with the link to your forked repository when ready

**Your submission should include:**

- Your solution code (runnable)
- `predictions.json` for the provided development files
- Fill in `NOTES.md` with:
  - Your approach and reasoning
  - Trade-offs you made
  - Ideas for improvement if you had more time

## Evaluation Criteria

1. **Does it work?** - Produces valid predictions, handles the data
2. **Approach** - How did you think about the problem?
3. **Code quality** - Readable, maintainable, well-organized
4. **Creativity** - Any interesting ideas or extensions?

## Extensions (Optional)

If you finish early and want to impress us, feel free to add any extensions you think would be valuable.

## Setup (Venv)

```bash
pip install -r requirements.txt
cp .env.example .env  # Then add your API key
```

## Provided Utilities

We've included some helper functions in `src/` to get you started:

### `src/utils.py`

- `load_boq_items(excel_path)` - Load work items from a BOQ Excel file
- `save_predictions(predictions, output_path)` - Save predictions to JSON

### `src/llm.py`

- `prompt(input, model, instructions, reasoning)` - Simple OpenAI API wrapper

Example usage:

```python
from src.utils import load_boq_items, save_predictions
from src.llm import prompt

# Load items from an Excel file
items = load_boq_items("data/boq_files/project_a.xlsx")

# Use OpenAI to classify
response = prompt(
    input="What trade would handle excavation work?",
    instructions="You are a construction expert."
)
```

## Questions?

Email gregory@muro.ai if you have questions about the task.
