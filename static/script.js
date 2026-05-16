document.getElementById('apiBtn').addEventListener('click', async () => {
    try {
        const response = await fetch('/api/hello');
        const data = await response.json();
        document.getElementById('response').textContent = data.message;
    } catch (error) {
        document.getElementById('response').textContent = 'Error: ' + error.message;
    }
});
