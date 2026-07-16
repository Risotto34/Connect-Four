const ROWS = 6;
const COLS = 7;
const EMPTY = 0, RED = 1, YELLOW = 2;

const params = new URLSearchParams(window.location.search);
const mode = params.get("mode") || "pvp";       // "pvp" | "ai"
const aiName = params.get("ai") || "random";    // which AI to fight

const AI_LABELS = {
    random: "🎲 Randy the Random",
    minimax: "🧠 Minimax",
    neural: "🤖 Neural Net",
};

const boardEl = document.getElementById("board");
const turnDisc = document.getElementById("turn-disc");
const turnText = document.getElementById("turn-text");
const statusNote = document.getElementById("status-note");
const overlay = document.getElementById("overlay");
const overlayTitle = document.getElementById("overlay-title");
const opponentLabel = document.getElementById("opponent-label");

let board, current, gameOver, locked;

opponentLabel.textContent =
    mode === "ai" ? `You (Red) vs ${AI_LABELS[aiName] || aiName}` : "Red vs Yellow — local game";

function initGame() {
    board = Array.from({ length: ROWS }, () => Array(COLS).fill(EMPTY));
    current = RED;
    gameOver = false;
    locked = false;
    statusNote.textContent = "";
    overlay.classList.add("hidden");
    renderBoard();
    updateTurnIndicator();
}

function renderBoard() {
    boardEl.innerHTML = "";
    for (let r = 0; r < ROWS; r++) {
        for (let c = 0; c < COLS; c++) {
            const cell = document.createElement("div");
            cell.className = "cell";
            cell.dataset.row = r;
            cell.dataset.col = c;
            cell.addEventListener("click", () => handleColumnClick(c));
            cell.addEventListener("mouseenter", () => highlightColumn(c, true));
            cell.addEventListener("mouseleave", () => highlightColumn(c, false));
            boardEl.appendChild(cell);
        }
    }
}

function highlightColumn(col, on) {
    if (gameOver || locked) on = false;
    boardEl.querySelectorAll(`.cell[data-col="${col}"]`).forEach((cell) => {
        const r = +cell.dataset.row;
        cell.classList.toggle("col-hover", on && board[r][col] === EMPTY);
    });
}

function lowestEmptyRow(col) {
    for (let r = ROWS - 1; r >= 0; r--) {
        if (board[r][col] === EMPTY) return r;
    }
    return -1;
}

function placeDisc(col, player) {
    const row = lowestEmptyRow(col);
    if (row === -1) return null;
    board[row][col] = player;

    const cell = boardEl.querySelector(`.cell[data-row="${row}"][data-col="${col}"]`);
    const disc = document.createElement("div");
    disc.className = `disc ${player === RED ? "red" : "yellow"}`;
    disc.style.setProperty("--drop-rows", row + 1);
    cell.appendChild(disc);
    return row;
}

function handleColumnClick(col) {
    if (gameOver || locked) return;
    const row = placeDisc(col, current);
    if (row === null) return;
    afterMove(row, col);
}

function afterMove(row, col) {
    const winCells = checkWin(row, col);
    if (winCells) {
        gameOver = true;
        winCells.forEach(([r, c]) =>
            boardEl.querySelector(`.cell[data-row="${r}"][data-col="${c}"]`).classList.add("win")
        );
        showOverlay(winnerLabel(current) + " wins! 🎉");
        return;
    }
    if (board[0].every((v) => v !== EMPTY) && board.flat().every((v) => v !== EMPTY)) {
        gameOver = true;
        showOverlay("It's a draw! 🤝");
        return;
    }

    current = current === RED ? YELLOW : RED;
    updateTurnIndicator();

    if (mode === "ai" && current === YELLOW) {
        aiTurn();
    }
}

function winnerLabel(player) {
    if (mode === "ai") return player === RED ? "You" : AI_LABELS[aiName] || "AI";
    return player === RED ? "Red" : "Yellow";
}

async function aiTurn() {
    locked = true;
    statusNote.textContent = "AI is thinking…";
    let col = null;
    try {
        const res = await fetch("/api/move", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ board, ai: aiName, player: YELLOW }),
        });
        if (res.ok) {
            const data = await res.json();
            if (Number.isInteger(data.column)) col = data.column;
        }
    } catch (_) {
        /* backend not ready yet — fall back below */
    }

    if (col === null || lowestEmptyRow(col) === -1) {
        // Fallback: random valid column, so the frontend is testable without the AI backend
        const valid = [];
        for (let c = 0; c < COLS; c++) if (lowestEmptyRow(c) !== -1) valid.push(c);
        col = valid[Math.floor(Math.random() * valid.length)];
        statusNote.textContent = "⚠ AI backend unavailable — playing a random move.";
    } else {
        statusNote.textContent = "";
    }

    // Small delay so the AI move feels natural
    setTimeout(() => {
        locked = false;
        const row = placeDisc(col, current);
        if (row !== null) afterMove(row, col);
    }, 450);
}

function checkWin(row, col) {
    const player = board[row][col];
    const dirs = [ [0, 1], [1, 0], [1, 1], [1, -1] ];
    for (const [dr, dc] of dirs) {
        const cells = [[row, col]];
        for (const sign of [1, -1]) {
            let r = row + dr * sign, c = col + dc * sign;
            while (r >= 0 && r < ROWS && c >= 0 && c < COLS && board[r][c] === player) {
                cells.push([r, c]);
                r += dr * sign;
                c += dc * sign;
            }
        }
        if (cells.length >= 4) return cells;
    }
    return null;
}

function updateTurnIndicator() {
    const isRed = current === RED;
    turnDisc.className = `turn-disc ${isRed ? "red" : "yellow"}`;
    turnText.textContent =
        mode === "ai"
            ? isRed ? "Your turn" : "AI's turn"
            : isRed ? "Red's turn" : "Yellow's turn";
}

function showOverlay(text) {
    overlayTitle.textContent = text;
    overlay.classList.remove("hidden");
}

document.getElementById("restart-btn").addEventListener("click", initGame);
document.getElementById("play-again-btn").addEventListener("click", initGame);

initGame();
