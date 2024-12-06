document.addEventListener("DOMContentLoaded", function () {
  const imageElement = document.getElementById("door-image");

  if (imageElement) {
    setInterval(() => {
      const timestamp = new Date().getTime();
      imageElement.src = `${imageElement.src.split("?")[0]}?t=${timestamp}`;
    }, 10000); // Refresh every 10 seconds
  }
});
