import pandas as pd

class Transformer:
    def __init__(self, missing_tokens=("?",), target_col="atraso", date_cols=(), numeric_cols=()):
        self.missing_tokens = missing_tokens
        self.target_col = target_col
        self.date_cols = list(date_cols)
        self.numeric_cols = list(numeric_cols)

    def replace_missing_tokens(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()
        for tok in self.missing_tokens:
            df.replace(tok, pd.NA, inplace=True)
        return df

    def drop_missing_critical(self, df: pd.DataFrame) -> pd.DataFrame:
        # remove linhas onde target ou avaliacao_cliente estão faltando (como vocês pediram)
        df = df.copy()
        cols = [self.target_col, "avaliacao_cliente"]
        existing = [c for c in cols if c in df.columns]
        return df.dropna(subset=existing)

    def coerce_numeric(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()
        for c in self.numeric_cols:
            if c in df.columns:
                df[c] = pd.to_numeric(df[c], errors="coerce")
        return df

    def parse_dates(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()
        for c in self.date_cols:
            if c in df.columns:
                df[c] = pd.to_datetime(df[c], errors="coerce")
        return df

    def create_time_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Features úteis (sem ML ainda): tempos em dias.
        """
        df = df.copy()
        if {"data_pedido","data_envio"}.issubset(df.columns):
            df["tempo_envio"] = (df["data_envio"] - df["data_pedido"]).dt.days

        if {"data_envio","data_entrega_prevista"}.issubset(df.columns):
            df["tempo_entrega_previsto"] = (df["data_entrega_prevista"] - df["data_envio"]).dt.days

        if {"data_envio","data_entrega_real"}.issubset(df.columns):
            df["tempo_entrega_real"] = (df["data_entrega_real"] - df["data_envio"]).dt.days

        return df

    def normalize_numeric_zscore(self, df: pd.DataFrame, cols: list[str]) -> pd.DataFrame:
        """
        Normalização simples (z-score) no estilo ETL:
        (x - média) / desvio
        """
        df = df.copy()
        for c in cols:
            if c in df.columns:
                mean = df[c].mean()
                std = df[c].std()
                if std and std != 0:
                    df[c] = (df[c] - mean) / std
        return df