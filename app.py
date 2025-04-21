from flask import Flask, render_template, request, jsonify
import os

app = Flask(__name__)

# Load the word list from file
def load_words(filename):
    with open(filename, 'r') as file:
        return [line.strip().lower() for line in file if line.strip()]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/filter', methods=['POST'])
def filter_words():
    data = request.json
    greens = data.get('greens', {})  # {"0": "a", "2": "r"}
    yellows = set(data.get('yellows', []))  # ["s", "t"]
    reds = set(data.get('reds', []))  # ["q", "z"]
    mode = data.get('mode', 'wordle')
    length = int(data.get('length', 5))

    filename = 'wordle_answers.txt' if mode == 'wordle' else 'lewdle_answers.txt'
    all_words = [word for word in load_words(filename) if len(word) == length]

    filtered = []
    for word in all_words:
        valid = True

        # Check green letters (must match at exact positions)
        for pos, char in greens.items():
            idx = int(pos)
            if idx >= len(word) or word[idx] != char:
                valid = False
                break

        if not valid:
            continue

        # Check yellow letters (must be in word, but NOT at any green position)
        for y in yellows:
            if y not in word:
                valid = False
                break
        if not valid:
            continue

        for pos, char in greens.items():
            if char in yellows and word[int(pos)] == char:
                valid = False
                break

        if not valid:
            continue

        # Check red letters (must not be in word, unless it's already green or yellow)
        for r in reds:
            if r in word and r not in greens.values() and r not in yellows:
                valid = False
                break

        if valid:
            filtered.append(word)

    return jsonify({"matches": filtered})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
