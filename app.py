#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 10 19:12:51 2025

@author: ei900
"""

from flask import Flask, render_template, request, jsonify
import os

app = Flask(__name__)

# Load the word list
def load_words(filename):
    with open(filename, 'r') as file:
        return [line.strip() for line in file if len(line.strip()) == 5]

WORD_LIST = load_words("wordle_answers.txt")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/filter', methods=['POST'])
def filter_words():
    data = request.json
    greens = data.get('greens', {})       # {"0": "a", "2": "r"}
    yellows = data.get('yellows', [])     # ["s", "t"]
    reds = data.get('reds', [])           # ["q", "z", ...]

    possible = []
    for word in WORD_LIST:
        match = True

        # Greens (correct letters in correct position)
        for pos, char in greens.items():
            if word[int(pos)] != char:
                match = False
                break
        if not match:
            continue

        # Yellows (correct letters in wrong positions)
        if not all(y in word for y in yellows):
            continue
        if any(word[int(pos)] == y for pos, y in greens.items() if y in yellows):
            continue

        # Reds (incorrect letters)
        for r in reds:
            if r in word and r not in greens.values() and r not in yellows:
                match = False
                break
        if match:
            possible.append(word)

    return jsonify({"matches": possible})

if __name__ == '__main__':
    app.run(debug=True)