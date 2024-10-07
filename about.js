// about.js

// Function to load the "About" page content directly with basic formatting
export function loadAboutPage() {
    // The text content directly embedded as plain text
    const aboutText = `
About This Tool

This tool helps you discover quotes from texts that have a specific numerical value according to English Qaballa. Here's how to use it:

1. Choose Your Input:
You can either enter a URL of a .txt file in the input box provided, or upload a local text file (TXT or PDF) by clicking on "Upload a file" and selecting the desired file.

2. Enter the Target Sum:
Type the numerical value you're looking for in the "Enter target sum" box. This sum is based on the English Qaballa values assigned to each letter in the quote.

3. Invoke the Search:
Click the "Invoke" button to start the search process.

4. View the Results:
The tool will display all quotes that match your target sum, along with their calculated values and source (URL or filename).

Tips:
- For best results when using URLs, ensure the links point to plain text content.
- Larger text files or documents may take longer to process, so please be patient.
- Experiment with different sums to uncover interesting patterns in the text.

What is English Qaballa?
English Qaballa is a system that assigns numerical values to numbers and letters. In this system:
0 = 0 , 1 = 1, .... 9 = 9
A = 10, B = 11, C = 12, and so on up to Z = 35. 
The sum of a word or phrase is the total of these values.
`;

    return `
        <style>
            .about-container {
                max-width: 800px;
                margin: 0 auto;
                padding: 30px;
                margin-top: 140px;
                font-family: 'Fira Code', monospace;
                line-height: 1.6;
                text-align: left; /* Align text to the left for plain text appearance */
                white-space: pre-wrap; /* Preserve whitespace, line breaks, and tabs */
                color: var(--text-color, #e0e0e0);
                background-color: var(--background-color, #1c1c1c);
                border: 1px solid #444;
                border-radius: 8px;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                overflow: visible; /* Remove overflow restrictions */
                font-size: 13px; /* Slightly smaller font size for a plain text appearance */
            }
        </style>

        <div class="about-container">
            ${convertToPlainText(aboutText)} <!-- Display the plain text content -->
        </div>
    `;
}

// Function to convert the plain text to a readable HTML format while preserving line breaks and spaces
function convertToPlainText(text) {
    // Escape HTML special characters to prevent HTML injection
    const escapedText = text.replace(/[&<>"']/g, function (char) {
        const escapeMap = {
            '&': '&amp;',
            '<': '&lt;',
            '>': '&gt;',
            '"': '&quot;',
            "'": '&#39;',
        };
        return escapeMap[char];
    });

    // Replace newlines with <br> to keep line breaks
    return escapedText.replace(/\n/g, '<br>');
}
