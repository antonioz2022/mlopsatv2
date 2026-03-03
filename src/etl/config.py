from dataclasses import dataclass
from pathlib import Path

@dataclass
class ETLConfig:
    raw_path: Path
    processed_path: Path

    # regras de limpeza
    missing_tokens: tuple = ("?",)
    target_col: str = "atraso"

    # colunas do dataset
    date_cols: tuple = ("data_pedido", "data_envio", "data_entrega_prevista", "data_entrega_real")
    numeric_cols: tuple = ("valor_compra", "peso_kg", "distancia_km", "avaliacao_cliente")