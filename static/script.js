let recorder;
let chunks = [];
let stream;

const startBtn = document.getElementById("startBtn");
const stopBtn = document.getElementById("stopBtn");
const statusText = document.getElementById("status");

async function startRecording() {
    try {
        stream = await navigator.mediaDevices.getDisplayMedia({ video: true });

        recorder = new MediaRecorder(stream);

        recorder.ondataavailable = e => {
            if (e.data.size > 0) {
                chunks.push(e.data);
            }
        };

        recorder.onstop = () => {
            const blob = new Blob(chunks, { type: "video/webm" });
            uploadVideo(blob);
            chunks = [];
        };

        recorder.start();

        statusText.innerText = "Status: Recording...";
        startBtn.disabled = true;
        stopBtn.disabled = false;

    } catch (err) {
        alert("Permission denied or error occurred.");
    }
}

function stopRecording() {
    if (recorder) recorder.stop();

    if (stream) {
        stream.getTracks().forEach(track => track.stop());
    }

    statusText.innerText = "Status: Uploading...";
    startBtn.disabled = false;
    stopBtn.disabled = true;
}

function uploadVideo(blob) {
    const formData = new FormData();
    formData.append("video", blob, "recording.webm");

    fetch('/upload', {
        method: 'POST',
        body: formData
    })
    .then(() => {
        statusText.innerText = "Status: Saved!";
        location.reload();
    })
    .catch(() => {
        statusText.innerText = "Upload failed";
    });
}