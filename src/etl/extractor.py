import pandas as pd
from pathlib import Path

class Extractor:
    def __init__(self, raw_path: Path):
        self.raw_path = raw_path

    def read_csv(self) -> pd.DataFrame:
        return pd.read_csv(self.raw_path)