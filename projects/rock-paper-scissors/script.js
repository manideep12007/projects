const rock = document.querySelector(".rock");
const paper = document.querySelector(".paper");
const scissors = document.querySelector(".scissors");
const info = document.getElementById("info");
const reset = document.querySelector(".reset");

let playerscore = document.querySelector(".user-score");
let computerscore = document.querySelector(".computer-score");

let score1 = 0;
let score2 = 0;

const choices = ["rock", "paper", "scissors"];

function playGame(user) {
    let computer = choices[Math.floor(Math.random() * choices.length)];

    if (user === computer) {
        info.innerHTML = `Computer choice: ${computer} <br>Your choice: ${user}<br><strong>Match tie!</strong>`;
    } else if (
        (user === "rock" && computer === "scissors") ||
        (user === "paper" && computer === "rock") ||
        (user === "scissors" && computer === "paper")
    ) {
        score1++;
        info.innerHTML = `Computer choice: ${computer} <br>Your choice: ${user}<br><strong>You win!</strong>`;
        info.style.color = "green";
    } else {
        score2++;
        info.innerHTML = `Computer choice: ${computer} <br>Your choice: ${user}<br><strong>Computer wins!</strong>`;
        info.style.color = "red";
    }

    info.style.display = "block";
    playerscore.textContent = `Player Score: ${score1} points`;
    computerscore.textContent = `Computer Score: ${score2} points`;
    reset.style.display = 'inline-block';
}

rock.addEventListener('click', () => playGame('rock'));
paper.addEventListener('click', () => playGame('paper'));
scissors.addEventListener('click', () => playGame('scissors'));

reset.addEventListener('click', () => {
    score1 = 0;
    score2 = 0;
    playerscore.textContent = `Player Score: 0 points`;
    computerscore.textContent = `Computer Score: 0 points`;
    info.innerHTML = `Game reset. Choose your move!`;
    info.style.color = "black";
});