import openai
import os

def validate_openai_key(api_key):
    """Validate the OpenAI API key by making a test request."""
    try:
        client = openai.Client(api_key=api_key)  # Use Client instance
        client.models.list()  # Making a request to check key validity
        os.environ["OPENAI_API_KEY"] = api_key
        return "Valid API Key!"
    except openai.AuthenticationError:
        return "Invalid API Key! Authentication failed."
    except openai.APIConnectionError:
        return "API Connection Error! Check your network."
    except Exception as e:
        return f"Error: {str(e)}"