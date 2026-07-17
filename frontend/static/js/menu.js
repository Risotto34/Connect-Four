import * as api from "./api.js";

const aiBtn = document.getElementById("mode-ai-btn");
const picker = document.getElementById("ai-picker");
const select = document.getElementById("ai-select");
const desc = document.getElementById("ai-desc");
const playBtn = document.getElementById("play-ai-btn");

const FALLBACK_AIS = [{ name: "Random", description: "Chooses a random valid column." }];

let ais = [];

async function loadAis() {
    try {
        ais = (await api.getAis()).ais;
    } catch (err) {
        ais = FALLBACK_AIS;
    }

    select.innerHTML = "";
    for (const ai of ais) {
        const option = document.createElement("option");
        option.value = ai.name.toLowerCase();
        option.textContent = ai.name;
        select.appendChild(option);
    }
    updateDescription();
}

function updateDescription() {
    const selected = ais[select.selectedIndex];
    desc.textContent = selected ? selected.description : "";
}

aiBtn.addEventListener("click", () => {
    picker.classList.toggle("hidden");
});

select.addEventListener("change", updateDescription);

playBtn.addEventListener("click", () => {
    const order = document.getElementById("order-select").value;
    const color = document.getElementById("color-select").value;
    window.location.href =
        `/game?mode=ai&ai=${encodeURIComponent(select.value)}&order=${order}&color=${color}`;
});

loadAis();
