const input = document.getElementById("user-input");
const chatBox = document.getElementById("chat-box");
const historyList = document.getElementById("history-list");

function escapeHtml(text) {
    const div = document.createElement("div");
    div.textContent = text;
    return div.innerHTML;
}

function addMessage(text, sender, sources = []) {
    const row = document.createElement("div");
    row.classList.add("message-row", sender === "user" ? "user-row" : "bot-row");

    if (sender === "bot") {
        const avatar = document.createElement("div");
        avatar.className = "avatar bot-avatar";
        avatar.textContent = "IA";
        row.appendChild(avatar);
    }

    const message = document.createElement("div");
    message.classList.add("message", sender === "user" ? "user-message" : "bot-message");

    let html = escapeHtml(text).replace(/\n/g, "<br>");

    if (sender === "bot" && sources && sources.length > 0) {
        const sourceNames = [...new Set(sources.map(src => src.source))];
        html += `<div class="sources">Sources : ${sourceNames.join(", ")}</div>`;
    }

    message.innerHTML = html;
    row.appendChild(message);
    chatBox.appendChild(row);
    chatBox.scrollTop = chatBox.scrollHeight;
}

function showLoader() {
    const row = document.createElement("div");
    row.classList.add("message-row", "bot-row");
    row.id = "loader-row";

    const avatar = document.createElement("div");
    avatar.className = "avatar bot-avatar";
    avatar.textContent = "IA";

    const message = document.createElement("div");
    message.classList.add("message", "bot-message");
    message.innerHTML = `
        <div class="typing">
            <span></span><span></span><span></span>
        </div>
    `;

    row.appendChild(avatar);
    row.appendChild(message);
    chatBox.appendChild(row);
    chatBox.scrollTop = chatBox.scrollHeight;
}

function removeLoader() {
    const loader = document.getElementById("loader-row");
    if (loader) loader.remove();
}

function addToHistory(question) {
    if (!historyList) return;

    const item = document.createElement("button");
    item.className = "history-item";
    item.textContent = question.length > 44 ? question.slice(0, 44) + "..." : question;

    item.addEventListener("click", () => {
        input.value = question;
        input.focus();
    });

    historyList.prepend(item);

    while (historyList.children.length > 6) {
        historyList.removeChild(historyList.lastChild);
    }
}

async function sendMessage() {
    const question = input.value.trim();
    if (!question) return;

    addMessage(question, "user");
    addToHistory(question);
    input.value = "";
    showLoader();

    try {
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), 60000);

        const response = await fetch("/ask/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ question: question }),
            signal: controller.signal
        });

        clearTimeout(timeoutId);

        const data = await response.json();
        removeLoader();

        if (response.ok && data.answer) {
            addMessage(data.answer, "bot", data.sources || []);
        } else {
            addMessage(data.error || "Erreur côté serveur", "bot");
        }
    } catch (error) {
        removeLoader();

        if (error.name === "AbortError") {
            addMessage("La requête a pris trop de temps. Réessaie.", "bot");
        } else {
            addMessage("Erreur de connexion", "bot");
        }

        console.error(error);
    }
}

async function clearChat() {
    try {
        await fetch("/clear/", {
            method: "POST"
        });
    } catch (error) {
        console.error(error);
    }

    chatBox.innerHTML = `
        <div class="message-row bot-row">
            <div class="avatar bot-avatar">IA</div>
            <div class="message bot-message">
                👋 Nouvelle conversation démarrée !
            </div>
        </div>
    `;
}

if (input) {
    input.addEventListener("keypress", function (event) {
        if (event.key === "Enter") {
            sendMessage();
        }
    });
}