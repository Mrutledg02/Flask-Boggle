$(document).ready(function () {
    class BoggleGame {
        constructor() {
            this.totalScore = 0;
            this.timeLimit = 60;
            this.timer = null;
            this.initializeEvents();
        }

        updateTimer() {
            $('#timer').text(`Time left: ${this.timeLimit} seconds`);
        }

        makeAjaxRequest(url, data) {
            return axios.post(url, data)
                .then(response => response.data)
                .catch(error => {
                    console.error('Error:', error);
                    throw error;
                });
        }

        handleFormSubmission() {
            const word = $('#word').val();

            this.makeAjaxRequest('/check_word', { word })
                .then(data => {
                    const resultMessage = data.result === 'ok' ?
                        `Valid word on the board! Score: ${data.score}` :
                        data.result === 'not-on-board' ?
                            'Word is not on the board.' :
                            'Not a valid word.';

                    this.totalScore += data.score;
                    $('#current-score').text(`Current Score: ${this.totalScore}`);
                    
                    // Display the result message
                    $('#result-message')
                        .text(resultMessage)
                        .show(); // Show the result message
                })
                .catch(error => {
                    console.error('Error:', error);
                    $('#error-message').text('An error occurred. Please try again.');
                });
        }

        initializeEvents() {
            $('#word-form').submit((event) => {
                event.preventDefault();

                if (this.timeLimit > 0) {
                    this.handleFormSubmission();
                }
            });
        }

        endGame() {
            $('#word').prop('disabled', true);
            $('#word-form button').prop('disabled', true);

            this.makeAjaxRequest('/end_game', { score: this.totalScore })
                .then(response => {
                    console.log(response.data);
                })
                .catch(error => {
                    console.error('Error:', error);
                    // Display an error message to the user
                    $('#error-message').text('An error occurred. Please try again.');
                });
        }

        startTimer() {
            this.timer = setInterval(() => {
                this.timeLimit--;
                this.updateTimer();

                if (this.timeLimit <= 0) {
                    clearInterval(this.timer);
                    $('#timer').text('Time is up!');
                    this.endGame();
                }
            }, 1000);

            this.updateTimer();
        }
    }

    const boggleGame = new BoggleGame();
    boggleGame.startTimer();
});
