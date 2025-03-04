import pandas as pd
import json

class DataLoader:
    def __init__(self, file_path: str):
        self.file_path = file_path

    def load_data(self) -> pd.DataFrame:
        """Load dataset from a JSON lines file, handling empty lines and errors."""
        data = []
        with open(self.file_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    record = json.loads(line)
                    data.append(record)
                except json.JSONDecodeError as e:
                    print(f"Skipping malformed line: {line}\nError: {e}")

        if not data:
            raise ValueError("No valid data found in the file.")

        df = pd.DataFrame(data)
        df['amount'] = pd.to_numeric(df['amount'], errors='coerce')
        df['height'] = pd.to_numeric(df['height'], errors='coerce')
        return df