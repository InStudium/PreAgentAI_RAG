"""
Dashboard Educacional Our World in Data com RAG
Aplicação Streamlit principal
"""
import streamlit as st
import pandas as pd
from src.data_loader import (
    load_dataset, clean_hdi_data, get_available_countries,
    get_available_years, filter_data
)
from src.rag_system import RAGSystem
from src.visualizations import (
    plot_hdi_timeline, plot_hdi_comparison,
    plot_hdi_heatmap, plot_hdi_statistics
)
from src.config import VIZ_CONFIG

# Configuração da página
st.set_page_config(
    page_title="Dashboard Our World in Data",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inicializar sistema RAG (com cache)
@st.cache_resource
def init_rag_system():
    """Inicializa o sistema RAG (cacheado para performance)"""
    return RAGSystem()

# Carregar dados (com cache)
@st.cache_data
def load_data():
    """Carrega e limpa os dados do HDI"""
    df, metadata = load_dataset("hdi")
    df_clean = clean_hdi_data(df)
    return df_clean, metadata

# Carregar dados
df, metadata = load_data()
rag_system = init_rag_system()

# Sidebar
st.sidebar.title("🌍 Dashboard Our World in Data")
st.sidebar.markdown("---")

# Menu de navegação
page = st.sidebar.radio(
    "Navegação",
    ["📊 Visualizações", "🤖 Sistema RAG", "ℹ️ Sobre"]
)

# Página: Visualizações
if page == "📊 Visualizações":
    st.title("📊 Visualizações Interativas - Human Development Index")
    
    st.markdown("""
    Explore os dados do Índice de Desenvolvimento Humano (HDI) através de visualizações interativas.
    Use os filtros na barra lateral para personalizar suas análises.
    """)
    
    # Filtros na sidebar
    st.sidebar.header("Filtros")
    
    # Filtro de países
    available_countries = get_available_countries(df)
    selected_countries = st.sidebar.multiselect(
        "Selecione países",
        options=available_countries,
        default=VIZ_CONFIG["default_countries"]
    )
    
    # Filtro de anos
    min_year, max_year = get_available_years(df)
    year_range = st.sidebar.slider(
        "Selecione o período",
        min_value=min_year,
        max_value=max_year,
        value=(min_year, max_year)
    )
    
    # Aplicar filtros
    df_filtered = filter_data(
        df,
        countries=selected_countries if selected_countries else None,
        years=year_range
    )
    
    # Tabs para diferentes visualizações
    tab1, tab2, tab3, tab4 = st.tabs([
        "📈 Evolução Temporal",
        "🏆 Comparação entre Países",
        "🔥 Heatmap",
        "📊 Estatísticas"
    ])
    
    with tab1:
        st.subheader("Evolução do HDI ao Longo do Tempo")
        if not df_filtered.empty:
            fig = plot_hdi_timeline(df_filtered, selected_countries)
            st.plotly_chart(fig, use_container_width=True)
            
            # Estatísticas rápidas
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Países Selecionados", len(selected_countries) if selected_countries else len(available_countries))
            with col2:
                st.metric("Período", f"{year_range[0]}-{year_range[1]}")
            with col3:
                st.metric("HDI Médio", f"{df_filtered['Human Development Index'].mean():.3f}")
            with col4:
                st.metric("HDI Máximo", f"{df_filtered['Human Development Index'].max():.3f}")
        else:
            st.warning("Selecione pelo menos um país para visualizar os dados.")
    
    with tab2:
        st.subheader("Comparação de HDI entre Países")
        comparison_year = st.selectbox(
            "Selecione o ano para comparação",
            options=range(year_range[0], year_range[1] + 1),
            index=len(range(year_range[0], year_range[1] + 1)) - 1
        )
        
        top_n = st.slider("Número de países a mostrar", 5, 50, 20)
        
        if comparison_year:
            fig = plot_hdi_comparison(df_filtered, comparison_year, top_n)
            st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        st.subheader("Heatmap de HDI por País e Ano")
        if selected_countries:
            max_countries = min(len(selected_countries), 15)
            heatmap_countries = st.multiselect(
                "Selecione países para o heatmap (máx 15)",
                options=selected_countries,
                default=selected_countries[:max_countries]
            )
            
            if heatmap_countries:
                fig = plot_hdi_heatmap(df_filtered, heatmap_countries)
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Selecione países nos filtros para visualizar o heatmap.")
    
    with tab4:
        st.subheader("Estatísticas Descritivas do HDI")
        if not df_filtered.empty:
            fig = plot_hdi_statistics(df_filtered, selected_countries)
            st.plotly_chart(fig, use_container_width=True)
            
            # Tabela com estatísticas detalhadas
            st.subheader("Estatísticas Detalhadas")
            stats_df = df_filtered.groupby("Entity")["Human Development Index"].agg([
                "mean", "std", "min", "max", "count"
            ]).round(3)
            stats_df.columns = ["Média", "Desvio Padrão", "Mínimo", "Máximo", "Observações"]
            st.dataframe(stats_df, use_container_width=True)
        else:
            st.warning("Selecione países para visualizar as estatísticas.")

# Página: Sistema RAG
elif page == "🤖 Sistema RAG":
    st.title("🤖 Sistema RAG - Demonstração Educacional")
    
    st.markdown("""
    ## O que é RAG?
    
    **RAG (Retrieval-Augmented Generation)** é uma técnica que combina busca de informações com geração de respostas.
    O sistema busca informações relevantes em uma base de conhecimento antes de responder, evitando alucinações
    e garantindo respostas baseadas em dados reais.
    """)
    
    # Seção de busca
    st.header("🔍 Faça uma Pergunta sobre os Dados")
    
    # Exemplos de perguntas
    example_questions = [
        "O que é o HDI?",
        "Como o HDI é calculado?",
        "Qual é a fonte dos dados?",
        "Qual é o período dos dados disponíveis?",
        "Quais são as dimensões do desenvolvimento humano?",
        "O que significa expectativa de vida no HDI?"
    ]
    
    selected_example = st.selectbox(
        "Ou escolha uma pergunta de exemplo:",
        ["-- Selecione uma pergunta de exemplo --"] + example_questions
    )
    
    # Input de query
    if selected_example != "-- Selecione uma pergunta de exemplo --":
        query = st.text_input("Sua pergunta:", value=selected_example)
    else:
        query = st.text_input("Sua pergunta:", placeholder="Ex: O que é o HDI?")
    
    if query:
        # Processar query
        with st.spinner("Processando sua pergunta..."):
            explanation = rag_system.explain_rag_process(query)
        
        # Mostrar processo passo a passo
        st.header("📚 Processo RAG - Passo a Passo")
        
        for step_info in explanation["process_steps"]:
            with st.expander(f"Passo {step_info['step']}: {step_info['name']}", expanded=True):
                st.write(step_info["description"])
        
        # Mostrar resultados
        st.header("📄 Documentos Encontrados")
        
        if explanation["results"]:
            for result in explanation["results"]:
                with st.expander(
                    f"📌 Documento #{result['rank']} - Score: {result['similarity_score']:.3f} - {result['source']}",
                    expanded=result['rank'] == 1
                ):
                    st.write(f"**Tipo:** {result['type']}")
                    st.write(f"**Fonte:** {result['source']}")
                    st.write(f"**Similaridade:** {result['similarity_score']:.3f}")
                    st.markdown("---")
                    st.write(result["text"])
            
            # Resposta baseada no contexto
            st.header("💡 Resposta Baseada no Contexto")
            st.info("""
            **Como funciona:** A resposta é gerada usando APENAS as informações encontradas nos documentos acima.
            Isso garante que a resposta seja precisa e baseada em dados reais, evitando alucinações.
            """)
            
            # Construir resposta simples baseada no contexto
            top_result = explanation["results"][0]
            st.success(f"""
            **Resposta:**
            
            {top_result['text']}
            
            *Fonte: {top_result['source']} (Similaridade: {top_result['similarity_score']:.3f})*
            """)
        else:
            st.warning("Nenhum documento relevante encontrado. Tente reformular sua pergunta.")
        
        # Informações técnicas (colapsável)
        with st.expander("🔧 Informações Técnicas"):
            st.write(f"**Dimensão do Embedding:** {explanation['embedding_dimension']}")
            st.write(f"**Tamanho da Base de Conhecimento:** {explanation['knowledge_base_size']} documentos")
            st.write(f"**Documentos Retornados:** {len(explanation['results'])}")
            
            # Visualizar embedding (primeiras dimensões)
            st.write("**Primeiras 10 dimensões do embedding da query:**")
            st.code(explanation['query_embedding'][:10])
    
    # Seção educacional sobre RAG
    st.markdown("---")
    st.header("📖 Entendendo o RAG")
    
    st.markdown("""
    ### Por que RAG é importante?
    
    1. **Evita Alucinações**: A IA só responde com base em informações verificadas
    2. **Transparência**: Você pode ver exatamente quais documentos foram usados
    3. **Atualização**: A base de conhecimento pode ser atualizada sem retreinar o modelo
    4. **Rastreabilidade**: Cada resposta pode ser rastreada até sua fonte
    
    ### Como funciona neste sistema?
    
    - **Base de Conhecimento**: Criada a partir dos metadados e documentação dos datasets
    - **Embeddings**: Textos convertidos em vetores numéricos usando modelos de linguagem
    - **Busca Semântica**: Comparação de similaridade entre a pergunta e os documentos
    - **Recuperação**: Seleção dos documentos mais relevantes
    - **Resposta**: Geração de resposta baseada apenas no contexto recuperado
    """)

# Página: Sobre
elif page == "ℹ️ Sobre":
    st.title("ℹ️ Sobre o Projeto")
    
    st.markdown("""
    ## Dashboard Educacional Our World in Data com RAG
    
    Este projeto foi desenvolvido para fins educacionais, demonstrando como construir um dashboard
    interativo para visualização de dados estatísticos e como implementar um sistema RAG básico.
    
    ### Objetivos Educacionais
    
    1. **Visualização de Dados**: Aprender a criar visualizações interativas com Streamlit e Plotly
    2. **Sistema RAG**: Entender como funciona Retrieval-Augmented Generation na prática
    3. **Evitar Alucinações**: Demonstrar como RAG garante respostas baseadas em dados reais
    
    ### Tecnologias Utilizadas
    
    - **Streamlit**: Framework para criação de dashboards web
    - **Plotly**: Biblioteca para visualizações interativas
    - **Pandas**: Manipulação e análise de dados
    - **Sentence Transformers**: Modelos para geração de embeddings
    - **Scikit-learn**: Cálculo de similaridade de cosseno
    
    ### Fonte dos Dados
    
    Os dados utilizados são do **Our World in Data**:
    - Dataset: Human Development Index (HDI)
    - Fonte original: UNDP, Human Development Report (2025)
    - Processamento: Our World in Data
    
    ### Estrutura do Projeto
    
    ```
    ├── app.py                 # Aplicação principal Streamlit
    ├── src/
    │   ├── data_loader.py    # Carregamento de dados
    │   ├── rag_system.py     # Sistema RAG
    │   ├── visualizations.py # Funções de visualização
    │   └── config.py         # Configurações
    ├── Database/             # Datasets
    └── docs/                 # Documentação
    ```
    
    ### Como Usar
    
    1. Instale as dependências: `pip install -r requirements.txt`
    2. Execute a aplicação: `streamlit run app.py`
    3. Explore as visualizações e teste o sistema RAG
    
    ### Próximos Passos
    
    - Adicionar mais datasets do Our World in Data
    - Expandir a base de conhecimento do RAG
    - Adicionar mais tipos de visualizações
    - Implementar comparações entre datasets
    """)
    
    # Informações sobre os dados
    st.header("📊 Informações sobre os Dados")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total de Registros", len(df))
        st.metric("Países Únicos", len(get_available_countries(df)))
    
    with col2:
        min_year, max_year = get_available_years(df)
        st.metric("Período", f"{min_year} - {max_year}")
        st.metric("Anos de Dados", max_year - min_year + 1)
    
    # Mostrar amostra dos dados
    st.subheader("Amostra dos Dados")
    st.dataframe(df.head(10), use_container_width=True)

