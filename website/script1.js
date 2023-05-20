var colour_selctor1 = document.getElementById("colour_selector1");
var colour_selctor2 = document.getElementById("colour_selector2");
var board = document.getElementById("game_board");

var interactive_board;

board.addEventListener("load",function(){
    interactive_board = board.contentDocument;
    change_square_color(colour_selctor1.value, 0);
    change_square_color(colour_selctor2.value, 1);
})

function change_square_color(colour, square_type){
    var square_types = {
        0: interactive_board.querySelectorAll('.white_square'),
        1: interactive_board.querySelectorAll('.black_square'),
    };
    var squares = square_types[square_type];
    squares.forEach(square => {square.style.fill = colour;});
};

// function addChessPieceToBoard(chessPieceId, squareId) {
//     fetch('pieces.svg')
//       .then(response => response.text())
//       .then(svgString => {
//         const parser = new DOMParser();
//         const svgDoc = parser.parseFromString(svgString, 'image/svg+xml');
//         const chessPieceElement = svgDoc.getElementById(chessPieceId);
//         const squareElement = interactive_board.getElementById(squareId);

//         interactive_board.documentElement.appendChild(chessPieceElement);
  
//         const { width: sWidth, height: sHeight, x: sX, y: sY } = squareElement.getBoundingClientRect();
//         const { width: pWidth, height: pHeight, x: pX, y: pY } = chessPieceElement.getBoundingClientRect();
//         const translateX = sX - pX + (sWidth - pWidth) / 2;
//         const translateY = sY - pY + (sHeight - pHeight) / 2;
//         console.log(sX, sY, pX, pY, translateX, translateY);
//         chessPieceElement.style.transform = `trranslate(${translateX}px, ${translateY}px) scale(${sWidth / pWidth}, ${sHeight / pHeight})`;
//       });
//   }
//scale(0.0146712, 0.0159746) translate(-2150.744px, 8748.957px)
function addChessPieceToBoard(chessPieceId, squareId) {
  fetch('pieces.svg')
    .then(response => response.text())
    .then(svgString => {
      const parser = new DOMParser();
      const svgDoc = parser.parseFromString(svgString, 'image/svg+xml');
      const chessPieceElement = svgDoc.getElementById(chessPieceId);
      const squareElement = interactive_board.getElementById(squareId);

      interactive_board.documentElement.appendChild(chessPieceElement);

      // Get the bounding client rects for the square element and chess piece element
      const square = squareElement.getBoundingClientRect();
      const piece = chessPieceElement.getBoundingClientRect();

      // Set the scaling transformation
      chessPieceElement.setAttribute('transform', `scale(${square.width / piece.width}, ${square.height / piece.height})`);

      // // Get the updated bounding client rect of the chess piece element after scaling
      // const updatedPRect = chessPieceElement.getBoundingClientRect();

      // // Calculate the translation values needed to move the chess piece element to the bottom right corner of the square element
      // const translateX = sX - updatedPRect.x + (sWidth - updatedPRect.width) / 2;
      // const translateY = sY - updatedPRect.y + (sHeight - updatedPRect.height) / 2;
      // const currentTransform = chessPieceElement.style.transform;

      // console.log(translateX, translateY, updatedPRect.x, updatedPRect.y)

      // // Use the translate values to move the chess piece element to the bottom right corner of the square element
      // chessPieceElement.style.transform = `${currentTransform} translate(${translateX}px, ${translateY}px)`;
    });
}
  