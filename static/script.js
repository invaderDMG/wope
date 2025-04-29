document.getElementById('publishBtn').addEventListener('click', async () => {
    const text = document.getElementById('postText').value;
    const statusDiv = document.getElementById('status');
    statusDiv.innerHTML = "📡 Publicando...";

    const response = await fetch('/post', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text })
    });

    const result = await response.json();
    let html = "";

    for (const [platform, res] of Object.entries(result)) {
        if (res.status === "success") {
            html += `<p class="success">✅ ${platform}: ${res.message}</p>`;
        } else {
            html += `<p class="error">❌ ${platform}: ${res.message}</p>`;
        }
    }

    statusDiv.innerHTML = html;
});
