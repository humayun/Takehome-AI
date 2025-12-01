#!/usr/bin/env python3
"""
BOQ Tagging Utilities

Helper functions for loading BOQ data and saving predictions.
"""
import json
from pathlib import Path

from openpyxl import load_workbook


def load_boq_items(excel_path: str) -> list[dict]:
    """
    Load work items from a BOQ Excel file.

    Returns list of items, each with:
    - file: filename
    - sheet: sheet name
    - row: 1-indexed row number
    - description: the work item description
    - qty: the quantity value

    Only returns rows that have a numeric QTY value (actual work items).
    """
    wb = load_workbook(excel_path, data_only=True)
    items = []
    filename = Path(excel_path).name

    for sheet_name in wb.sheetnames:
        sheet = wb[sheet_name]

        # Find header row (look for DESCRIPTION and QTY columns)
        desc_col = qty_col = header_row = None
        for row in range(1, min(10, sheet.max_row + 1)):
            for col in range(1, min(15, sheet.max_column + 1)):
                val = sheet.cell(row=row, column=col).value
                if val and str(val).strip().upper() == "DESCRIPTION":
                    desc_col = col
                    header_row = row
                elif val and str(val).strip().upper() == "QTY":
                    qty_col = col

        if not all([desc_col, qty_col, header_row]):
            continue  # Skip sheets without required columns

        # Extract items with QTY values
        for row in range(header_row + 1, sheet.max_row + 1):
            qty_val = sheet.cell(row=row, column=qty_col).value
            desc_val = sheet.cell(row=row, column=desc_col).value

            # Only include rows with numeric QTY
            try:
                float(qty_val)
            except (ValueError, TypeError):
                continue

            if desc_val:
                items.append({
                    "file": filename,
                    "sheet": sheet_name,
                    "row": row,
                    "description": str(desc_val).strip(),
                    "qty": qty_val,
                })

    return items


def save_predictions(predictions: list[dict], output_path: str = "predictions.json"):
    """Save predictions to JSON file in the required format."""
    with open(output_path, "w") as f:
        json.dump(predictions, f, indent=2)
    print(f"Saved {len(predictions)} predictions to {output_path}")
