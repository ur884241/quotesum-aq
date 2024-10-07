export function loadHomePage() {
    return `
        <div class="container">
            <div class="title-container">
                <canvas id="titleCanvas"></canvas>
            </div>
            <div class="ascii-art" id="ascii-sigil"></div>
            <input type="text" id="urlInput" placeholder="Enter URL of .txt file">
            <div class="file-upload">
                <label for="fileInput" class="file-label">Upload a file (PDF or TXT)</label>
                <input type="file" id="fileInput" accept=".pdf,.txt">
            </div>
            <input type="number" id="targetSum" placeholder="Enter target sum" required>
            <button onclick="searchQuotes()">Invoke</button>
            <div id="results"></div>
        </div>
    `;
}