export const ROWS = 6;
export const COLS = 7;
export const PLAYER_0 = 0;
export const PLAYER_1 = 1;

let playerColors = { [PLAYER_0]: "red", [PLAYER_1]: "yellow" };

export function setPlayerColors(colors) {
    playerColors = colors;
}

export function colorOf(player) {
    return playerColors[player];
}

const boardEl = document.getElementById("board");
const turnDisc = document.getElementById("turn-disc");
const turnText = document.getElementById("turn-text");
const statusNote = document.getElementById("status-note");
const overlay = document.getElementById("overlay");
const overlayTitle = document.getElementById("overlay-title");
const opponentLabel = document.getElementById("opponent-label");

function colorClass(player) {
    return playerColors[player];
}

export function buildBoard(onColumnClick) {
    boardEl.innerHTML = "";
    for (let r = 0; r < ROWS; r++) {
        for (let c = 0; c < COLS; c++) {
            const cell = document.createElement("div");
            cell.className = "cell";
            cell.dataset.row = r;
            cell.dataset.col = c;
            cell.addEventListener("click", () => onColumnClick(c));
            boardEl.appendChild(cell);
        }
    }
}

export function renderBoard(board, animateCell = null) {
    for (let r = 0; r < ROWS; r++) {
        for (let c = 0; c < COLS; c++) {
            const cell = boardEl.querySelector(`.cell[data-row="${r}"][data-col="${c}"]`);
            cell.innerHTML = "";
            cell.classList.remove("win");

            const player = board[r][c];
            if (player === null) continue;

            const disc = document.createElement("div");
            disc.className = `disc ${colorClass(player)}`;
            if (animateCell && animateCell.row === r && animateCell.col === c) {
                disc.style.setProperty("--drop-rows", r + 1);
            } else {
                disc.style.animation = "none";
            }
            cell.appendChild(disc);
        }
    }
}

export function highlightWin(cells) {
    cells.forEach(([r, c]) =>
        boardEl.querySelector(`.cell[data-row="${r}"][data-col="${c}"]`).classList.add("win")
    );
}

export function setTurnIndicator(player, text) {
    turnDisc.className = `turn-disc ${colorClass(player)}`;
    turnText.textContent = text;
}

export function setStatus(text) {
    statusNote.textContent = text;
}

export function setOpponentLabel(text) {
    opponentLabel.textContent = text;
}

export function showOverlay(text) {
    overlayTitle.textContent = text;
    overlay.classList.remove("hidden");
}

export function hideOverlay() {
    overlay.classList.add("hidden");
}

export function onRestart(handler) {
    document.getElementById("restart-btn").addEventListener("click", handler);
    document.getElementById("play-again-btn").addEventListener("click", handler);
}
