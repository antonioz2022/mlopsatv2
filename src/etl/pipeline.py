import pandas as pd
from .extractor import Extractor
from .transformer import Transformer
from .loader import Loader
from .config import ETLConfig

class DeliveryETLPipeline:
    def __init__(self, config: ETLConfig):
        self.config = config
        self.extractor = Extractor(config.raw_path)
        self.transformer = Transformer(
            missing_tokens=config.missing_tokens,
            target_col=config.target_col,
            date_cols=config.date_cols,
            numeric_cols=config.numeric_cols,
        )
        self.loader = Loader(config.processed_path)

    def run(self) -> pd.DataFrame:
        df = self.extractor.read_csv()

        # LIMPEZA (o que vocês fizeram no EDA)
        df = self.transformer.replace_missing_tokens(df)
        df = self.transformer.coerce_numeric(df)
        df = self.transformer.parse_dates(df)
        df = self.transformer.drop_missing_critical(df)

        # FEATURE ENGINEERING “ETL style”
        df = self.transformer.create_time_features(df)

        # NORMALIZAÇÃO (opcional por enquanto, mas já deixa pronto)
        df = self.transformer.normalize_numeric_zscore(
            df,
            cols=["valor_compra", "peso_kg", "distancia_km", "avaliacao_cliente"]
        )

        # CARGA
        self.loader.save_csv(df)
        return df