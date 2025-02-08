from flask import Flask, request, jsonify
import openai
import os
from dotenv import load_dotenv
from flask_cors import CORS

# Charger les variables d'environnement et configurer la clé API
load_dotenv()
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Historique de conversation avec le message système initial
conversation_history = [
    {"role": "system", "content": "Tu es un expert en cuisine. Tu ne réponds qu'aux questions sur la cuisine."}
]

def est_question_cuisine(user_input):
    """
    Vérifie avec GPT si la question est liée à la cuisine.
    Répond uniquement par 'OUI' ou 'NON' sans explications.
    """
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": (
                    "Tu es un classificateur de questions. Pour chaque question, réponds uniquement par 'OUI' "
                    "si la question concerne la cuisine (cuisine, ingrédients, etc...), ou par 'NON' dans le cas contraire. Ne donne aucune explication."
                )
            },
            {"role": "user", "content": user_input}
        ]
    )
    classification = response.choices[0].message.content.strip().upper()
    print("Classification brute:", classification)  # Ligne de debug pour vérifier la réponse
    return "OUI" in classification

def chatbot_response(user_input):
    """
    Gère la réponse du chatbot :
      - Vérifie si la question concerne la cuisine.
      - Si oui, ajoute le message à l'historique et interroge l'API OpenAI.
      - Sinon, renvoie un message par défaut.
    """
    global conversation_history

    # Vérifier si la question est liée à la cuisine
    if not est_question_cuisine(user_input):
        return "Je ne parle que de cuisine ! Pose-moi une question sur les plats, les recettes ou les ingrédients. 😊"
    
    # Ajouter le message de l'utilisateur à l'historique
    conversation_history.append({"role": "user", "content": user_input})
    
    # Garder le message système et les 10 derniers échanges
    conversation_history = [conversation_history[0]] + conversation_history[-10:]
    
    # Appeler l'API OpenAI pour obtenir la réponse
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=conversation_history
    )
    
    # Extraire la réponse du bot
    bot_reply = response.choices[0].message.content.strip()
    print(bot_reply)  # Ligne de debug pour vérifier la réponse
    
    # Ajouter la réponse à l'historique
    conversation_history.append({"role": "assistant", "content": bot_reply})
    
    return bot_reply

# Initialisation de l'application Flask
app = Flask(__name__)
CORS(app)  # Autoriser les requêtes cross-origin

@app.route('/chat', methods=['POST'])
def chat_endpoint():
    data = request.get_json()
    if not data or 'message' not in data:
        return jsonify({"error": "Message non fourni"}), 400

    user_input = data['message']
    answer = chatbot_response(user_input)
    return jsonify({"response": answer})

if __name__ == '__main__':
    app.run(debug=True)
