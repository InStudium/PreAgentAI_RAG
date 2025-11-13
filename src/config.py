"""
Configurações centralizadas do projeto
"""
import os
from pathlib import Path

# Caminhos base
BASE_DIR = Path(__file__).parent.parent
DATABASE_DIR = BASE_DIR / "Database"
EMBEDDINGS_DIR = BASE_DIR / "embeddings"
DOCS_DIR = BASE_DIR / "docs"

# Criar diretórios se não existirem
EMBEDDINGS_DIR.mkdir(exist_ok=True)
DOCS_DIR.mkdir(exist_ok=True)

# Configurações de datasets
DATASETS = {
    "hdi": {
        "csv_file": DATABASE_DIR / "human-development-index.csv",
        "metadata_file": DATABASE_DIR / "human-development-index.metadata.json",
        "name": "Human Development Index",
        "description": "Índice de Desenvolvimento Humano (HDI)"
    }
}

# Configurações RAG
RAG_CONFIG = {
    "model_name": "sentence-transformers/all-MiniLM-L6-v2",
    "top_k": 5,  # Número de documentos mais relevantes a retornar
    "similarity_threshold": 0.3,  # Threshold mínimo de similaridade
    "embeddings_cache_file": EMBEDDINGS_DIR / "knowledge_base_embeddings.pkl"
}

# Configurações de visualização
VIZ_CONFIG = {
    "default_years": (1990, 2023),
    "default_countries": ["Brazil", "United States", "China", "India", "Germany"],
    "color_palette": "plotly"
}

