from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Load the word list

def load_words(filename):
    with open(filename, 'r') as file:
        return [line.strip() for line in file if line.strip()]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/filter', methods=['POST'])
def filter_words():
    data = request.json
    greens = data.get('greens', {})
    yellows = data.get('yellows', [])
    reds = data.get('reds', [])
    mode = data.get('mode', 'wordle')
    length = int(data.get('length', 5))

    if mode == 'lewdle':
        word_list = load_words('lewdle_answers.txt')
    else:
        word_list = load_words('wordle_answers.txt')

    word_list = [w for w in word_list if len(w) == length]

    possible = []
    for word in word_list:
        match = True

        # Greens
        for pos, char in greens.items():
            if int(pos) >= len(word) or word[int(pos)] != char:
                match = False
                break
        if not match:
            continue

        # Yellows
        if not all(y in word for y in yellows):
            continue
        if any(word[int(pos)] == y for pos, y in greens.items() if y in yellows):
            continue

        # Reds
        for r in reds:
            if r in word and r not in greens.values() and r not in yellows:
                match = False
                break

        if match:
            possible.append(word)

    return jsonify({"matches": possible})

if __name__ == '__main__':
    app.run(debug=True)
