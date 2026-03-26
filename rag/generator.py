from openai import OpenAI

from rag.config import OPENAI_API_KEY, LLM_MODEL
from rag.prompts import SYSTEM_PROMPT


class ResponseGenerator:
    def __init__(self):
        self.client = OpenAI(api_key=OPENAI_API_KEY)
        self.model = LLM_MODEL

    def generate_with_context(self, query: str, contexts: list[dict], domain: str) -> str:
        context_text = "\n\n".join(
            [
                f"Source: {doc['source']}\n"
                f"Domaine: {doc.get('domain', 'general')}\n"
                f"Pertinence: {doc.get('score', 0):.3f}\n"
                f"Contenu: {doc['text']}"
                for doc in contexts
            ]
        )

        user_prompt = f"""
Question utilisateur :
{query}

Domaine détecté :
{domain}

Contexte documentaire :
{context_text}

Consignes :
- Réponds d'abord à partir du contexte.
- Si le contexte est partiel, complète uniquement avec des connaissances générales prudentes.
- Si une réponse dépend des clauses du contrat, précise-le.
- Termine par :
Sources : <liste des fichiers utilisés>
"""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.1,
        )

        return response.choices[0].message.content.strip()

    def generate_general(self, query: str, domain: str) -> str:
        user_prompt = f"""
Question utilisateur :
{query}

Domaine détecté :
{domain}

Consignes :
- Donne une réponse générale, fiable et pédagogique.
- N'invente pas de détails contractuels précis.
- Si la réponse dépend du contrat, de la banque ou de l'assureur, indique-le.
- Structure la réponse clairement.
- Termine par :
Sources : réponse générale (sans base documentaire suffisante)
"""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.2,
        )

        return response.choices[0].message.content.strip()