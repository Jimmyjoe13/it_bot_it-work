import os
import logging
import asyncio
from datetime import datetime
from typing import List, Dict, Optional
from dotenv import load_dotenv
from groq import Groq
from knowledge_base import KnowledgeBase

class Chatbot:
    def __init__(self):
        # Chargement de la clé API depuis les variables d'environnement
        load_dotenv()
        self.groq_client = Groq(api_key=os.getenv('GROQ_API_KEY'))
        
        # Initialisation de la base de connaissances
        self.knowledge_base = KnowledgeBase()
        
        # Configuration du système de prompt
        self.system_prompt = """Tu es l'assistant virtuel d'IT-Work, une entreprise de services informatiques basée en France. 
        
Ton rôle est d'être :
- Chaleureux et empathique : Montre une véritable compréhension des besoins
- Naturel et décontracté : Parle comme un vrai conseiller, pas comme un robot
- Proactif et attentif : Anticipe les besoins et propose des solutions adaptées
- Concis et pertinent : Va droit au but tout en restant aimable

Style de communication :
1. Utilise un langage simple et accessible
2. Évite le jargon technique sauf si nécessaire
3. Sois conversationnel et dynamique
4. Montre de l'enthousiasme et de l'intérêt
5. Crée une connexion personnelle avec l'utilisateur

Important :
- Ne cite pas explicitement tes sources, intègre naturellement les informations
- Évite les formules toutes faites ou trop commerciales
- Adapte ton niveau de langage à celui de l'utilisateur
- Si tu proposes un lien, fais-le de manière naturelle dans la conversation
- Reste honnête : si tu ne sais pas, dis-le simplement

Ta mission est d'être un véritable partenaire de confiance, comme un collègue bienveillant qui connaît bien IT-Work."""

        # Initialisation de l'historique des conversations
        self.conversation_history = []
        self.max_history = 5  # Nombre maximum de messages dans l'historique
        
        self.setup_logging()

    def setup_logging(self):
        self.logger = logging.getLogger('Chatbot')
        self.logger.setLevel(logging.INFO)
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)

    def prepare_context(self, user_input: str) -> str:
        """Prépare le contexte pour la réponse en recherchant les informations pertinentes"""
        try:
            # Recherche d'informations pertinentes
            relevant_content = self.knowledge_base.search_knowledge(user_input, k=3)
            
            # Si la question semble porter sur les contacts
            contact_keywords = ['contact', 'téléphone', 'email', 'adresse', 'joindre', 'appeler']
            if any(keyword in user_input.lower() for keyword in contact_keywords):
                contact_info = self.knowledge_base.get_contact_info()
                context = "Voici les informations de contact d'IT-Work :\n"
                if contact_info['phone']:
                    context += f"Téléphone : {', '.join(contact_info['phone'])}\n"
                if contact_info['email']:
                    context += f"Email : {', '.join(contact_info['email'])}\n"
                if contact_info['address']:
                    context += f"Adresse : {', '.join(contact_info['address'])}\n"
                if contact_info['social_media']:
                    context += "Réseaux sociaux :\n"
                    for platform, url in contact_info['social_media'].items():
                        context += f"- {platform.capitalize()} : {url}\n"
                return context

            # Formater les résultats de recherche
            return self.knowledge_base.format_knowledge_response(relevant_content)

        except Exception as e:
            self.logger.error(f"Erreur lors de la préparation du contexte : {str(e)}")
            return ""

    def add_to_history(self, role: str, content: str):
        """Ajoute un message à l'historique des conversations"""
        self.conversation_history.append({
            'role': role,
            'content': content,
            'timestamp': datetime.now().isoformat()
        })
        
        # Garder uniquement les derniers messages
        if len(self.conversation_history) > self.max_history * 2:  # *2 car on compte les paires Q/R
            self.conversation_history = self.conversation_history[-self.max_history * 2:]

    def format_conversation_history(self) -> List[Dict[str, str]]:
        """Formate l'historique de conversation pour l'API Groq"""
        formatted_history = []
        for msg in self.conversation_history:
            formatted_history.append({
                'role': msg['role'],
                'content': msg['content']
            })
        return formatted_history

    def clear_history(self):
        """Efface l'historique des conversations"""
        self.conversation_history = []
        self.logger.info("Historique des conversations effacé")

    async def get_response(self, user_input: str) -> str:
        """Génère une réponse à l'entrée utilisateur"""
        try:
            # Préparation du contexte
            context = self.prepare_context(user_input)
            
            # Détection des besoins
            detected_needs = self.knowledge_base.detect_needs(user_input)
            
            # Construction du prompt avec contexte masqué
            prompt = f"""Question de l'utilisateur : {user_input}

Information contexte :
{context}

Instructions spéciales :
- Utilise les informations du contexte de manière naturelle, sans les citer
- Si des liens sont pertinents, intègre-les subtilement dans la conversation
- Reste décontracté et amical dans ta réponse
- Concentre-toi sur l'aide concrète plutôt que sur les détails techniques"""

            # Ajout du message utilisateur à l'historique
            self.add_to_history('user', user_input)

            # Appel à l'API Groq dans une coroutine séparée
            loop = asyncio.get_event_loop()
            chat_completion = await loop.run_in_executor(
                None,
                lambda: self.groq_client.chat.completions.create(
                    messages=[
                        {"role": "system", "content": self.system_prompt},
                        *self.format_conversation_history(),
                        {"role": "user", "content": prompt}
                    ],
                    model="mixtral-8x7b-32768",
                    temperature=0.8,  # Légèrement augmenté pour plus de naturel
                    max_tokens=1024
                )
            )

            # Récupération de la réponse
            response = chat_completion.choices[0].message.content

            # Ajout de la réponse à l'historique
            self.add_to_history('assistant', response)
            return response

        except Exception as e:
            self.logger.error(f"Erreur lors de la génération de la réponse : {str(e)}")
            return "Désolé, j'ai un petit souci technique. On peut réessayer ?"
