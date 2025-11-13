"""
Sistema RAG (Retrieval-Augmented Generation) educacional
Demonstra como funciona busca semântica e recuperação de contexto
"""
import pickle
from pathlib import Path
from typing import List, Dict, Tuple
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import json

from src.config import RAG_CONFIG, DATABASE_DIR, DOCS_DIR


class RAGSystem:
    """
    Sistema RAG educacional para buscar informações sobre os datasets
    """
    
    def __init__(self):
        """Inicializa o sistema RAG"""
        self.model = SentenceTransformer(RAG_CONFIG["model_name"])
        self.knowledge_base = []
        self.embeddings = None
        self._load_or_create_knowledge_base()
    
    def _load_or_create_knowledge_base(self):
        """Carrega ou cria a base de conhecimento"""
        # Tentar carregar embeddings salvos
        if RAG_CONFIG["embeddings_cache_file"].exists():
            try:
                with open(RAG_CONFIG["embeddings_cache_file"], "rb") as f:
                    cache = pickle.load(f)
                    self.knowledge_base = cache["knowledge_base"]
                    self.embeddings = cache["embeddings"]
                return
            except Exception as e:
                print(f"Erro ao carregar cache: {e}. Recriando base de conhecimento...")
        
        # Criar base de conhecimento
        self._build_knowledge_base()
        self._save_embeddings()
    
    def _build_knowledge_base(self):
        """Constrói a base de conhecimento a partir dos metadados e documentação"""
        documents = []
        
        # Carregar metadados do HDI
        metadata_file = DATABASE_DIR / "human-development-index.metadata.json"
        if metadata_file.exists():
            with open(metadata_file, "r", encoding="utf-8") as f:
                metadata = json.load(f)
            
            # Extrair informações sobre o HDI
            hdi_info = metadata.get("columns", {}).get("Human Development Index", {})
            
            # Adicionar descrição principal
            if "descriptionShort" in hdi_info:
                documents.append({
                    "text": hdi_info["descriptionShort"],
                    "source": "Metadados HDI - Descrição",
                    "type": "description"
                })
            
            # Adicionar descrições detalhadas
            if "descriptionKey" in hdi_info:
                for desc in hdi_info["descriptionKey"]:
                    documents.append({
                        "text": desc,
                        "source": "Metadados HDI - Detalhes",
                        "type": "methodology"
                    })
            
            # Adicionar informações sobre citação
            if "citationShort" in hdi_info:
                documents.append({
                    "text": f"Fonte dos dados: {hdi_info['citationShort']}",
                    "source": "Metadados HDI - Citação",
                    "type": "citation"
                })
            
            # Adicionar informações sobre período
            if "timespan" in hdi_info:
                documents.append({
                    "text": f"Período dos dados: {hdi_info['timespan']}. Última atualização: {hdi_info.get('lastUpdated', 'N/A')}",
                    "source": "Metadados HDI - Período",
                    "type": "metadata"
                })
        
        # Carregar readme.md
        readme_file = DATABASE_DIR / "readme.md"
        if readme_file.exists():
            with open(readme_file, "r", encoding="utf-8") as f:
                readme_content = f.read()
            
            # Dividir readme em seções menores
            sections = readme_content.split("\n## ")
            for i, section in enumerate(sections):
                if section.strip():
                    documents.append({
                        "text": section.strip(),
                        "source": f"README.md - Seção {i+1}",
                        "type": "documentation"
                    })
        
        # Adicionar informações sobre estrutura dos dados
        documents.append({
            "text": "O dataset contém colunas: Entity (nome do país/entidade), Code (código ISO), Year (ano), Human Development Index (valor do HDI de 0 a 1), World regions according to OWID (região geográfica).",
            "source": "Estrutura de Dados",
            "type": "structure"
        })
        
        # Adicionar explicação sobre o que é HDI
        documents.append({
            "text": "O Índice de Desenvolvimento Humano (HDI) é uma medida resumida de dimensões-chave do desenvolvimento humano: uma vida longa e saudável, uma boa educação e um padrão de vida decente. Valores mais altos indicam maior desenvolvimento humano. O HDI varia de 0 a 1.",
            "source": "Definição HDI",
            "type": "definition"
        })
        
        # Adicionar informações sobre metodologia
        documents.append({
            "text": "O HDI é calculado como a média geométrica de três índices: Índice de Expectativa de Vida (baseado na expectativa de vida ao nascer), Índice de Educação (baseado em anos esperados e médios de escolaridade) e Índice de Renda Nacional Bruta (baseado no RNB per capita em PPP$).",
            "source": "Metodologia HDI",
            "type": "methodology"
        })
        
        self.knowledge_base = documents
        
        # Gerar embeddings para todos os documentos
        texts = [doc["text"] for doc in documents]
        self.embeddings = self.model.encode(texts, show_progress_bar=False)
    
    def _save_embeddings(self):
        """Salva os embeddings em cache"""
        cache = {
            "knowledge_base": self.knowledge_base,
            "embeddings": self.embeddings
        }
        with open(RAG_CONFIG["embeddings_cache_file"], "wb") as f:
            pickle.dump(cache, f)
    
    def search(self, query: str, top_k: int = None) -> List[Dict]:
        """
        Busca documentos relevantes para uma query
        
        Args:
            query: Texto da pergunta/busca
            top_k: Número de documentos a retornar (usa config padrão se None)
            
        Returns:
            Lista de documentos com scores de similaridade
        """
        if top_k is None:
            top_k = RAG_CONFIG["top_k"]
        
        # Gerar embedding da query
        query_embedding = self.model.encode([query], show_progress_bar=False)
        
        # Calcular similaridade de cosseno
        similarities = cosine_similarity(query_embedding, self.embeddings)[0]
        
        # Obter top_k documentos mais relevantes
        top_indices = np.argsort(similarities)[::-1][:top_k]
        
        # Filtrar por threshold mínimo
        results = []
        for idx in top_indices:
            score = float(similarities[idx])
            if score >= RAG_CONFIG["similarity_threshold"]:
                result = self.knowledge_base[idx].copy()
                result["similarity_score"] = score
                result["rank"] = len(results) + 1
                results.append(result)
        
        return results
    
    def get_query_embedding(self, query: str) -> np.ndarray:
        """
        Retorna o embedding de uma query (para visualização educacional)
        
        Args:
            query: Texto da query
            
        Returns:
            Array numpy com o embedding
        """
        return self.model.encode([query], show_progress_bar=False)[0]
    
    def explain_rag_process(self, query: str) -> Dict:
        """
        Explica o processo RAG passo a passo (para fins educacionais)
        
        Args:
            query: Texto da query
            
        Returns:
            Dicionário com informações sobre cada etapa do processo
        """
        query_embedding = self.get_query_embedding(query)
        results = self.search(query)
        
        return {
            "query": query,
            "query_embedding": query_embedding,
            "embedding_dimension": len(query_embedding),
            "knowledge_base_size": len(self.knowledge_base),
            "results": results,
            "process_steps": [
                {
                    "step": 1,
                    "name": "Query de Entrada",
                    "description": f"O usuário faz a pergunta: '{query}'"
                },
                {
                    "step": 2,
                    "name": "Geração de Embedding",
                    "description": f"A query é convertida em um vetor numérico de {len(query_embedding)} dimensões usando o modelo {RAG_CONFIG['model_name']}"
                },
                {
                    "step": 3,
                    "name": "Busca Semântica",
                    "description": f"O vetor da query é comparado com {len(self.knowledge_base)} documentos na base de conhecimento usando similaridade de cosseno"
                },
                {
                    "step": 4,
                    "name": "Retrieval (Recuperação)",
                    "description": f"Foram encontrados {len(results)} documentos relevantes acima do threshold de {RAG_CONFIG['similarity_threshold']}"
                },
                {
                    "step": 5,
                    "name": "Contexto para Resposta",
                    "description": "Os documentos mais relevantes são usados como contexto para gerar uma resposta precisa, evitando alucinações"
                }
            ]
        }

