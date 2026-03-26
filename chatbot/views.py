import os
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json


# Page d'accueil (test Railway OK)
def home(request):
    return HttpResponse("Chatbot IA Assurance en ligne ✅")


# Endpoint chatbot
@csrf_exempt
def chat(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST request required"}, status=400)

    try:
        data = json.loads(request.body)
        message = data.get("message", "")

        if not message:
            return JsonResponse({"error": "Message vide"}, status=400)

        # 🔥 Import OpenAI ici (important pour éviter crash au démarrage)
        from openai import OpenAI

        client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Tu es un expert en assurance."},
                {"role": "user", "content": message}
            ]
        )

        answer = response.choices[0].message.content

        return JsonResponse({"response": answer})

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)