"""
Módulo para carregar e processar datasets do Our World in Data
"""
import pandas as pd
import json
from pathlib import Path
from typing import Dict, Optional, Tuple
from src.config import DATASETS


def load_dataset(dataset_key: str = "hdi") -> Tuple[pd.DataFrame, Dict]:
    """
    Carrega um dataset CSV e seus metadados JSON
    
    Args:
        dataset_key: Chave do dataset em DATASETS config
        
    Returns:
        Tupla com (DataFrame, metadados)
    """
    if dataset_key not in DATASETS:
        raise ValueError(f"Dataset '{dataset_key}' não encontrado. Disponíveis: {list(DATASETS.keys())}")
    
    config = DATASETS[dataset_key]
    
    # Carregar CSV
    if not config["csv_file"].exists():
        raise FileNotFoundError(f"Arquivo CSV não encontrado: {config['csv_file']}")
    
    df = pd.read_csv(config["csv_file"])
    
    # Carregar metadados
    metadata = {}
    if config["metadata_file"].exists():
        with open(config["metadata_file"], "r", encoding="utf-8") as f:
            metadata = json.load(f)
    
    return df, metadata


def clean_hdi_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Limpa e prepara dados do HDI
    
    Args:
        df: DataFrame com dados brutos
        
    Returns:
        DataFrame limpo
    """
    df_clean = df.copy()
    
    # Remover linhas com valores NaN no HDI
    df_clean = df_clean.dropna(subset=["Human Development Index"])
    
    # Garantir que Year é numérico
    df_clean["Year"] = pd.to_numeric(df_clean["Year"], errors="coerce")
    
    # Remover linhas com Year inválido
    df_clean = df_clean.dropna(subset=["Year"])
    
    # Ordenar por Entity e Year
    df_clean = df_clean.sort_values(["Entity", "Year"])
    
    return df_clean


def get_available_countries(df: pd.DataFrame) -> list:
    """
    Retorna lista de países disponíveis no dataset
    
    Args:
        df: DataFrame com dados
        
    Returns:
        Lista ordenada de países únicos
    """
    countries = df["Entity"].unique().tolist()
    # Remover entidades que não são países (como regiões)
    regions = ["Africa", "Asia", "Europe", "North America", "South America", 
               "Oceania", "World", "European Union"]
    countries = [c for c in countries if c not in regions]
    return sorted(countries)


def get_available_years(df: pd.DataFrame) -> Tuple[int, int]:
    """
    Retorna o range de anos disponível
    
    Args:
        df: DataFrame com dados
        
    Returns:
        Tupla com (ano_min, ano_max)
    """
    return int(df["Year"].min()), int(df["Year"].max())


def filter_data(df: pd.DataFrame, 
                countries: Optional[list] = None,
                years: Optional[Tuple[int, int]] = None,
                region: Optional[str] = None) -> pd.DataFrame:
    """
    Filtra dados por país, ano ou região
    
    Args:
        df: DataFrame com dados
        countries: Lista de países para filtrar
        years: Tupla com (ano_min, ano_max)
        region: Nome da região para filtrar
        
    Returns:
        DataFrame filtrado
    """
    df_filtered = df.copy()
    
    if countries:
        df_filtered = df_filtered[df_filtered["Entity"].isin(countries)]
    
    if years:
        min_year, max_year = years
        df_filtered = df_filtered[
            (df_filtered["Year"] >= min_year) & 
            (df_filtered["Year"] <= max_year)
        ]
    
    if region:
        df_filtered = df_filtered[df_filtered["World regions according to OWID"] == region]
    
    return df_filtered

