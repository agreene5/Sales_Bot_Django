from django.shortcuts import render, redirect
from django.http import JsonResponse, StreamingHttpResponse
from django.conf import settings
from .models import Preference, User_Input, Checkout
from .forms import PreferenceForm, UserInputForm
from ollama import Client
import json

client = Client(host=settings.OLLAMA_HOST)


def index(request):
    form = PreferenceForm()
    Preferences = Preference.objects.all()

    if request.method == "POST":
        form = PreferenceForm(request.POST)

        if form.is_valid():
            form.save()

        return redirect("sales_screen")

    context = {"Preferences": Preferences, "PreferenceForm": form}
    return render(request, "preference_screen.html", context)


def build_context(previous_messages, new_message):
    context = ""
    for msg in previous_messages:
        context += f"User: {msg.user_input}\n"
        if msg.llm_response:
            context += f"Assistant: {msg.llm_response}\n"

    context += f"User: {new_message}\n"
    return context


def stream_response(response_stream):
    for chunk in response_stream:
        if 'response' in chunk:
            yield f"data: {json.dumps({'text': chunk['response']})}\n\n"


def sales_screen(request):
    form = UserInputForm()
    user_inputs = User_Input.objects.all().order_by('timestamp')

    latest_preferences = Preference.objects.last()  # Gets the most recent preference entry

    system_prompt = f"You are an eccentric sales bot who's purpose is to sell unique and relevant items to the user. \
    You talk like a traditional salesman and use everything you can to try and strike a deal. That being said, you are \
    shrewd in your dealings and won't accept unprofitable sales. Here are the items the user likes:\
    {latest_preferences.items_likes if latest_preferences else 'None'} and here are the items the user dislikes:\
    {latest_preferences.items_dislikes if latest_preferences else 'None'}. Sell the user items one at a time, only \
    moving to the next item if the user purchases or rejects the current item. Also, keep your responses concise and \
    don't ramble for too long"

    context = {"user_input_form": form, "user_inputs": user_inputs}

    if request.method == "POST":
        if request.POST.get('clear'):
            User_Input.objects.all().delete()
            return JsonResponse({'status': 'success'})

        form = UserInputForm(request.POST)
        if form.is_valid():
            user_input = form.save(commit=False)

            try:
                previous_messages = User_Input.objects.all().order_by('-timestamp')[:5]
                prompt = build_context(previous_messages, user_input.user_input)

                user_input.save()

                response_stream = client.generate(
                    model = "llama3.2:3b",
                    system = system_prompt,
                    prompt = prompt,
                    stream = True
                )

                response = StreamingHttpResponse(
                    stream_response(response_stream),
                    content_type='text/event-stream'
                )
                response['Cache-Control'] = 'no-cache'
                return response

            except Exception as e:
                print(f"Error in LLM generation: {str(e)}")
                return JsonResponse({
                    'status': 'error',
                    'message': str(e)
                }, status=500)

    return render(request, "sales_screen.html", context)


def checkout_screen(request):
    if request.method == "POST":
        time_shopping = float(request.POST.get("time_shopping", 0.0))
        items_bought = int(request.POST.get("items_bought", 0))
        money_spent = int(request.POST.get("money_spent", 0))

        Checkout.objects.create(
            time_shopping=time_shopping,
            items_bought=items_bought,
            money_spent=money_spent
        )

        context = {
            "time_spent": time_shopping,
            "items_bought": items_bought,
            "money_spent": money_spent
        }
        return render(request, "checkout_screen.html", context)

        context = {
            "error": "Invalid checkout data provided.",
            "time_spent": 0,
            "items_bought": 0,
            "money_spent": 0
        }
        return render(request, "checkout_screen.html", context)

    return render(request, 'checkout_screen.html', {
        "time_spent": 0,
        "items_bought": 0,
        "money_spent": 0
    })