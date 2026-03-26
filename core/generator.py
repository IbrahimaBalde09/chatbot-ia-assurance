from openai import OpenAI

from core.config import OPENAI_API_KEY, LLM_MODEL
from core.prompts import SYSTEM_PROMPT


class ResponseGenerator:
    def __init__(self):
        self.client = OpenAI(api_key=OPENAI_API_KEY)
        self.model = LLM_MODEL

    def generate(self, query: str, contexts: list[dict]) -> str:
        context_text = "\n\n".join(
            [
                f"Source: {doc['source']}\nContenu: {doc['text']}"
                for doc in contexts
            ]
        )

        user_prompt = f"""
Question utilisateur :
{query}

Contexte :
{context_text}

Consignes :
- Réponds uniquement avec les informations du contexte
- Sois clair, structuré et professionnel
- Si tu ne sais pas, dis-le
"""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.2,
        )

        return response.choices[0].message.content