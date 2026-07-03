const askBtn = document.getElementById("askBtn");
const questionBox = document.getElementById("question");
const answerBox = document.getElementById("answer");

let startTime = 0;

// Ask AI
askBtn.addEventListener("click", async () => {

    const question = questionBox.value.trim();

    if (question === "") {
        alert("Please enter a research question.");
        return;
    }

    // Start timer
    startTime = performance.now();

    // Disable button
    askBtn.disabled = true;
    askBtn.innerHTML = "⏳ Generating...";

    // Loading Animation
    answerBox.innerHTML = `
        <div class="loading">
            <div class="loader"></div>

            <h3>🤖 Gemini AI is Thinking...</h3>

            <p>
                Please wait while your research report is being generated.
            </p>
        </div>
    `;

    try {

        const response = await fetch("/ask", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                question: question
            })

        });

        const data = await response.json();

        answerBox.innerHTML = marked.parse(data.answer);

        // Response Time
        const endTime = performance.now();

        const seconds = ((endTime - startTime) / 1000).toFixed(2);

        // Word Count
        const words = answerBox.innerText
            .trim()
            .split(/\s+/)
            .length;

        answerBox.innerHTML += `

        <hr>

        <div class="stats">

            <h3>📊 Research Statistics</h3>

            <p><b>Words:</b> ${words}</p>

            <p><b>Generated In:</b> ${seconds} sec</p>

            <p><b>Model:</b> Gemini 2.5 Flash</p>

        </div>

        `;

        // Smooth Scroll
        answerBox.scrollIntoView({
            behavior: "smooth"
        });

    }

    catch (error) {

        answerBox.innerHTML = `

        <h2 style="color:red;">
            ❌ Error
        </h2>

        <p>${error}</p>

        `;

    }

    finally {

        askBtn.disabled = false;

        askBtn.innerHTML = "🚀 Ask AI";

    }

});

// Copy Answer
document.getElementById("copyBtn").onclick = () => {

    navigator.clipboard.writeText(answerBox.innerText);

    alert("✅ Answer Copied!");

};

// Download PDF
document.getElementById("pdfBtn").onclick = () => {

    window.location.href = "/download_pdf";

};

// Enter Key Support
questionBox.addEventListener("keydown", function (e) {

    if (e.key === "Enter" && !e.shiftKey) {

        e.preventDefault();

        askBtn.click();

    }

});

// Suggested Topics

document.querySelectorAll(".topic").forEach(button => {

    button.addEventListener("click", () => {

        questionBox.value = button.innerText;

        questionBox.focus();

    });

});