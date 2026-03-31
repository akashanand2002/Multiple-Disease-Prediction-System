import requests


def get_response(user_input):

    try:

        url = "http://localhost:11434/api/generate"

        payload = {
            "model": "llama3.2:3b",
            "prompt": f"You are a medical assistant. Answer clearly: {user_input}",
            "stream": False,
            "options": {
                "temperature": 0.3,
                "num_predict": 200
            }
        }

        response = requests.post(
            url,
            json=payload,
            timeout=300
        )

        if response.status_code == 200:

            data = response.json()

            return data.get(
                "response",
                "No response from model"
            )

        else:

            return f"Error: {response.status_code}"

    except Exception as e:

        print("ERROR:", e)

        return "AI model is slow. Try again."
