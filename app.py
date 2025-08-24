from flask import Flask, render_template, request, jsonify
import wikipedia
import openai
import os

app = Flask(__name__)

# ✅ OpenAI API key
openai.api_key = os.environ.get("OPENAI_API_KEY")  # Set in Vercel/Env

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_msg = request.json.get("message", "").strip()
    lower_msg = user_msg.lower()

    # Fixed Commands
    if "hello" in lower_msg or "hi" in lower_msg:
        reply = "Access Granted ✅ Hello Agent 👨‍💻"
    elif "hack" in lower_msg:
        reply = "⚡ Initiating hacking sequence... (simulation only)"
    elif "owner" in lower_msg:
        reply = "My owner is 👑 Devi"
    elif "bye" in lower_msg:
        reply = "👋 Logging off... Stay anonymous!"
    else:
        # Try Wikipedia first
        try:
            wiki_result = wikipedia.summary(user_msg, sentences=2)
            reply = f"📡 Wikipedia Intel: {wiki_result}"
        except:
            # If Wikipedia fails, fallback to OpenAI GPT
            try:
                response = openai.ChatCompletion.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": "You are a hacker style assistant. Respond concisely with green terminal vibes."},
                        {"role": "user", "content": user_msg}
                    ],
                    max_tokens=150
                )
                reply = response.choices[0].message.content
            except Exception as e:
                reply = f"❌ Cannot fetch data: {str(e)}"

    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run(debug=True)