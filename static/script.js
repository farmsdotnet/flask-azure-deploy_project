/* ── Tab switching ─────────────────────────────── */
document.querySelectorAll('.tab-btn').forEach(btn => {
    btn.addEventListener('click', () => {
        document.querySelectorAll('.tab-btn').forEach(b => {
            b.classList.remove('active');
            b.setAttribute('aria-selected', 'false');
        });
        document.querySelectorAll('.tab-panel').forEach(p => p.classList.remove('active'));

        btn.classList.add('active');
        btn.setAttribute('aria-selected', 'true');
        document.getElementById(btn.dataset.target).classList.add('active');

        clearStatus();
    });
});

/* ── Character counter ─────────────────────────── */
document.getElementById('textInput').addEventListener('input', function () {
    document.getElementById('charCount').textContent = this.value.length;
});

/* ── File-name display ─────────────────────────── */
document.getElementById('fileInput').addEventListener('change', function () {
    const label = document.querySelector('.file-label');
    if (this.files[0]) {
        document.getElementById('fileName').textContent = this.files[0].name;
        label.classList.add('has-file');
    } else {
        document.getElementById('fileName').textContent = 'Choose a .txt file';
        label.classList.remove('has-file');
    }
});

/* ── Conversion ────────────────────────────────── */
document.getElementById('convertBtn').addEventListener('click', async () => {
    const activePanel = document.querySelector('.tab-panel.active').id;
    const formData   = new FormData();

    if (activePanel === 'textPanel') {
        const text = document.getElementById('textInput').value.trim();
        if (!text) { showStatus('Please enter some text.', 'error'); return; }
        formData.append('text', text);
    } else {
        const file = document.getElementById('fileInput').files[0];
        if (!file) { showStatus('Please select a .txt file.', 'error'); return; }
        formData.append('file', file);
    }

    setConverting(true);
    clearStatus();

    try {
        const response = await fetch('/synthesize', { method: 'POST', body: formData });

        if (!response.ok) {
            const err = await response.json();
            showStatus(err.error || 'Conversion failed.', 'error');
            return;
        }

        // Build a temporary object URL from the audio blob and attach it to the player
        const blob = await response.blob();
        const url  = URL.createObjectURL(blob);

        const player      = document.getElementById('audioPlayer');
        const downloadBtn = document.getElementById('downloadLink');

        // Revoke any previous object URL to free memory
        if (player.src && player.src.startsWith('blob:')) {
            URL.revokeObjectURL(player.src);
        }

        player.src      = url;
        downloadBtn.href = url;

        document.getElementById('audioSection').hidden = false;
        player.play();
        showStatus('Audio ready!', 'success');

    } catch {
        showStatus('Network error — please try again.', 'error');
    } finally {
        setConverting(false);
    }
});

/* ── Helpers ───────────────────────────────────── */
function setConverting(loading) {
    const btn = document.getElementById('convertBtn');
    btn.disabled    = loading;
    btn.textContent = loading ? 'Converting…' : 'Convert to Speech';
}

function showStatus(msg, type) {
    const el = document.getElementById('statusMsg');
    el.textContent = msg;
    el.className   = 'status ' + type;
}

function clearStatus() {
    showStatus('', '');
}
