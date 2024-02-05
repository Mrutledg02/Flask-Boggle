from flask import Flask, render_template, session, request, jsonify
from boggle import Boggle

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'

# Instantiate Boggle class
boggle_game = Boggle()

@app.route('/')
def index():
    """Render the main Boggle game page."""
    board = boggle_game.make_board()
    session['board'] = board  # Store the board in the session
    return render_template('index.html', board=board)

# Set to store guessed words
guessed_words = set()

# Route to check for a valid word
@app.route('/check_word', methods=['POST'])
def check_word():
    """Check if a submitted word is valid and return the result and score."""
    word = request.json['word']
    board = session['board']

    # Check if the word has already been guessed
    if word in guessed_words:
        return jsonify({'result': 'duplicate', 'score': 0})

    # Use the Boggle class methods to check for a valid word
    result = boggle_game.check_valid_word(board, word)

    # Calculate the score (score is equal to the length of the word)
    if result == 'ok':
        score = len(word)
        # Add the word to the set of guessed words
        guessed_words.add(word)
    else:
        score = 0

    # Respond with JSON including the result and the score
    return jsonify({'result': result, 'score': score})


#Route to update statistics after the game ends
@app.route('/end_game', methods=['POST'])
def end_game():
    """Update game statistics after the game ends."""
    score = request.json['score']

    # Increment the number of times the user has played
    session['num_played'] = session.get('num_played', 0) + 1

    # Update the highest score if the current score is higher
    session['highest_score'] = max(session.get('highest_score', 0), score)

    # Save the updated session
    session.modified = True

    # Respond with any relevant information (optional)
    return jsonify({'message': 'Game ended successfully', 'num_played': session['num_played'], 'highest_score': session['highest_score']})

if __name__ == '__main__':
    app.run(debug=True)
