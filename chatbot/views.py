import os
import json
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt


def home(request):
    return render(request, "chatbot/index.html")


@csrf_exempt
def chat(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST request required"}, status=400)

    try:
        data = json.loads(request.body)
        message = data.get("message", "").strip()
        history = data.get("history", [])

        if not message:
            return JsonResponse({"error": "Message vide"}, status=400)

        from openai import OpenAI

        client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

        messages = [
            {
                "role": "system",
                "content": (
                    "Tu es un assistant expert en assurance. "
                    "Réponds en français, de façon claire, utile et concise. "
                    "Quand une information dépend du contrat, précise qu'il faut vérifier les garanties exactes."
                ),
            }
        ]

        # On garde seulement les derniers échanges pour éviter des requêtes trop lourdes
        for item in history[-10:]:
            role = item.get("role")
            content = item.get("content", "").strip()
            if role in ["user", "assistant"] and content:
                messages.append({"role": role, "content": content})

        messages.append({"role": "user", "content": message})

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            temperature=0.4,
        )

        answer = response.choices[0].message.content
        return JsonResponse({"response": answer})

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)