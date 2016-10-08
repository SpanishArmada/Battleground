"use strict";

/* http://stackoverflow.com/a/14388512 */
var replayData = null;
var ws = new WebSocket("ws://localhost:8888/ws");
        var client_id;
        console.log("INSIDE simulation")
        ws.onopen = function() {
            console.log("Connection open")
            ws.send(JSON.stringify({type: 3}));
        };
        ws.onmessage = function (evt) {
            console.log(evt)
            console.log(evt.data)
            var data = JSON.parse(evt.data);
            if(data.type == 0) {
                client_id = data.client_id; 
            }
            if(data.type == 1) {
                replayData = JSON.parse(data.jsonData)
                playReplay()
            }
        };

        window.onbeforeunload = function() {
            ws.send(JSON.stringify({type: 1, client_id: client_id}));
            ws.onclose = function () {}; // disable onclose handler first
            ws.close()
        };

var fetchJSONFile = function (path, callback) {
    var httpRequest = new XMLHttpRequest();
    httpRequest.onreadystatechange = function() {
        if (httpRequest.readyState === 4) {
            if (httpRequest.status === 200) {
                var data = JSON.parse(httpRequest.responseText);
                if (callback) callback(data);
            }
        }
    };
    httpRequest.open('GET', path);
    httpRequest.send(); 
}

var canvas = document.getElementById('canvas');
var ctx = canvas.getContext('2d');

var topLeft = [51, 51];

// var bgColor = '#789030';
var bgColor = '#000000';
var gridProperties = {
    dirtColor: '#703500',
    wallColor: '#000000',
    fogColor: '#666666',
    width: 16,
    height: 16,
    spacing: 2,
    EMPTY: 0,
    WALL: 1,
    HIVE: 9,
}

var unitProperties = {
    color: [
        '#ff0000',
        '#0000ff',
        '#00ff00',
    ],
    radius: 4,
}

var hiveProperties = {
    color: [
        '#7f7f7f',
        '#7f0000',
        '#00007f',
        '#007f00',
    ],
    radius: 6,
    border: 4,
}

var mapWidth = 4;
var mapHeight = 4;
var map = [];

var directions = ['ne', 'e', 'se','sw', 'w', 'nw'];
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

var perspective = -1;
// var replayData = {
//     map: [[0,0,0,0], [0,0,0,0], [0,0,0,0], [0,0,0,0]],
//     turnData: [
//         {
//             unitData: [],
//             baseData: [[0,0,0],[3,3,1],[3,0,-1],[0,3,-1]],
//         },
//         {
//             unitData: [[0,0,0],[3,3,1]],
//             baseData: [[0,0,0],[3,3,1],[3,0,-1],[0,3,-1]],
//         },
//         {
//             unitData: [[0,1,0],[3,2,1]],
//             baseData: [[0,0,0],[3,3,1],[3,0,-1],[0,3,-1]],
//         },
//         {
//             unitData: [[1,0,0],[3,1,1],[0,0,0],[3,3,1]],
//             baseData: [[0,0,0],[3,3,1],[3,0,-1],[0,3,-1]],
//         },
//     ]
// };

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

var drawEmpty = function (row, col) {
    var relativeCoordinate = resolveCoordinate(row, col);
    var x1 = topLeft[0] + relativeCoordinate[0];
    var y1 = topLeft[1] + relativeCoordinate[1];
    ctx.save();
    ctx.fillStyle = gridProperties.dirtColor;
    ctx.fillRect(x1, y1, gridProperties.width, gridProperties.height);
    ctx.restore();
}

var drawWall = function (row, col) {
    var relativeCoordinate = resolveCoordinate(row, col);
    var x1 = topLeft[0] + relativeCoordinate[0];
    var y1 = topLeft[1] + relativeCoordinate[1];
    ctx.save();
    ctx.fillStyle = gridProperties.wallColor;
    ctx.fillRect(x1, y1, gridProperties.width, gridProperties.height);
    ctx.restore();
}

var drawHive = function (row, col, playerId) {
    playerId = (typeof playerId === 'undefined' || playerId === -1 ? 0 : playerId);
    var relativeCoordinate = resolveCoordinate(row, col);
    var x1 = topLeft[0] + relativeCoordinate[0];
    var y1 = topLeft[1] + relativeCoordinate[1];
    var xCenter = topLeft[0] + relativeCoordinate[0] + gridProperties.width / 2;
    var yCenter = topLeft[1] + relativeCoordinate[1] + gridProperties.height / 2;
    ctx.save();
    ctx.fillStyle = gridProperties.dirtColor;
    ctx.fillRect(x1, y1, gridProperties.width, gridProperties.height);
    ctx.lineWidth = hiveProperties.border;
    ctx.fillStyle = '#000000';
    ctx.strokeStyle = hiveProperties.color[playerId];
    ctx.lineWidth = hiveProperties.border;
    ctx.beginPath();
    ctx.arc(xCenter, yCenter, hiveProperties.radius, 0, 2*Math.PI);
    ctx.closePath();
    ctx.fill()
    ctx.stroke();
    ctx.restore();
}

var drawMap = function (objects) {
    ctx.save();
    ctx.fillStyle = '#000000';
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    ctx.restore();
    for(var row = 0; row < mapHeight; ++row) {
        for(var col = 0; col < mapWidth; ++col) {
            var gridType = map[row][col];
            if(gridType === gridProperties.WALL) {
                drawWall(row, col)
            } else if(gridType === gridProperties.EMPTY) {
                drawEmpty(row, col)
            } else if(gridType >= HIVE) {
                drawHive(row, col, gridType - HIVE);
            }
        }
    }

    if(typeof objects === 'undefined') {
        return;
    }

    objects.baseData.forEach(function (base, index) {
        var baseRow = base[0];
        var baseCol = base[1];
        var playerId = base[2]
            // This is fucking retarded
            +1;
        drawHive(baseRow, baseCol, playerId)
    })

    objects.unitData.forEach(function (unit, index) {
        var unitRow = unit[0];
        var unitCol = unit[1];
        var playerId = unit[2];
        drawUnit(unitRow, unitCol, playerId)
    })
}

var playReplay = function () {
    map = replayData.map;
    drawMap();
    var drawInterval = 450;
    replayData.turnData.forEach(function (objects, index) {
        setTimeout(function() {
            drawMap(objects);
        }, index * drawInterval + drawInterval);
    })
}

var test = (function () {
    var mapWidth = 30;
    var mapHeight = 30;
    var topLeft = [51, 51];

    var testDraw = function () {
        canvas.width = 640;
        canvas.height = 640;
        ctx.save();
        ctx.fillStyle = bgColor;
        ctx.fillRect(0, 0, 800, 800);
        ctx.restore();
        var wallChance = 0.07;
        var hiveChance = wallChance + 0.002;
        for(var row = 0; row < mapHeight; ++row) {
            for(var col = 0; col < mapWidth; ++col) {
                var relativeCoordinate = resolveCoordinate(row, col);
                var x1 = topLeft[0] + relativeCoordinate[0];
                var y1 = topLeft[1] + relativeCoordinate[1];
                ctx.save();
                var roll = Math.random();
                if(roll < wallChance) {
                    ctx.fillStyle = gridProperties.wallColor;
                    ctx.fillRect(x1, y1, gridProperties.width, gridProperties.height);
                } else if(roll < hiveChance) {
                    drawHive(row, col);
                }
                else {
                    ctx.fillStyle = gridProperties.dirtColor;
                    ctx.fillRect(x1, y1, gridProperties.width, gridProperties.height);
                }
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
        drawMap();
        drawUnit(position[0], position[1], 0);
        var orders = ['ne', 'ne', 'ne', 'e', 'e', 'e', 'se', 'se', 'se', 'sw', 'sw', 'sw', 'w', 'w', 'w', 'nw', 'nw', 'nw'];
        var drawInterval = 450;
        orders.forEach(function (direction, index) {
            setTimeout(function () {
                position = resolve(position[0], position[1], direction);
                drawMap();
                drawUnit(position[0], position[1], 0);
            }, (index + 1) * drawInterval)
        })
    }

    return {
        draw: testDraw,
        unitMovementDraw: testUnitMovementDraw,
    }
})();

document.addEventListener('DOMContentLoaded', function (event) {
    canvas.width = 640;
    canvas.height = 640;
    // test.draw();
    // test.unitMovementDraw();
    // drawMap();
    // playReplay();
})
