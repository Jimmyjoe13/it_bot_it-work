import os
from dotenv import load_dotenv
from groq import Groq

# Charger les variables d'environnement
load_dotenv()

class Chatbot:
    def __init__(self):
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        self.conversation_history = []
        self.model = "mixtral-8x7b-32768"
        self.max_history = 5

    def generate_system_prompt(self):
        return """Tu es un assistant virtuel français intelligent et serviable. 
        Tu fournis des réponses précises, pertinentes et utiles tout en maintenant 
        un ton professionnel et amical. Tu es capable de traiter divers sujets 
        et de fournir des informations détaillées tout en restant concis."""

    def format_conversation_history(self):
        formatted_history = self.generate_system_prompt() + "\n\n"
        for message in self.conversation_history[-self.max_history:]:
            role = "Assistant" if message["role"] == "assistant" else "Utilisateur"
            formatted_history += f"{role}: {message['content']}\n"
        return formatted_history

    async def get_response(self, user_input: str) -> str:
        # Ajouter le message de l'utilisateur à l'historique
        self.conversation_history.append({"role": "user", "content": user_input})
        
        try:
            # Préparer le contexte complet de la conversation
            conversation_context = self.format_conversation_history()
            
            # Appeler l'API Groq
            completion = self.client.chat.completions.create(
                messages=[
                    {"role": "system", "content": self.generate_system_prompt()},
                    {"role": "user", "content": conversation_context + "\nUtilisateur: " + user_input}
                ],
                model=self.model,
                temperature=0.7,
                max_tokens=1000,
                top_p=0.9,
            )

            # Extraire la réponse
            response = completion.choices[0].message.content
            
            # Ajouter la réponse à l'historique
            self.conversation_history.append({"role": "assistant", "content": response})
            
            return response

        except Exception as e:
            error_message = f"Une erreur est survenue : {str(e)}"
            return error_message

    def clear_history(self):
        """Effacer l'historique de la conversation"""
        self.conversation_history = []
