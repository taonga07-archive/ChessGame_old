// Get a reference to the chess board element
const chessBoard = document.querySelector('.chess-board');

// Add squares to the chess board
for (let i = 0; i < 64; i++) {
    const square = document.createElement('div');
    square.classList.add('square');
  chessBoard.appendChild(square);
}