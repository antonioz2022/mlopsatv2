import pandas as pd
from pathlib import Path

class Loader:
    def __init__(self, processed_path: Path):
        self.processed_path = processed_path

    def save_csv(self, df: pd.DataFrame) -> None:
        self.processed_path.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(self.processed_path, index=False)