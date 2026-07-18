import * as api from "./api.js";

const opponentList = document.getElementById("opponent-list");
const aiBtn = document.getElementById("mode-ai-btn");
const aivaiBtn = document.getElementById("mode-aivai-btn");
const aiPicker = document.getElementById("ai-picker");
const aivaiPicker = document.getElementById("aivai-picker");

const FALLBACK_AIS = [{ name: "Random", description: "Chooses a random valid column." }];

let ais = [];

function fillSelect(select) {
    select.innerHTML = "";
    for (const ai of ais) {
        const option = document.createElement("option");
        option.value = ai.name.toLowerCase();
        option.textContent = ai.name;
        select.appendChild(option);
    }
}

function bindDescription(selectId, descId) {
    const select = document.getElementById(selectId);
    const desc = document.getElementById(descId);
    const update = () => {
        const selected = ais[select.selectedIndex];
        desc.textContent = selected ? selected.description : "";
    };
    select.addEventListener("change", update);
    update();
}

async function loadAis() {
    try {
        ais = (await api.getAis()).ais;
    } catch (err) {
        ais = FALLBACK_AIS;
    }

    for (const id of ["ai-select", "ai1-select", "ai2-select"]) {
        fillSelect(document.getElementById(id));
    }
    bindDescription("ai-select", "ai-desc");
    bindDescription("ai1-select", "ai1-desc");
    bindDescription("ai2-select", "ai2-desc");
}

function showPicker(picker) {
    opponentList.classList.add("hidden");
    picker.classList.remove("hidden");
}

function showMenu() {
    aiPicker.classList.add("hidden");
    aivaiPicker.classList.add("hidden");
    opponentList.classList.remove("hidden");
}

aiBtn.addEventListener("click", () => showPicker(aiPicker));
aivaiBtn.addEventListener("click", () => showPicker(aivaiPicker));

for (const btn of document.querySelectorAll("[data-back]")) {
    btn.addEventListener("click", showMenu);
}

document.getElementById("play-ai-btn").addEventListener("click", () => {
    const ai = document.getElementById("ai-select").value;
    const order = document.getElementById("order-select").value;
    window.location.href =
        `/game?mode=ai&ai=${encodeURIComponent(ai)}&order=${order}`;
});

document.getElementById("play-aivai-btn").addEventListener("click", () => {
    const ai1 = document.getElementById("ai1-select").value;
    const ai2 = document.getElementById("ai2-select").value;
    window.location.href =
        `/game?mode=aivai&ai1=${encodeURIComponent(ai1)}&ai2=${encodeURIComponent(ai2)}`;
});

loadAis();
