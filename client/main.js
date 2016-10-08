"use strict";

var canvas = document.getElementById('canvas');
var ctx = canvas.getContext('2d');

var topLeft = [21, 21];

var bgColor = '#789030';
var gridProperties = {
    dirtColor: '#784800',
    wallColor: '#e0cda7',
    width: 10,
    height: 10,
    spacing: 2,
}

var unitProperties = {
    color: [
        '#ff0000',
        '#0000ff',
        '#00ff00',
    ],
    radius: 4,
}

var mapWidth = 50;
var mapHeight = 50;
console.assert(mapWidth % 2 === 0, 'mapWidth in testDraw(mapWidth, mapHeight) is not an even number');

var resolution = [
    {
        'ne': [-1, 0],
        'e': [0, 1],
        'se': [1, 0],
        'nw': [-1, -1],
        'w': [0, -1],
        'sw': [1, -1],
    },
    {
        'ne': [-1, 1],
        'e': [0, 1],
        'se': [1, 1],
        'nw': [-1, 0],
        'w': [0, -1],
        'sw': [1, 0],
    }
]

var inBoundary = function (row, col) {
    return 0 <= row && row < mapHeight
        && 0 <= col && col < mapWidth;
}

var resolve = function (row, col, direction) {
    var remainder = row % 2;
    var delta = resolution[remainder][direction];
    var newRow = row + delta[0];
    var newCol = col + delta[1];
    if(inBoundary(newRow, newCol)) {
        return [newRow, newCol]
    } else return [row, col]
}

var resolveCoordinate = function (row, col) {
    /*
     * Return relative top-left coordinate (x, y)
     */
    if(row % 2 === 0) {
        return [col * gridProperties.width + col * gridProperties.spacing, row * gridProperties.height + row * gridProperties.spacing]
    } else {
        return [col * gridProperties.width + col * gridProperties.spacing + gridProperties.width / 2, row * gridProperties.height + row * gridProperties.spacing]
    }
}

var drawUnit = function (row, col, playerId) {
    var relativeCoordinate = resolveCoordinate(row, col);
    var x1 = topLeft[0] + relativeCoordinate[0] + gridProperties.width / 2;
    var y1 = topLeft[1] + relativeCoordinate[1] + gridProperties.height / 2;
    ctx.save();
    ctx.fillStyle = unitProperties.color[playerId];
    ctx.beginPath();
    ctx.arc(x1, y1, unitProperties.radius, 0, 2*Math.PI);
    ctx.closePath();
    ctx.fill();
    ctx.restore();
}

var testDraw = function () {
    canvas.width = 640;
    canvas.height = 640;
    ctx.save();
    ctx.fillStyle = bgColor;
    ctx.fillRect(0, 0, 800, 800);
    ctx.restore();
    var wallChance = 0.05;
    for(var row = 0; row < mapHeight; ++row) {
        for(var col = 0; col < mapWidth; ++col) {
            var relativeCoordinate = resolveCoordinate(row, col);
            var x1 = topLeft[0] + relativeCoordinate[0];
            var y1 = topLeft[1] + relativeCoordinate[1];
            ctx.save();
            if(Math.random() < wallChance) {
                ctx.fillStyle = gridProperties.wallColor;
            } else ctx.fillStyle = gridProperties.dirtColor;
            ctx.fillRect(x1, y1, gridProperties.width, gridProperties.height);
            ctx.restore();
        }
    }
}

var testUnitMovementDraw = function () {
    canvas.width = 640;
    canvas.height = 640;
    ctx.save();
    ctx.fillStyle = bgColor;
    ctx.fillRect(0, 0, 800, 800);
    ctx.restore();
    var drawMap = function () {
        for(var row = 0; row < mapHeight; ++row) {
            for(var col = 0; col < mapWidth; ++col) {
                var relativeCoordinate = resolveCoordinate(row, col);
                var x1 = topLeft[0] + relativeCoordinate[0];
                var y1 = topLeft[1] + relativeCoordinate[1];
                ctx.save();
                ctx.fillStyle = gridProperties.dirtColor;
                ctx.fillRect(x1, y1, gridProperties.width, gridProperties.height);
                ctx.restore();
            }
        }
    }
    var position = [2, 10];
    var orders = ['ne', 'ne', 'ne', 'ne', 'e', 'e', 'e', 'se', 'se', 'se', 'sw', 'sw', 'sw', 'w', 'w', 'w', 'nw', 'nw', 'nw'];
    var drawDelay = 500;
    orders.forEach(function (direction, index) {
        setTimeout(function () {
            drawMap();
            drawUnit(position[0], position[1], 0);
            position = resolve(position[0], position[1], direction);
        }, index * drawDelay)
    })
}

document.addEventListener('DOMContentLoaded', function (event) {
    // testDraw();
    // testUnitMovementDraw();
})