from flask import Flask, render_template, request, redirect, url_for, session
import random

app = Flask(__name__)
app.secret_key = "supersecretkey"

# Load questions from file
questions = []
with open("ok.txt", "r", encoding="utf-8") as f:
    for line in f:
        parts = line.strip().split(";")
        if len(parts) == 6:
            q, a, b, c, d, correct = parts
            questions.append({
                "question": q,
                "options": {"A": a, "B": b, "C": c, "D": d},
                "answer": correct
            })


@app.route("/")
def home():
    return render_template("start.html")


@app.route("/start")
def start_quiz():
    random.shuffle(questions)
    session["quiz"] = questions[:10]   # Select 10 random questions
    session["current"] = 0
    session["score"] = 0
    return redirect(url_for("quiz_question", qno=1))


@app.route("/quiz/<int:qno>", methods=["GET", "POST"])
def quiz_question(qno):
    quiz = session.get("quiz", [])
    if not quiz:
        return redirect(url_for("home"))

    if request.method == "POST":
        user_ans = request.form.get("answer")
        current = session["current"]
        correct = quiz[current]["answer"]

        # Score handling
        if user_ans == correct:
            session["score"] += 4
        elif user_ans is not None:
            session["score"] -= 1

        session["current"] = current + 1

        # If quiz finished
        if session["current"] >= len(quiz):
            return redirect(url_for("result"))

        # Go to next question
        return redirect(url_for("quiz_question", qno=session["current"] + 1))

    # Display question
    current = session["current"]
    q = quiz[current]
    return render_template("question.html", qno=qno, question=q, total=len(quiz))


@app.route("/result")
def result():
    score = session.get("score", 0)
    return render_template("result.html", score=score)


if __name__ == "__main__":
    app.run(debug=True)
