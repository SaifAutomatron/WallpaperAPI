document.addEventListener('DOMContentLoaded', function() {
    document.getElementById("walluploadform").addEventListener("submit", async function (e) {
        e.preventDefault();
        const form = e.currentTarget;
        const formData = new FormData(form);

        const jsonData = {
            title: form.querySelector('[name="title"]').value,
            description: form.querySelector('[name="description"]').value,
            category: form.querySelector('[name="category"]').value
        };

        formData.append("wallpaper_request", JSON.stringify(jsonData));

        try {
            const response = await fetch(form.action, {
                method: 'POST',
                body: formData
            });

            if (response.ok) {
                const result = await response.json();
                console.log("Success:", result);
                alert("Upload successful!");
            } else {
                console.error("Upload failed:", response.statusText);
                alert("Upload failed: " + response.statusText);
            }
        } catch (error) {
            console.error("Error:", error);
            alert("An error occurred while uploading.");
        }
    });
});
