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


def build_context(previous_messages, new_message, reset_context=False):
    conversation_history = []

    reminder_context = """
    IMPORTANT INSTRUCTIONS:
    1. After processing a purchase with [BUY: (Item_Name, Price)], treat it as completed
    2. Focus on responding to the current request
    3. Remember only your last response to maintain conversation flow
    """
    conversation_history.append({"role": "system", "content": reminder_context})

    if previous_messages and not reset_context:
        for msg in previous_messages:
            conversation_history.append({
                "role": "user",
                "content": msg.user_input
            })
            if msg.llm_response:
                conversation_history.append({
                    "role": "assistant",
                    "content": msg.llm_response
                })
    elif previous_messages and reset_context:
        last_message = previous_messages[-1]
        if last_message.llm_response:
            conversation_history.append({
                "role": "assistant",
                "content": last_message.llm_response
            })

    conversation_history.append({
        "role": "user",
        "content": new_message
    })

    return format_context(conversation_history)

def format_context(conversation_history):
    formatted_context = "SYSTEM INSTRUCTIONS:\n" + conversation_history[0]['content'] + "\n\n"
    formatted_context += "CONVERSATION:\n" + "\n".join([
        f"{msg['role'].upper()}: {msg['content'].strip()}"
        for msg in conversation_history[1:]
    ])
    return formatted_context


def stream_response(response_stream):
    try:
        accumulated_response = ""
        for chunk in response_stream:
            if 'response' in chunk:
                accumulated_response += chunk['response']
                yield f"data: {json.dumps({'text': chunk['response'], 'full_response': accumulated_response})}\n\n"
    except Exception as e:
        print(f"Error in stream_response: {str(e)}")
        yield f"data: {json.dumps({'error': str(e)})}\n\n"


def sales_screen(request):
    form = UserInputForm()
    user_inputs = User_Input.objects.order_by('-timestamp')[:20]
    user_inputs = list(user_inputs)
    user_inputs.reverse()

    latest_preferences = Preference.objects.last()

    SYSTEM_PROMPT = '''
    You are a focused yet wacky sales bot that:
    1. Handles one interaction at a time
    2. After completing a [BUY: (Item_Name, Price)], start fresh
    3. Only remembers the last purchase
    4. Focuses on current requests and new items

    Current user preferences:
    - Likes: {likes}
    - Dislikes: {dislikes}

    Remember: After processing a purchase, treat it as a new conversation while remembering only the last purchase details.
    '''

    system_prompt = SYSTEM_PROMPT.format(
        likes=latest_preferences.items_likes if latest_preferences else "None",
        dislikes=latest_preferences.items_dislikes if latest_preferences else "None"
    )

    context = {
        "user_input_form": form,
        "user_inputs": user_inputs,
    }

    if request.method == "POST":
        if request.POST.get('clear'):
            User_Input.objects.all().delete()
            return JsonResponse({'status': 'success'})

        form = UserInputForm(request.POST)
        if form.is_valid():
            user_input = form.save(commit=False)
            user_input.save()

            try:
                previous_messages = list(User_Input.objects.order_by('-timestamp')[:15])
                previous_messages.reverse()

                reset_context = request.POST.get('reset_context') == 'true'

                prompt = build_context(
                    previous_messages,
                    user_input.user_input,
                    reset_context=reset_context
                )

                response_stream = client.generate(
                    model="gemma2:9b", #gemma2:9b #llama3.1:8b #llama3.2:3b
                    system=system_prompt,
                    prompt=prompt,
                    stream=True,
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
        money_spent = float(request.POST.get("money_spent", 0))

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