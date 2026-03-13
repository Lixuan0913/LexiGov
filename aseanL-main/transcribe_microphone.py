from flask import Flask, render_template, request, jsonify
from openai import OpenAI

app = Flask(__name__)

client = OpenAI(api_key="YOUR_API_KEY")


def simplify_text(text):

    prompt = f"""
    Rewrite the following text in simple English (5th grade level).

    {text}
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content


def summarize_text(text):

    prompt = f"""
    Summarize this into 3-5 actionable bullet points.

    {text}
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/simplify", methods=["POST"])
def simplify():

    data = request.json
    text = data["text"]

    simple = simplify_text(text)
    summary = summarize_text(simple)

    return jsonify({
        "simplified": simple,
        "summary": summary
    })


if __name__ == "__main__":
    app.run(debug=True)