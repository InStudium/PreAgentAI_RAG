"""
Funções de visualização reutilizáveis para o dashboard
"""
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from typing import List, Optional, Tuple


def plot_hdi_timeline(df: pd.DataFrame, 
                     countries: Optional[List[str]] = None,
                     title: str = "Evolução do HDI ao Longo do Tempo") -> go.Figure:
    """
    Cria gráfico de linha mostrando evolução do HDI por país
    
    Args:
        df: DataFrame com dados do HDI
        countries: Lista de países para plotar (None = todos)
        title: Título do gráfico
        
    Returns:
        Figura Plotly
    """
    df_plot = df.copy()
    
    if countries:
        df_plot = df_plot[df_plot["Entity"].isin(countries)]
    
    fig = px.line(
        df_plot,
        x="Year",
        y="Human Development Index",
        color="Entity",
        title=title,
        labels={
            "Year": "Ano",
            "Human Development Index": "HDI",
            "Entity": "País"
        },
        hover_data=["Code"]
    )
    
    fig.update_layout(
        xaxis_title="Ano",
        yaxis_title="Índice de Desenvolvimento Humano (HDI)",
        hovermode="x unified",
        height=500
    )
    
    return fig


def plot_hdi_comparison(df: pd.DataFrame,
                       year: int,
                       top_n: int = 20,
                       title: str = "Comparação de HDI entre Países") -> go.Figure:
    """
    Cria gráfico de barras comparando HDI entre países em um ano específico
    
    Args:
        df: DataFrame com dados do HDI
        year: Ano para comparação
        top_n: Número de países para mostrar (top N)
        title: Título do gráfico
        
    Returns:
        Figura Plotly
    """
    df_year = df[df["Year"] == year].copy()
    
    # Remover entidades que não são países
    regions = ["Africa", "Asia", "Europe", "North America", "South America", 
               "Oceania", "World", "European Union"]
    df_year = df_year[~df_year["Entity"].isin(regions)]
    
    # Ordenar e pegar top N
    df_year = df_year.nlargest(top_n, "Human Development Index")
    
    fig = px.bar(
        df_year,
        x="Human Development Index",
        y="Entity",
        orientation="h",
        title=f"{title} - {year}",
        labels={
            "Human Development Index": "HDI",
            "Entity": "País"
        },
        color="Human Development Index",
        color_continuous_scale="Viridis"
    )
    
    fig.update_layout(
        yaxis={"categoryorder": "total ascending"},
        height=max(400, top_n * 30),
        xaxis_title="Índice de Desenvolvimento Humano (HDI)",
        yaxis_title=""
    )
    
    return fig


def plot_hdi_heatmap(df: pd.DataFrame,
                    countries: List[str],
                    title: str = "Heatmap de HDI por País e Ano") -> go.Figure:
    """
    Cria heatmap mostrando HDI por país e ano
    
    Args:
        df: DataFrame com dados do HDI
        countries: Lista de países para incluir
        title: Título do gráfico
        
    Returns:
        Figura Plotly
    """
    df_plot = df[df["Entity"].isin(countries)].copy()
    
    # Criar pivot table
    pivot = df_plot.pivot_table(
        values="Human Development Index",
        index="Entity",
        columns="Year",
        aggfunc="mean"
    )
    
    fig = px.imshow(
        pivot,
        title=title,
        labels=dict(x="Ano", y="País", color="HDI"),
        aspect="auto",
        color_continuous_scale="Viridis"
    )
    
    fig.update_layout(height=max(400, len(countries) * 30))
    
    return fig


def plot_hdi_statistics(df: pd.DataFrame,
                       countries: Optional[List[str]] = None,
                       title: str = "Estatísticas Descritivas do HDI") -> go.Figure:
    """
    Cria gráfico com estatísticas descritivas (média, mediana, etc)
    
    Args:
        df: DataFrame com dados do HDI
        countries: Lista de países para filtrar (None = todos)
        title: Título do gráfico
        
    Returns:
        Figura Plotly
    """
    df_plot = df.copy()
    
    if countries:
        df_plot = df_plot[df_plot["Entity"].isin(countries)]
    
    # Calcular estatísticas por ano
    stats = df_plot.groupby("Year")["Human Development Index"].agg([
        "mean", "median", "std", "min", "max"
    ]).reset_index()
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=stats["Year"],
        y=stats["mean"],
        name="Média",
        mode="lines+markers",
        line=dict(color="blue", width=2)
    ))
    
    fig.add_trace(go.Scatter(
        x=stats["Year"],
        y=stats["median"],
        name="Mediana",
        mode="lines+markers",
        line=dict(color="green", width=2)
    ))
    
    fig.add_trace(go.Scatter(
        x=stats["Year"],
        y=stats["min"],
        name="Mínimo",
        mode="lines+markers",
        line=dict(color="red", width=1, dash="dash")
    ))
    
    fig.add_trace(go.Scatter(
        x=stats["Year"],
        y=stats["max"],
        name="Máximo",
        mode="lines+markers",
        line=dict(color="purple", width=1, dash="dash")
    ))
    
    fig.update_layout(
        title=title,
        xaxis_title="Ano",
        yaxis_title="HDI",
        hovermode="x unified",
        height=500
    )
    
    return fig

