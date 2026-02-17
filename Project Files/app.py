import os
from flask import Flask, render_template, request
from dotenv import load_dotenv

try:
    # Preferred SDK (actively maintained)
    from google import genai as google_genai
    _GENAI_MODE = "new"
except ImportError:
    # Backward-compatible fallback for older environments
    import google.generativeai as google_genai
    _GENAI_MODE = "legacy"

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Get API key
API_KEY = os.getenv("GOOGLE_API_KEY", "").strip()
print(f"API key loaded: {'yes' if API_KEY else 'no'}")

# Configure legacy Gemini SDK
if API_KEY and _GENAI_MODE == "legacy":
    google_genai.configure(api_key=API_KEY)

# Programmer jokes
PROGRAMMER_JOKES = [
    "Why do programmers prefer dark mode? Because light attracts bugs!",
    "A SQL query walks into a bar, walks up to two tables, and asks: Can I join you?",
    "There are 10 kinds of people in the world: those who understand binary and those who do not.",
    "Debugging is like being the detective in a crime movie where you are also the murderer.",
]


def fallback_recipe(topic: str, word_count: int) -> str:
    return (
        f"{topic} - Simple Home Recipe Guide\n\n"
        "Ingredients:\n"
        "- 2 cups main ingredient of choice\n"
        "- 1 tbsp oil or butter\n"
        "- 1 tsp salt (adjust to taste)\n"
        "- 1 tsp spices/herbs\n"
        "- Optional garnish\n\n"
        "Steps:\n"
        "1. Prep all ingredients and preheat cookware.\n"
        "2. Cook base ingredients on medium heat until aromatic.\n"
        "3. Add seasonings and simmer until textures are just right.\n"
        "4. Plate, garnish, and serve warm.\n\n"
        "Cooking Tips:\n"
        "- Taste and adjust seasoning near the end.\n"
        "- Keep heat moderate to avoid burning.\n"
        "- Pair with a fresh side salad or bread.\n\n"
        f"Requested target length: ~{word_count} words."
    )


def call_gemini(prompt: str) -> str:
    if not API_KEY:
        raise RuntimeError("GOOGLE_API_KEY is not configured.")

    if _GENAI_MODE == "new":
        client = google_genai.Client(api_key=API_KEY)
        model_candidates = ["gemini-2.5-flash", "gemini-2.0-flash", "gemini-1.5-flash"]
        last_error = None
        for model_name in model_candidates:
            try:
                response = client.models.generate_content(
                    model=model_name,
                    contents=prompt,
                )
                text = (response.text or "").strip()
                if text:
                    return text
            except Exception as exc:
                last_error = exc
        raise RuntimeError(f"Gemini new SDK failed for all model candidates: {last_error}")

    model_candidates = ["gemini-2.0-flash", "gemini-1.5-flash", "gemini-1.5-flash-latest"]
    last_error = None
    for model_name in model_candidates:
        try:
            model = google_genai.GenerativeModel(model_name)
            response = model.generate_content(prompt)
            text = (response.text or "").strip()
            if text:
                return text
        except Exception as exc:
            last_error = exc
    raise RuntimeError(f"Gemini legacy SDK failed for all model candidates: {last_error}")


def generate_recipe(topic: str, word_count: int) -> str:
    print(f"Generating recipe for topic: {topic}")

    prompt = (
        f"Write a detailed recipe blog about '{topic}' "
        f"with approximately {word_count} words. "
        "Include ingredients, numbered steps, prep/cook times, "
        "and practical cooking tips."
    )

    try:
        ai_text = call_gemini(prompt)
        if ai_text:
            return ai_text
        raise RuntimeError("Gemini response did not include text.")
    except Exception as exc:
        print(f"Gemini generation failed: {exc}")
        return fallback_recipe(topic, word_count)


@app.route("/")
def home():
    return render_template("index.html", jokes=PROGRAMMER_JOKES)


@app.route("/generate", methods=["POST"])
def generate():
    topic = request.form.get("topic", "Quick and Easy Cooking")
    word_count_raw = request.form.get("word_count", 300)
    variations_raw = request.form.get("variations", 1)
    selected_joke = request.form.get("joke") or PROGRAMMER_JOKES[0]

    try:
        word_count = int(word_count_raw)
    except (TypeError, ValueError):
        word_count = 300
    word_count = max(50, min(1500, word_count))

    try:
        variations = int(variations_raw)
    except (TypeError, ValueError):
        variations = 1
    variations = max(1, min(3, variations))

    blogs = [generate_recipe(topic, word_count) for _ in range(variations)]

    return render_template("result.html", blog=blogs, joke=selected_joke)


if __name__ == "__main__":
    app.run(debug=True)
