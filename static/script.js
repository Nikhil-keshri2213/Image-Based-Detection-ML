document.getElementById('imageInput').addEventListener('change', function(event) {
    let file = event.target.files[0];
    if (file) {
        let reader = new FileReader();
        reader.onload = function(e) {
            let preview = document.getElementById('image-preview');
            preview.src = e.target.result;
            preview.style.display = 'block';
        };
        reader.readAsDataURL(file);
    }
});

function uploadImage() {
    let input = document.getElementById('imageInput');
    if (!input.files[0]) {
        alert("Please select an image.");
        return;
    }

    let formData = new FormData();
    formData.append("file", input.files[0]);

    fetch("/predict", {
        method: "POST",
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById("result").innerText = 
            `Class: ${data.class}, Confidence: ${(data.confidence * 100).toFixed(2)}%`;
    })
    .catch(error => console.error("Error:", error));
}
