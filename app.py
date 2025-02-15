import gradio as gr
from chatbot import Chatbot
import os

# Initialiser le chatbot
chatbot = Chatbot()

def respond(message, history):
    """Fonction pour gérer les réponses du chatbot"""
    # Obtenir la réponse du chatbot de manière synchrone
    response = chatbot.get_response_sync(message)
    return response

# Créer l'interface Gradio
demo = gr.ChatInterface(
    respond,
    chatbot=gr.Chatbot(
        height=600,
        show_label=False,
        show_share_button=True,
        avatar_images=(
            "static/images/user.png",
            "static/images/bot.png"
        ),
    ),
    title="IT Support Assistant - IT-Work",
    description="Je suis votre assistant IT spécialisé, posez-moi vos questions techniques !",
    theme=gr.themes.Soft(),
    examples=[
        "Comment réinitialiser mon mot de passe Windows ?",
        "Mon ordinateur est lent, que faire ?",
        "Comment configurer une imprimante réseau ?",
        "Que faire si mon écran reste noir ?",
        "Quels sont vos services d'infogérance ?",
        "Comment protéger mon entreprise contre les cyberattaques ?",
    ],
    retry_btn="Réessayer",
    undo_btn="Annuler",
    clear_btn="Effacer la conversation",
)

# Configuration pour Replit
if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=int(os.environ.get("PORT", 8080)))
