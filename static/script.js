document.getElementById('messageBtn').addEventListener('click', async () => {
    try {
        const response = await fetch('/api/message');
        const data = await response.json();
        const resultDiv = document.getElementById('result');
        resultDiv.textContent = data.message;
        resultDiv.style.display = 'block';
    } catch (error) {
        document.getElementById('result').textContent = 'Error: ' + error.message;
        document.getElementById('result').style.display = 'block';
    }
});
