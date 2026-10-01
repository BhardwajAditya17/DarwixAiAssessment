from pathlib import Path
import pandas as pd


def load_csv_file(file_path: str, source_type: str = "table") -> dict:
    path = Path(file_path)

    df = pd.read_csv(path)

    records = df.to_dict(orient="records")

    title = path.stem.replace("_", " ").title()

    return {
        "document_id": f"{source_type}_{path.stem}",
        "source_type": source_type,
        "source_file": str(path),
        "title": title,
        "content": records,
        "metadata": {
            "file_name": path.name,
            "file_extension": path.suffix,
            "row_count": len(df),
            "columns": list(df.columns),
        },
    }
