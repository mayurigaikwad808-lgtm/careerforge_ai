from groq import Groq
from backend.config.settings import GROQ_API_KEY


client = Groq(api_key=GROQ_API_KEY)

models = client.models.list()

print("\nModels available to your API key:\n")

for model in models.data:
    print(model.id)