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

        if not message:
            return JsonResponse({"error": "Message vide"}, status=400)

        from openai import OpenAI

        client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Tu es un expert en assurance."},
                {"role": "user", "content": message},
            ],
        )

        answer = response.choices[0].message.content
        return JsonResponse({"response": answer})

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)