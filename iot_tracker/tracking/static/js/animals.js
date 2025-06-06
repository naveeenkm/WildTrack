document.addEventListener("DOMContentLoaded", () => {
  // Safely retrieve the animal-data element
  const animalDataElement = document.getElementById("animal-data");

  if (!animalDataElement) {
      console.error("Element with id 'animal-data' is missing from the DOM.");
      return;
  }

  // Parse JSON data
  let databaseAnimals;
  try {
      databaseAnimals = JSON.parse(animalDataElement.textContent);
  } catch (e) {
      console.error("Failed to parse animal data:", e);
      return;
  }

  console.log("Database Animals:", databaseAnimals); // Debug log

  const animalColors = {
      Tiger: "rgb(146 26 0)",
      Elephant: "#8E44AD",
      Deer: "#28B463",
      Lion: "#F4D03F",
      Bear: "#34495E"
  };

  const predefinedAnimals = [
      { msg: "Tiger", radius: 13, angle: 0, color: animalColors["Tiger"] },
      { msg: "Elephant", radius: 13, angle: 80, color: animalColors["Elephant"] },
      { msg: "Lion", radius: 13, angle: 180, color: animalColors["Lion"] }
  ];

  function calculatePosition(radius, angle) {
      const radians = (angle * Math.PI) / 180;
      const x = 50 + radius * Math.cos(radians);
      const y = 50 + radius * Math.sin(radians);
      return { x, y };
  }

  function renderAnimals() {
      const container = document.querySelector(".alerts-container");

      if (!container) {
          console.error("Element with class 'alerts-container' is missing.");
          return;
      }

      // Render database animals
      databaseAnimals.forEach(animal => {
          const position = calculatePosition(28, animal.angle);
          let animalDiv = document.querySelector(`.alerts-animal[data-name="${animal.name}"]`);

          if (!animalDiv) {
              animalDiv = document.createElement("div");
              animalDiv.className = "alerts-animal alerts-alerted-animal";
              animalDiv.setAttribute("data-name", animal.name);
              container.appendChild(animalDiv);
          }

          animalDiv.style.top = position.x + "%";
          animalDiv.style.left = position.y + "%";
          animalDiv.style.backgroundColor = animalColors[animal.name] || "gray";
          animalDiv.textContent = animal.name;
      });

      // Render predefined animals
      predefinedAnimals.forEach(animal => {
          if (!databaseAnimals.some(dbAnimal => dbAnimal.name === animal.msg)) {
              const position = calculatePosition(animal.radius, animal.angle);
              let animalDiv = document.querySelector(`.alerts-animal[data-name="${animal.msg}"]`);

              if (!animalDiv) {
                  animalDiv = document.createElement("div");
                  animalDiv.className = "alerts-animal";
                  animalDiv.setAttribute("data-name", animal.msg);
                  container.appendChild(animalDiv);
              }

              animalDiv.style.top = position.y + "%";
              animalDiv.style.left = position.x + "%";
              animalDiv.style.backgroundColor = animal.color;
              animalDiv.textContent = animal.msg;
          }
      });
  }

  function updateAngles() {
      databaseAnimals.forEach(animal => {
          animal.angle = (animal.angle + 1) % 360;
      });
      predefinedAnimals.forEach(animal => {
          animal.angle = (animal.angle - 1) % 360;
      });
  }

  function animateAnimals() {
      updateAngles();
      renderAnimals();
  }

  renderAnimals();
  setInterval(animateAnimals, 100);
});
