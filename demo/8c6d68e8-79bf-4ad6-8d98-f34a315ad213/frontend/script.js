let clickCount = 0;

function addContent() {
    clickCount++;
    const contentDiv = document.getElementById('dynamic-content');
    contentDiv.innerHTML = `
        <h3>Dynamic Content</h3>
        <p>Button clicked ${clickCount} times!</p>
        <p>This content was generated dynamically using JavaScript.</p>
    `;
}

// Initialize page
document.addEventListener('DOMContentLoaded', function() {
    console.log('Simple Web App loaded successfully!');
});