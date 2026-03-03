from pathlib import Path
from src.etl.config import ETLConfig
from src.etl.pipeline import DeliveryETLPipeline

def main():
    config = ETLConfig(
        raw_path=Path("data/raw/entregas.csv"),
        processed_path=Path("data/processed/entregas_clean.csv"),
    )

    pipeline = DeliveryETLPipeline(config)
    df_clean = pipeline.run()
    print("ETL finalizado! Shape:", df_clean.shape)
    print(df_clean.head())

if __name__ == "__main__":
    main()