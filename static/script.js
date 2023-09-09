class Game {
  constructor() {
    this.score = 0;
    this.highScore = parseInt($('#high-score').text());
    this.words = new Set();
    this.$count = $('#count');
  }

  addWord(word) {
    this.words.add(word);
    let wordList = $('#word-list');

    let li = $('<li></li>').text(word);
    wordList.append(li);

    this.score += 1;
    $('#score').text(this.score);
  }

  async finishGame() {
    if (this.score > this.highScore) {
      $('#high-score').text(this.score);
    }
    await axios.post('/score', { score: this.score }, {
      headers: {
        'Content-Type': 'application/json'
      }
    });
    let count = parseInt(this.$count.text());
    this.$count.text(count + 1);
    alert(`Game over! Your score was ${this.score}!`);
  }
}

let game = new Game();
let time = $('[data-v-time]');

let timer = setInterval((() => {
  let count = 60;

  return async () => {
    time.text(count);
    count--;
    if (count < 0) {
      clearInterval(timer);
      $('button').prop('disabled', true);
      await game.finishGame();
    }
  }
})(), 1000);

$('#check-word').submit(async (e) => {
  e.preventDefault();

  let word = $('input[name="word"]').val();

  try {
    let response = await axios.get(`/check/${word}`);
    let result = response.data.result;

    if (result !== 'ok') {
      return alert("That word doesn't exist in this boggle!");
    } else if (game.words.has(word)) {
      return alert("You've already guessed that word!");
    }

    game.addWord(word);
  } catch (error) {
    console.error(error);
    alert("An error occurred while checking the word.");
  }
});