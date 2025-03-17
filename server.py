from flask import Flask, request, jsonify
from app import CelestiCode  # Import CelestiCode from app.py

app = Flask(__name__)

# Initialize CelestiCode with API keys (replace these later with actual keys)
celesti = CelestiCode("your-openai-key", "your-gemini-key", "your-claude-key")

@app.route("/generate", methods=["POST"])
def generate():
    data = request.json
    prompt = data.get("prompt", "")
    model = data.get("model", "openai")
    length = data.get("length", 1000)
    style = data.get("style", "academic")
    
    if not prompt:
        return jsonify({"error": "No prompt provided"}), 400
    
    response = celesti.generate_paper(prompt, model, length, style)
    return jsonify({"response": response})

@app.route("/speak", methods=["POST"])
def speak():
    data = request.json
    text = data.get("text", "")
    if text:
        celesti.speak(text)
        return jsonify({"message": "Speaking..."})
    return jsonify({"error": "No text provided"}), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
