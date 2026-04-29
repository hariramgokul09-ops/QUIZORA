import google.generativeai as genai
import ast
import re

def getquestions(subject, chapter):
    # Configure Gemini API key
    genai.configure(api_key="AIzaSyC4xFKByoyzNIJaXOfJ8WqQCdNg2oLFqMk")

    # Initialize the model
    model = genai.GenerativeModel("models/gemini-2.5-flash")

    # --- Dynamic Prompt ---
    prompt = f"""
    Generate exactly 5 multiple-choice quiz questions for Class 5 students on the topic '{chapter}' from the subject '{subject}'.

    Return only a valid Python list variable named 'questions' in the following structure:
    questions = [
        ["Question text", ["Option A", "Option B", "Option C", "Option D"], correct_option_number (1-4),
        "Short explanation", level_number (1 for easy, 2 for medium, 3 for hard)]
    ]

    Rules:
    - Do not include any markdown formatting.
    - Do not include ``` or code fences.
    - Do not include any text outside the Python code.
    Only output the Python list exactly as shown above.
    """

    # Generate response
    response = model.generate_content(prompt)
    text = response.text.strip()

    # --- Clean up ---
    text = re.sub(r"^```(?:python)?|```$", "", text, flags=re.MULTILINE).strip()

    # Extract list if "questions = [ ... ]"
    if text.startswith("questions"):
        match = re.search(r"questions\s*=\s*(\[.*\])", text, re.DOTALL)
        if match:
            text = match.group(1).strip()

    # --- Parse safely ---
    try:
        questions = ast.literal_eval(text)
        print("✅ Parsed successfully! Generated questions:\n")
        for q in questions:
            print(q, "\n")
        return questions
    except Exception as e:
        print("⚠️ Could not parse AI output directly:", e)
        print("\n--- Raw output from Gemini ---\n")
        print(text)
        return []

# Example usage:
# getquestions("Biology", "Living and Non-Living Things")
