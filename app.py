from flask import Flask, render_template, request, jsonify, send_file
from google import genai
from dotenv import load_dotenv
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.colors import HexColor
from datetime import datetime
import os
import io

# ----------------------------
# Load Environment Variables
# ----------------------------

load_dotenv()

app = Flask(__name__)

# ----------------------------
# Gemini API
# ----------------------------

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

latest_question = ""
latest_answer = ""

# ----------------------------
# Home Page
# ----------------------------

@app.route("/")
def home():
    return render_template("index.html")


# ----------------------------
# Ask AI
# ----------------------------

@app.route("/ask", methods=["POST"])
def ask():

    global latest_question, latest_answer

    try:

        data = request.get_json()

        question = data.get("question", "").strip()

        if question == "":

            return jsonify({
                "answer": "Please enter a research question."
            })

        prompt = f"""
You are a professional AI Research Assistant.

Generate a well-structured research report in Markdown.

Rules:

# Title

## Definition

Explain in 5–7 lines.

## Key Points

Use bullet points.

## Applications

Use bullet points.

## Advantages

Use bullet points.

## Disadvantages

Use bullet points.

## Future Scope

Explain briefly.

## Conclusion

Write a short conclusion.

Keep the language simple, professional and suitable for students.

Question:

{question}
"""

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        latest_question = question
        latest_answer = response.text

        return jsonify({
            "answer": latest_answer
        })

    except Exception as e:

        return jsonify({
            "answer": f"❌ Error : {str(e)}"
        })
# ------------------------------------
# Download PDF
# ------------------------------------

@app.route("/download_pdf")
def download_pdf():

    global latest_question, latest_answer

    buffer = io.BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )

    styles = getSampleStyleSheet()

    title = styles["Title"]
    title.alignment = TA_CENTER
    title.textColor = HexColor("#1E3A8A")
    title.fontSize = 24

    heading = styles["Heading2"]
    heading.textColor = HexColor("#2563EB")
    heading.fontSize = 16

    body = styles["BodyText"]
    body.fontSize = 12
    body.leading = 20

    story = []

    # -------------------------
    # Header
    # -------------------------

    story.append(
        Paragraph(
            "🤖 AI Research Assistant",
            title
        )
    )

    story.append(
        Paragraph(
            "<b>AI Generated Research Report</b>",
            body
        )
    )

    story.append(Spacer(1, 20))

    story.append(
        Paragraph(
            "<b>Date:</b> " +
            datetime.now().strftime("%d %B %Y  %I:%M %p"),
            body
        )
    )

    story.append(Spacer(1, 18))

    story.append(
        Paragraph(
            "<font color='blue'><b>Research Question</b></font>",
            heading
        )
    )

    story.append(
        Paragraph(
            latest_question,
            body
        )
    )

    story.append(Spacer(1, 20))

    # -------------------------
    # AI Answer Formatting
    # -------------------------

    lines = latest_answer.split("\n")

    for line in lines:

        line = line.strip()

        if line == "":
            story.append(Spacer(1, 8))
            continue

        # Main Title
        if line.startswith("# "):

            story.append(
                Paragraph(
                    f"<font size='20' color='#1E3A8A'><b>{line[2:]}</b></font>",
                    body
                )
            )

            story.append(Spacer(1, 15))

        # Heading

        elif line.startswith("## "):

            story.append(
                Paragraph(
                    f"<font size='16' color='#2563EB'><b>{line[3:]}</b></font>",
                    body
                )
            )

            story.append(Spacer(1, 10))

        # Bullet Points

        elif line.startswith("- "):

            story.append(
                Paragraph(
                    f"• {line[2:]}",
                    body
                )
            )

        # Bold text

        elif line.startswith("**"):

            story.append(
                Paragraph(
                    f"<b>{line.replace('**','')}</b>",
                    body
                )
            )

        else:

            story.append(
                Paragraph(
                    line,
                    body
                )
            )

    story.append(Spacer(1, 25))

    story.append(
        Paragraph(
            "<font color='green'><b>Generated using Google Gemini AI</b></font>",
            body
        )
    )

    doc.build(story)

    buffer.seek(0)

    return send_file(
        buffer,
        as_attachment=True,
        download_name="AI_Research_Report.pdf",
        mimetype="application/pdf"
    )


# ------------------------------------
# Run Flask
# ------------------------------------

if __name__ == "__main__":
    app.run(debug=True)