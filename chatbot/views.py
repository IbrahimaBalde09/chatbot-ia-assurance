import json

from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from .services import get_chatbot_response


def home_view(request):
    return render(request, "chatbot/home.html")


@csrf_exempt
def ask_view(request):
    if request.method != "POST":
        return JsonResponse({"error": "Méthode non autorisée"}, status=405)

    try:
        data = json.loads(request.body)
        question = data.get("question", "").strip()

        if not question:
            return JsonResponse({"error": "Question vide"}, status=400)

        result = get_chatbot_response(question)

        return JsonResponse({
            "answer": result["answer"],
            "sources": result["sources"],
            "domain": result["domain"],
        })

    except Exception as e:
        return JsonResponse({
            "error": str(e)
        }, status=500)


def clear_chat_view(request):
    return JsonResponse({"status": "ok"})