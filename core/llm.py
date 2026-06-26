import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "qwen2.5:7b"


def ask_llm(prompt):
    payload = {
        "model": MODEL,
        "prompt": prompt,
        "stream": False,
        "options": {
            "num_predict": 300
        }
    }

    try:
        response = requests.post(
            OLLAMA_URL,
            json=payload,
            timeout=120
        )

        if response.status_code != 200:
            return "Erreur : impossible de contacter Ollama."

        return response.json().get("response", "")

    except requests.exceptions.Timeout:
        return "Erreur : Ollama met trop de temps à répondre."

    except requests.exceptions.RequestException as error:
        return f"Erreur : problème de connexion à Ollama ({error})."
