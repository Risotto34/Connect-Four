async function post(url, body) {
    const res = await fetch(url, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: body === undefined ? null : JSON.stringify(body),
    });
    if (!res.ok) throw new Error(`${url} failed with status ${res.status}`);
    return res.json();
}

async function get(url) {
    const res = await fetch(url);
    if (!res.ok) throw new Error(`${url} failed with status ${res.status}`);
    return res.json();
}

export function newGame() {
    return post("/api/new-game");
}

export function chooseAi(ai) {
    return post("/api/choose-ai", { ai });
}

export function userPlay(column) {
    return post("/api/user-play", { column });
}

export function aiPlay() {
    return post("/api/ai-play");
}

export function getBoard() {
    return get("/api/board");
}

export function getAis() {
    return get("/api/ais");
}
