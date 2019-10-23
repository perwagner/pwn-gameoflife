var socket = io();
socket.on('connect', function() {
    socket.emit('connectionEstablished', {data: 'Game of life connection established'});
});

var canvas, canvasContext;
var mouseX, mouseY;
var cellSize = 25;

var canvasPaddingX = 50;
var canvasPaddingY = 112;




window.onload = function() {
    canvas = document.getElementById("GameCanvas");
    canvasContext = canvas.getContext("2d");

    canvasContext.fillStyle = "#e0e0eb ";
    canvasContext.fillRect(0, 0, canvas.width, canvas.height);

    canvas.addEventListener("mousedown", clickCell, false);

    drawGrid(canvasContext, canvas.width, canvas.height);
}

window.setInterval(function(){
    socket.emit('updateTurn', {data: "update the turn"});
  }, 1000);


function drawGrid(context, canvasWidth, canvasHeight) {
    for (var x = 0; x <= canvasWidth; x += cellSize) {
        context.moveTo(x, 0);
        context.lineTo(x, canvasHeight);
    }

    for (var x = 0; x <= canvasHeight; x += cellSize) {
        context.moveTo(0, x);
        context.lineTo(canvasWidth, x);
    }

    context.strokeStyle = "black";
    context.stroke()
}


function getMousePos(canvas, event) {
    var rect = canvas.getBoundingClientRect();
    return {
      x: event.clientX - rect.left,
      y: event.clientY - rect.top
    };
  }


function clickCell(event) {
    var mousePosition = getMousePos(canvas, event);
    x = mousePosition.x;
    y = mousePosition.y;

    var cell = getCellFromCoordinates(x, y);
    cellX = cell[0];
    cellY = cell[1];

    socket.emit('cellClick', {data: "", cellX: cellX, cellY, cellY});

    colorCell(cellX, cellY, "#444444")
}

function getCellFromCoordinates(x, y) {
    cellX = Math.floor(x / cellSize) + 1;
    cellY = Math.floor(y / cellSize) + 1;

    return [cellX, cellY];
}

function getCellCoordinates(cellX, cellY) {
    var x = (cellX - 1) * cellSize;
    var y = (cellY - 1) * cellSize;

    return [x, y];
}

function colorCell(cellX, cellY, color) {
    var cellCoordinates = getCellCoordinates(cellX, cellY);

    var x = cellCoordinates[0];
    var y = cellCoordinates[1];

    canvasContext.fillStyle = color;
    canvasContext.fillRect(x, y, cellSize, cellSize);
}

function restartGame() {
    socket.emit('restartGame');
}