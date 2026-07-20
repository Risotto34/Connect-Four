import * as api from "./api.js";
import * as ui from "./ui.js";

const params = new URLSearchParams(window.location.search);
const mode = params.get("mode") || "pvp";
const aiName = params.get("ai") || "random";
const order = params.get("order") || "first";
const aiNames = [params.get("ai1") || "random", params.get("ai2") || "random"];

let humanPlayer;
let aiPlayer;
let aiOf = {};

let board;
let current;
let gameOver;
let locked;

function colorName(player) {
    const color = ui.colorOf(player);
    return color.charAt(0).toUpperCase() + color.slice(1);
}

async function initGame() {
    gameOver = false;
    locked = false;
    current = ui.PLAYER_0;

    ui.hideResult();
    ui.setStatus("");
    ui.buildBoard(handleColumnClick);
    updateTurnIndicator();

    try {
        await api.newGame();
        if (mode === "ai") {
            const res = await api.chooseAi(aiName);
            if (!res.success) {
                ui.setStatus(`⚠ This AI is not available yet: ${aiName}`);
                locked = true;
                return;
            }
        }
        const state = await api.getBoard();
        board = state.board;
        current = state.currentPlayer;
        ui.setPlayerColors({ [current]: "red", [1 - current]: "yellow" });

        if (mode === "ai") {
            humanPlayer = order === "first" ? current : 1 - current;
            aiPlayer = 1 - humanPlayer;
        } else if (mode === "aivai") {
            humanPlayer = null;
            aiOf = { [current]: aiNames[0], [1 - current]: aiNames[1] };
        } else {
            humanPlayer = current;
            aiPlayer = 1 - current;
        }

        ui.setOpponentLabel(
            mode === "ai"
                ? `You (${colorName(humanPlayer)}, ${order}) vs ${aiName}`
                : mode === "aivai"
                    ? `${aiNames[0]} (${colorName(current)}) vs ${aiNames[1]} (${colorName(1 - current)})`
                    : "Red vs Yellow — local game"
        );

        ui.renderBoard(board);
        updateTurnIndicator();
        if (mode === "ai" && current === aiPlayer) {
            await aiTurn();
        } else if (mode === "aivai") {
            locked = true;
            await aivaiLoop();
        }

    } catch (err) {
        ui.setStatus("⚠ Could not reach the server.");
        locked = true;
    }
}

async function handleColumnClick(col) {
    if (gameOver || locked) return;
    if (mode === "ai" && current !== humanPlayer) return;
    locked = true;

    const finished = await playMove(() => api.userPlay(col));
    if (finished) return;

    if (mode === "ai" && current === aiPlayer) {
        await aiTurn();
    } else {
        locked = false;
    }
}

async function aiTurn() {
    ui.setStatus("AI is thinking…");
    await new Promise((resolve) => setTimeout(resolve, 450));

    const finished = await playMove(() => api.aiPlay());
    if (!finished) {
        ui.setStatus("");
        locked = false;
    }
}

async function aivaiLoop() {
    while (!gameOver) {
        ui.setStatus(`${aiOf[current]} is thinking…`);
        await new Promise((resolve) => setTimeout(resolve, 450));

        try {
            const res = await api.chooseAi(aiOf[current], current);
            if (!res.success) {
                ui.setStatus(`⚠ This AI is not available yet: ${aiOf[current]}`);
                return;
            }
        } catch (err) {
            ui.setStatus("⚠ Could not reach the server.");
            return;
        }

        const finished = await playMove(() => api.aiPlay(current));
        if (finished) return;
        ui.setStatus("");
    }
}

async function playMove(request) {
    let data;
    try {
        data = await request();
    } catch (err) {
        ui.setStatus("⚠ Could not reach the server.");
        locked = false;
        return true;
    }

    if (!data.success) {
        locked = false;
        return true;
    }

    const newBoard = data.board.board;
    ui.renderBoard(newBoard, findNewDisc(board, newBoard));
    board = newBoard;
    current = data.board.currentPlayer;

    if (data.winner) {
        const winner = 1 - current;
        gameOver = true;
        ui.setStatus("");
        ui.highlightWin(findWinCells(board, winner));
        ui.showResult(winnerLabel(winner) + " wins! 🎉");
        return true;
    }
    if (data.draw) {
        gameOver = true;
        ui.setStatus("");
        ui.showResult("It's a draw! 🤝");
        return true;
    }

    updateTurnIndicator();
    return false;
}

function findNewDisc(oldBoard, newBoard) {
    for (let r = 0; r < ui.ROWS; r++) {
        for (let c = 0; c < ui.COLS; c++) {
            if (newBoard[r][c] !== null && (!oldBoard || oldBoard[r][c] === null)) {
                return { row: r, col: c };
            }
        }
    }
    return null;
}

function findWinCells(board, player) {
    const dirs = [ [0, 1], [1, 0], [1, 1], [1, -1] ];
    for (let r = 0; r < ui.ROWS; r++) {
        for (let c = 0; c < ui.COLS; c++) {
            if (board[r][c] !== player) continue;
            for (const [dr, dc] of dirs) {
                const cells = [];
                for (let i = 0; i < 4; i++) {
                    const rr = r + dr * i, cc = c + dc * i;
                    if (rr < 0 || rr >= ui.ROWS || cc < 0 || cc >= ui.COLS) break;
                    if (board[rr][cc] !== player) break;
                    cells.push([rr, cc]);
                }
                if (cells.length === 4) return cells;
            }
        }
    }
    return [];
}

function winnerLabel(player) {
    if (mode === "aivai") {
        return `${aiOf[player]} (${colorName(player)})`;
    }
    return colorName(player);
}

function updateTurnIndicator() {
    const text =
        mode === "ai"
            ? current === humanPlayer ? "Your turn" : "AI's turn"
            : mode === "aivai"
                ? `${aiOf[current]}'s turn`
                : `${colorName(current)}'s turn`;
    ui.setTurnIndicator(current, text);
}

ui.onRestart(initGame);
initGame();
