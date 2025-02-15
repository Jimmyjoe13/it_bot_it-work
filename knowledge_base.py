import os
import json
import logging
from datetime import datetime
from typing import List, Dict, Optional
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from pathlib import Path

class KnowledgeBase:
    def __init__(self):
        self.setup_logging()
        
        # Configuration du cache local
        cache_dir = Path.home() / '.cache' / 'it-work-chatbot'
        cache_dir.mkdir(parents=True, exist_ok=True)
        
        # Configuration de Hugging Face
        os.environ['TRANSFORMERS_CACHE'] = str(cache_dir)
        os.environ['HF_HOME'] = str(cache_dir)
        
        # Initialisation du modèle d'embedding
        self.model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2',
                                       cache_folder=str(cache_dir))
        
        # Création de l'index FAISS
        self.dimension = 384  # Dimension des embeddings du modèle MiniLM
        self.index = faiss.IndexFlatL2(self.dimension)
        
        # Stockage des données
        self.documents = []
        self.urls = []
        self.contact_info = {}
        self.page_titles = {}
        self.urls_map = {
            "cloud": "https://it-work.fr/cloud/",
            "voip": "https://it-work.fr/voip/",
            "medical": "https://it-work.fr/medical/",
            "retail": "https://it-work.fr/retails/",
            "entreprises": "https://it-work.fr/entreprises/",
            "associations": "https://it-work.fr/associations/",
            "hotellerie": "https://it-work.fr/hotellerie/",
            "reseaux": "https://it-work.fr/reseaux/",
            "contact": "https://it-work.fr/contact/",
            "offres": "https://it-work.fr/nos-offres/",
            "about": "https://it-work.fr/qui-sommes-nous/"
        }
        
        # Mots-clés associés aux besoins
        self.needs_keywords = {
            "cloud": ["cloud", "hébergement", "serveur", "stockage", "sauvegarde", "données"],
            "voip": ["téléphonie", "voip", "communication", "téléphone", "appel"],
            "medical": ["médical", "santé", "cabinet", "clinique", "hôpital"],
            "retail": ["commerce", "magasin", "retail", "boutique", "point de vente"],
            "entreprises": ["entreprise", "société", "business", "pme", "pmi"],
            "associations": ["association", "asso", "non-profit", "but non lucratif"],
            "hotellerie": ["hôtel", "restaurant", "tourisme", "hébergement"],
            "reseaux": ["réseau", "infrastructure", "wifi", "internet", "câblage"],
            "contact": ["contact", "joindre", "appeler", "rendez-vous", "devis"],
            "offres": ["offre", "service", "prix", "tarif", "pack"],
            "about": ["entreprise it-work", "à propos", "qui sommes-nous", "présentation"]
        }
        
        # Chargement des données
        self.load_knowledge()
        self.build_index()

    def setup_logging(self):
        self.logger = logging.getLogger('KnowledgeBase')
        self.logger.setLevel(logging.INFO)
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)

    def load_knowledge(self):
        """Charge toutes les données scrapées dans la base de connaissances"""
        try:
            data_dir = "scraped_data"
            if not os.path.exists(data_dir):
                self.logger.warning("Dossier de données non trouvé")
                return

            for file in os.listdir(data_dir):
                if file.endswith('.json'):
                    file_path = os.path.join(data_dir, file)
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            data = json.load(f)
                            
                            # Stockage des informations de contact
                            if data.get('contact_info'):
                                self.contact_info[data['url']] = data['contact_info']
                            
                            # Stockage des titres de pages
                            if data.get('title'):
                                self.page_titles[data['url']] = data['title']
                            
                            # Traitement du contenu principal
                            content_parts = []
                            
                            # Ajout du titre et de la meta description
                            if data.get('title'):
                                content_parts.append(f"Titre: {data['title']}")
                            if data.get('meta_description'):
                                content_parts.append(f"Description: {data['meta_description']}")
                            
                            # Traitement du contenu principal
                            if data.get('main_content'):
                                for item in data['main_content']:
                                    if isinstance(item, dict):
                                        content_parts.append(item.get('content', ''))
                            
                            # Création du document
                            document = {
                                'content': ' '.join(content_parts),
                                'url': data['url'],
                                'title': data.get('title', ''),
                                'links': data.get('links', []),
                                'contact_info': data.get('contact_info', {})
                            }
                            
                            self.documents.append(document)
                            self.urls.append(data['url'])
                            
                    except Exception as e:
                        self.logger.error(f"Erreur lors du chargement de {file_path}: {str(e)}")
            
            self.logger.info(f"Base de connaissances chargée : {len(self.documents)} documents")
        except Exception as e:
            self.logger.error(f"Erreur lors du chargement de la base de connaissances: {str(e)}")

    def build_index(self):
        """Construit l'index vectoriel des documents"""
        try:
            if not self.documents:
                self.logger.warning("Aucun document à indexer")
                return

            # Création des embeddings pour chaque document
            texts = [doc['content'] for doc in self.documents]
            embeddings = self.model.encode(texts, convert_to_tensor=True)
            embeddings = embeddings.cpu().numpy()

            # Ajout à l'index FAISS
            self.index = faiss.IndexFlatL2(self.dimension)
            self.index.add(embeddings.astype(np.float32))
            self.logger.info(f"Index vectoriel construit avec {len(texts)} documents")

        except Exception as e:
            self.logger.error(f"Erreur lors de la construction de l'index: {str(e)}")
            raise

    def search_knowledge(self, query: str, k: int = 5) -> List[Dict]:
        """
        Recherche les documents les plus pertinents pour une requête donnée
        """
        try:
            # Création de l'embedding de la requête
            query_vector = self.model.encode([query])[0].reshape(1, -1)

            # Recherche des documents les plus proches
            distances, indices = self.index.search(query_vector.astype(np.float32), k=k)
            
            relevant_content = []
            for idx, distance in zip(indices[0], distances[0]):
                if idx >= 0 and idx < len(self.documents):
                    doc = self.documents[idx]
                    
                    # Calcul du score de pertinence (0 à 100)
                    relevance_score = max(0, min(100, (1 - distance/10) * 100))
                    
                    # Ne garder que les résultats suffisamment pertinents
                    if relevance_score >= 30:
                        result = {
                            'content': doc['content'],
                            'url': doc['url'],
                            'title': doc['title'],
                            'relevance_score': relevance_score,
                            'links': doc.get('links', []),
                            'contact_info': doc.get('contact_info', {})
                        }
                        relevant_content.append(result)

            return relevant_content

        except Exception as e:
            self.logger.error(f"Erreur lors de la recherche: {str(e)}")
            return []

    def get_contact_info(self) -> Dict[str, List[str]]:
        """Récupère les informations de contact depuis le fichier contact_info.json"""
        try:
            contact_file = os.path.join('scraped_data', 'contact_info.json')
            if os.path.exists(contact_file):
                with open(contact_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                self.logger.warning("Fichier contact_info.json non trouvé")
                return {"phone": [], "email": [], "address": [], "social_media": []}
        except Exception as e:
            self.logger.error(f"Erreur lors de la lecture des informations de contact : {e}")
            return {"phone": [], "email": [], "address": [], "social_media": []}

    def format_knowledge_response(self, relevant_content: List[Dict]) -> str:
        """Formate les résultats de recherche en une réponse structurée"""
        if not relevant_content:
            return "Je n'ai pas trouvé d'information pertinente pour votre demande."

        response_parts = []
        
        for item in sorted(relevant_content, key=lambda x: x['relevance_score'], reverse=True):
            response_parts.append(f"\nSource: {item['title']} ({item['url']})")
            response_parts.append(f"Contenu pertinent: {item['content'][:500]}...")
            
            # Ajout des liens pertinents
            if item['links']:
                response_parts.append("\nLiens utiles:")
                for link in item['links'][:3]:  # Limiter à 3 liens
                    response_parts.append(f"- {link['text']}: {link['url']}")
            
            # Ajout des informations de contact si présentes
            if item['contact_info']:
                response_parts.append("\nInformations de contact:")
                if item['contact_info'].get('phone'):
                    response_parts.append(f"Téléphone: {', '.join(item['contact_info']['phone'])}")
                if item['contact_info'].get('email'):
                    response_parts.append(f"Email: {', '.join(item['contact_info']['email'])}")

        return "\n".join(response_parts)

    def detect_needs(self, text: str) -> List[Dict[str, str]]:
        """Détecte les besoins dans le texte et retourne les liens pertinents"""
        text = text.lower()
        detected_needs = []
        
        for need, keywords in self.needs_keywords.items():
            if any(keyword in text for keyword in keywords):
                detected_needs.append({
                    "type": need,
                    "url": self.urls_map[need]
                })
        
        return detected_needs
