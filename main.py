# #!/usr/bin/env python3
"""
BOQ Trade Tagging Solution

Loads BOQ Excel files, classifies each work item into a trade package
using an LLM, and outputs predictions.json in the required format.
"""
import csv
import argparse
from pathlib import Path
from src.utils import load_boq_items, save_predictions, compare_predictions, load_allowed_tag, normalize_tag
from src.llm import classify_trade

UNIQUE_TAGS_CSV = 'tags_classification_by_llm.csv'

DATA_DIR = Path("data/boq_files")
FALLBACK_TAG = "General / Preliminaries"

def main():
    # Load allowed Tags
    allowed_trades_dic, allowed_trades = load_allowed_tag(UNIQUE_TAGS_CSV)

    excel_files = sorted(DATA_DIR.glob("*.xlsx"))
    if not excel_files:
        raise RuntimeError(f"No Excel files found in {DATA_DIR}")

    for excel_path in excel_files:
        print(f"Processing file: {excel_path.name}")

        items = load_boq_items(excel_path)
        print(f"Found {len(items)} work items")

        all_predictions = []
        for _, item in enumerate(items, start=1):
            raw_prediction = classify_trade(
                description=item["description"],
                allowed_trades=allowed_trades
            )

            predicted_tag = normalize_tag(raw_prediction)
            if predicted_tag not in allowed_trades:
                predicted_tag = FALLBACK_TAG

            all_predictions.append({
                "file": item["file"],
                "sheet": item["sheet"],
                "row": item["row"],
                "item": item["description"],
                "predicted_tag": predicted_tag,
            })

        save_predictions(all_predictions, "predictions_"+excel_path.name.split('.')[0]+".json")
        print(f"Saved {len(all_predictions)} predictions of {excel_path.name} file to predictions_"+excel_path.name.split('.')[0]+".json")

        total, correct, mismatches = compare_predictions(all_predictions, allowed_trades_dic)
        
        # Accuracy per parser
        accuracy = correct / total if total else 0
        print(f"Total Trades: {total}, Correctly Classified: {correct}, Accuracy: {accuracy:.2%}")
        #print(f"Mismatches:\n {mismatches}")
        

if __name__ == "__main__":
    main()