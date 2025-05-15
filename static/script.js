const video = document.getElementById('video');
const canvas = document.getElementById('canvas');
const ctx = canvas.getContext('2d');
let predictionEl = document.getElementById('prediction');

// Request camera permission and start video
navigator.mediaDevices.getUserMedia({ video: true })
    .then(stream => { video.srcObject = stream; })
    .catch(err => { console.error('Error accessing camera:', err); });

// Send frames periodically for prediction
setInterval(() => {
    ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
    const dataURL = canvas.toDataURL('image/jpeg');
    fetch('/predict', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ image: dataURL })
    })
        .then(res => res.json())
        .then(data => { predictionEl.textContent = data.label; })
        .catch(console.error);
}, 1000);

function speak() {
    const text = predictionEl.textContent;
    const textLang = document.getElementById('textLang').value;
    const audioLang = document.getElementById('audioLang').value;
    fetch('/speak', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text, text_lang: textLang, audio_lang: audioLang })
    })
        .then(res => res.json())
        .then(data => {
            const audio = new Audio(data.audio_url);
            audio.play();
        });
}

function logout() {
    window.location.href = '/logout';
}