<<<<<<< HEAD
# Flavour Fusion - AI-Driven Recipe Blogging

Flavour Fusion is a Flask web app that uses Google Gemini to generate detailed recipe blogs from a user topic and target word count.

## Category
Cloud Application Development

## Skills Used
NLP, Prompt Engineering, Web Development (Flask), API Integration

## Features
- Generate recipe blogs from a custom topic and word count
- Supports 1 to 3 content variations per request
- Shows a programmer joke while content is being generated
- Handles Gemini model fallback for better reliability
- Works in fallback mode when no API key is configured

## Project Structure
- `app.py` - Flask backend and Gemini API integration
- `templates/index.html` - Input form and loading/joke UI
- `templates/result.html` - Generated output view
- `static/css/style.css` - Styling
- `requirements.txt` - Python dependencies

## Prerequisites
- Python 3.10+
- A Google AI Studio / Gemini API key (optional for live AI generation)

## Setup
1. Create and activate virtual environment:
   - Windows PowerShell:
     - `python -m venv venv`
     - `venv\\Scripts\\Activate.ps1`
2. Install dependencies:
   - `pip install -r requirements.txt`
3. Set environment variable:
   - PowerShell (current session):
     - `$env:GOOGLE_API_KEY="your_api_key_here"`
4. Run app:
   - `python app.py`
5. Open browser:
   - `http://127.0.0.1:5000`

## Notes
- If `GOOGLE_API_KEY` is missing, the app returns a local fallback recipe template.
- If you get `403`, verify API key restrictions and Gemini API enablement.
- If you get `429`, wait and retry due to rate limiting.

## Example Scenarios
- Vegan Recipe Blog: Topic `Vegan Chocolate Cake`, Word Count `1200`
- Quick Dinner Blog: Topic `Quick Weeknight Dinners`, Word Count `800`
- Gluten-Free Baking Blog: Topic `Gluten-Free Bread`, Word Count `1500`
=======
# Flavour-Fusion-AI-Driven-Recipe-Blogging
>>>>>>> d588561c2ffd55ed06e6400e95b0d239783560a7
