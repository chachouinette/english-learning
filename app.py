#!/usr/bin/env python3
from flask import Flask, render_template, request, redirect, url_for, jsonify, session
import json
import random
import os

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')

VOCAB_FILE = "vocabulary.json"

def load_vocabulary():
    """Load vocabulary from JSON file."""
    if not os.path.exists(VOCAB_FILE):
        return []

    with open(VOCAB_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_vocabulary(vocab):
    """Save vocabulary to JSON file."""
    with open(VOCAB_FILE, 'w', encoding='utf-8') as f:
        json.dump(vocab, f, indent=4, ensure_ascii=False)

@app.route('/')
def index():
    """Main page."""
    return render_template('index.html')

@app.route('/vocabulary')
def vocabulary():
    """Display all words."""
    vocab = load_vocabulary()
    return render_template('vocabulary.html', words=vocab)

@app.route('/add', methods=['GET', 'POST'])
def add_word():
    """Add a new word."""
    if request.method == 'POST':
        french = request.form.get('french', '').strip()
        english = request.form.get('english', '').strip()

        if french and english:
            vocab = load_vocabulary()
            vocab.append({"french": french, "english": english})
            save_vocabulary(vocab)
            return redirect(url_for('vocabulary'))

    return render_template('add_word.html')

@app.route('/delete/<int:index>', methods=['POST'])
def delete_word(index):
    """Delete a word by index."""
    vocab = load_vocabulary()
    if 0 <= index < len(vocab):
        vocab.pop(index)
        save_vocabulary(vocab)
    return redirect(url_for('vocabulary'))

@app.route('/quiz')
def quiz():
    """Start quiz page."""
    vocab = load_vocabulary()
    if not vocab:
        return render_template('quiz.html', no_words=True)

    # Shuffle and store in session
    quiz_words = vocab.copy()
    random.shuffle(quiz_words)
    session['quiz_words'] = quiz_words
    session['quiz_index'] = 0
    session['quiz_score'] = 0

    return render_template('quiz.html',
                         current_word=quiz_words[0],
                         question_num=1,
                         total=len(quiz_words))

@app.route('/quiz/answer', methods=['POST'])
def quiz_answer():
    """Process quiz answer."""
    quiz_words = session.get('quiz_words', [])
    current_index = session.get('quiz_index', 0)
    score = session.get('quiz_score', 0)

    if current_index >= len(quiz_words):
        return redirect(url_for('quiz_results'))

    answer = request.form.get('answer', '').strip().lower()
    correct_answer = quiz_words[current_index]['english'].lower()

    is_correct = answer == correct_answer
    if is_correct:
        score += 1
        session['quiz_score'] = score

    current_index += 1
    session['quiz_index'] = current_index

    # Check if quiz is complete
    if current_index >= len(quiz_words):
        return render_template('quiz_result.html',
                             is_correct=is_correct,
                             correct_answer=quiz_words[current_index-1]['english'],
                             french_word=quiz_words[current_index-1]['french'],
                             final_score=score,
                             total=len(quiz_words),
                             show_final=True)

    return render_template('quiz_result.html',
                         is_correct=is_correct,
                         correct_answer=quiz_words[current_index-1]['english'],
                         french_word=quiz_words[current_index-1]['french'],
                         next_word=quiz_words[current_index],
                         question_num=current_index+1,
                         total=len(quiz_words),
                         score=score)

@app.route('/quiz/results')
def quiz_results():
    """Display final quiz results."""
    score = session.get('quiz_score', 0)
    quiz_words = session.get('quiz_words', [])
    total = len(quiz_words)

    percentage = (score / total * 100) if total > 0 else 0

    # Clear session
    session.pop('quiz_words', None)
    session.pop('quiz_index', None)
    session.pop('quiz_score', None)

    return render_template('results.html',
                         score=score,
                         total=total,
                         percentage=percentage)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=False)
