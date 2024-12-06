document.addEventListener("DOMContentLoaded", function () {
  const imageElement = document.getElementById("door-image");

  if (imageElement) {
    setInterval(() => {
      const timestamp = new Date().getTime();

      // New feature: Fetch the latest image URL from the server
      fetch("/latest_image_url")
        .then((response) => response.json())
        .then((data) => {
          if (data.image_url) {
            // If the server returns a new image URL, use it
            imageElement.src = `${data.image_url}?t=${timestamp}`;
          } else {
            // If no image URL is returned, fallback to the existing logic
            // which refreshes the current image by appending a timestamp
            imageElement.src = `${
              imageElement.src.split("?")[0]
            }?t=${timestamp}`;
          }
        })
        .catch((error) => {
          console.error("Error fetching latest image:", error);
          // On error, fallback to the existing logic
          imageElement.src = `${imageElement.src.split("?")[0]}?t=${timestamp}`;
        });
    }, 3000); // Refresh every 10 seconds
  }
});
