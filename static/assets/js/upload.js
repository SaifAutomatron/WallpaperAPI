document.getElementById("walluploadform").addEventListener("submit", async function (e) {
    e.preventDefault();

    const form = e.currentTarget;
    const formData = new FormData(form);

    // Construct the JSON data.
    const jsonData = {
        title: form.querySelector('[name="title"]').value,
        description: form.querySelector('[name="description"]').value,
        category: form.querySelector('[name="category"]').value
    };

    // Add the JSON data under a single key.
    formData.append("wallpaper_request", JSON.stringify(jsonData));

    try {
        const response = await fetch(form.action, {
            method: 'POST',
            body: formData
        });

        if (response.ok) {
            const result = await response.json();
            console.log("Success:", result);

            // Display success message to the user
            const successDiv = document.getElementById("upload-success-message");
            successDiv.textContent = result.message; // Assuming your response object has a message key
            successDiv.style.display = "block"; // Make the success message visible

        } else {
            console.error("Upload failed:", response.statusText);
            // You might want to show this error to the user as well
        }
    } catch (error) {
        console.error("Error:", error);
        // You might want to show this error to the user
    }
});
