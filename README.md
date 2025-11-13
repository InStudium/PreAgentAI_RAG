# Dashboard Educacional Our World in Data com RAG

Dashboard interativo em Streamlit para visualização de dados estatísticos do [Our World in Data](https://ourworldindata.org/), incluindo uma camada RAG (Retrieval-Augmented Generation) educacional que demonstra como o método funciona para evitar alucinações de IA.

## 🌍 Sobre o Projeto

Este projeto foi desenvolvido para fins educacionais, demonstrando:

1. **Visualização de Dados**: Como criar dashboards interativos com Streamlit e Plotly
2. **Sistema RAG**: Como implementar Retrieval-Augmented Generation na prática
3. **Evitar Alucinações**: Como RAG garante respostas baseadas em dados reais

## 📊 Dataset Atual

- **Human Development Index (HDI)**: Índice de Desenvolvimento Humano
  - Fonte: UNDP, Human Development Report (2025)
  - Processamento: Our World in Data
  - Período: 1990-2023
  - Países: ~200 países e regiões

## 🚀 Instalação

### Pré-requisitos

- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)

### Passos

1. **Clone o repositório** (ou baixe os arquivos)

2. **Instale as dependências**:
```bash
pip install -r requirements.txt
```

3. **Execute a aplicação**:
```bash
streamlit run app.py
```

4. **Acesse no navegador**:
   - O Streamlit abrirá automaticamente em `http://localhost:8501`

## 📁 Estrutura do Projeto

```
├── app.py                      # Aplicação principal Streamlit
├── requirements.txt            # Dependências do projeto
├── README.md                   # Este arquivo
├── .gitignore                  # Arquivos ignorados pelo Git
├── Fonte_dados.txt            # Informações sobre a fonte dos dados
│
├── Database/                   # Datasets
│   ├── human-development-index.csv
│   ├── human-development-index.metadata.json
│   └── readme.md
│
├── src/                        # Módulos do projeto
│   ├── __init__.py
│   ├── config.py              # Configurações centralizadas
│   ├── data_loader.py         # Carregamento e processamento de dados
│   ├── rag_system.py          # Sistema RAG educacional
│   └── visualizations.py      # Funções de visualização
│
├── embeddings/                 # Cache de embeddings (gerado automaticamente)
│   └── knowledge_base_embeddings.pkl
│
└── docs/                       # Documentação educacional
    └── RAG_EXPLANATION.md     # Explicação detalhada sobre RAG
```

## 🎯 Funcionalidades

### 📊 Visualizações Interativas

- **Evolução Temporal**: Gráfico de linha mostrando evolução do HDI por país
- **Comparação entre Países**: Gráfico de barras comparando HDI em um ano específico
- **Heatmap**: Visualização de HDI por país e ano
- **Estatísticas Descritivas**: Média, mediana, mínimo, máximo ao longo do tempo

**Filtros disponíveis:**
- Seleção de países (múltipla escolha)
- Range de anos (1990-2023)
- Filtros por região

### 🤖 Sistema RAG Educacional

- **Busca Semântica**: Faça perguntas sobre os dados em linguagem natural
- **Processo Transparente**: Veja cada etapa do processo RAG
- **Documentos Recuperados**: Visualize quais documentos foram encontrados e seus scores
- **Respostas Baseadas em Contexto**: Respostas geradas apenas com informações verificadas

**Exemplos de perguntas:**
- "O que é o HDI?"
- "Como o HDI é calculado?"
- "Qual é a fonte dos dados?"
- "Qual é o período dos dados disponíveis?"

## 🔧 Tecnologias Utilizadas

- **Streamlit**: Framework para criação de dashboards web
- **Pandas**: Manipulação e análise de dados
- **Plotly**: Visualizações interativas
- **Sentence Transformers**: Modelos para geração de embeddings semânticos
- **Scikit-learn**: Cálculo de similaridade de cosseno
- **NumPy**: Operações numéricas

## 📚 Entendendo o RAG

O sistema RAG implementado demonstra:

1. **Preparação da Base de Conhecimento**: Criação de embeddings a partir de metadados e documentação
2. **Busca Semântica**: Comparação de similaridade entre query e documentos
3. **Recuperação**: Seleção dos documentos mais relevantes
4. **Geração de Resposta**: Resposta baseada apenas no contexto recuperado

Para mais detalhes, consulte: [`docs/RAG_EXPLANATION.md`](docs/RAG_EXPLANATION.md)

## 🎓 Objetivos Educacionais

Este projeto foi desenvolvido para:

- Demonstrar visualizações interativas de dados estatísticos
- Ensinar como implementar um sistema RAG básico
- Mostrar como RAG evita alucinações em sistemas de IA
- Fornecer uma base para projetos futuros com múltiplos datasets

## 🔮 Próximos Passos

- [ ] Adicionar mais datasets do Our World in Data
- [ ] Expandir a base de conhecimento do RAG
- [ ] Adicionar mais tipos de visualizações (mapas mundiais, etc.)
- [ ] Implementar comparações entre diferentes indicadores
- [ ] Adicionar exportação de dados e gráficos

## 📝 Licença

Este projeto é para fins educacionais. Os dados são de:
- **Our World in Data**: [ourworldindata.org](https://ourworldindata.org/)
- **Fonte Original**: UNDP, Human Development Report (2025)

## 🤝 Contribuindo

Este é um projeto educacional. Sugestões e melhorias são bem-vindas!

## 📧 Contato

Para dúvidas ou sugestões sobre este projeto educacional, consulte a documentação ou abra uma issue no repositório.

---

**Desenvolvido para fins educacionais** | **Turma - Inovação_IA_DS_BD_Negócios - Nov25**

