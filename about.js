export function loadAboutPage() {
    return `
        <style>
            .about-container {
                max-width: 800px;
                margin: 0 auto;
                padding: 20px;
                font-family: Arial, sans-serif;
                line-height: 1.6;
                text-align: justify;
                color: #333;
            }
        </style>

        <div class="about-container" id="about-content">
            <p>Loading content...</p>
        </div>

        <script>
            // Fetch and display the content from the .txt file
            fetch('/aboutContent.txt')
                .then(response => response.text())
                .then(data => {
                    document.getElementById('about-content').innerHTML = '<pre>' + data + '</pre>';
                })
                .catch(error => {
                    console.error('Error fetching the content:', error);
                    document.getElementById('about-content').innerText = 'Failed to load content.';
                });
        </script>
    `;
}
