import pandas as pd
from pathlib import Path
import random
from typing import List

# Configuration
INPUT_DATA_PATH = Path("data/structured_dataset.csv")
OUTPUT_DIRS = {
    "processed": Path("processed"),
    "embeddings": Path("embeddings")
}
TRAIN_TEST_SPLIT = 0.8
RANDOM_STATE = 42
X_FIELDS = [
    "name", "unit no", "admission date", "date of birth", "sex", "service",
    "allergies", "attending", "chief complaint", "major surgical or invasive procedure",
    "history of present illness", "past medical history", "social history",
    "family history", "physical exam", "pertinent results", "medications on admission"
]
X_FIELDS = [field.lower() for field in X_FIELDS]

def combine_fields(row: pd.Series, fields: List[str]) -> str:
    """Combine non-empty fields from a row into a formatted string.
    
    Args:
        row: Pandas Series representing a row of data
        fields: List of field names to include
        
    Returns:
        Concatenated string of non-empty fields
    """
    chunks = []
    for field in fields:
        val = row.get(field)
        if pd.notna(val) and str(val).strip():
            chunks.append(f"{field.title()}: {val}")
    return " ".join(chunks)

def main():
    # Create output directories
    for dir_path in OUTPUT_DIRS.values():
        dir_path.mkdir(exist_ok=True)

    # Load and shuffle data
    df = pd.read_csv(INPUT_DATA_PATH)
    df.columns = [col.strip().lower() for col in df.columns]
    df = df.sample(frac=1, random_state=RANDOM_STATE).reset_index(drop=True)
    
    # Split data
    split_idx = int(TRAIN_TEST_SPLIT * len(df))
    train_df = df.iloc[:split_idx].copy()
    test_df = df.iloc[split_idx:].copy()

    # Save splits
    train_df.to_csv(OUTPUT_DIRS["processed"]/"training_data.csv", index=False)
    test_df.drop(columns=["summary"], errors="ignore").to_csv(
        OUTPUT_DIRS["processed"]/"test_patients.csv", index=False
    )

    # Create RAG input text
    input_lines = train_df.apply(combine_fields, axis=1, fields=X_FIELDS)
    input_lines = input_lines[input_lines.str.strip() != ""]

    with open(OUTPUT_DIRS["embeddings"]/"input_texts.txt", "w", encoding="utf-8") as f:
        for line in input_lines:
            f.write(line.strip() + "\n")

    print("✅ Done! Files created:")
    print(f"- {OUTPUT_DIRS['processed']/'training_data.csv'}")
    print(f"- {OUTPUT_DIRS['processed']/'test_patients.csv'}")
    print(f"- {OUTPUT_DIRS['embeddings']/'input_texts.txt'}")

if __name__ == "__main__":
    main()