// Load Ink story JSON from an external file
fetch("story.json")
    .then(response => response.json())
    .then(data => {
        let story = new inkjs.Story(data);

        //showStory(story);
        // Check if a saved game exists
        if (localStorage.getItem("inkSave")) {
            loadGame(story, true); // Load progress if available
        } else {
            showStory(story); // Otherwise, start fresh
        }

        // Attach buttons
        document.getElementById("resetBtn").onclick = function () {
            resetGame(new inkjs.Story(data));
        };
    })
    .catch(error => console.error("Error loading Ink story:", error));

function showStory(story) {
    let storyContainer = document.getElementById("story");
    let choicesContainer = document.getElementById("choices");

    // Extract all new story content before clearing the screen
    let newText = "";
    let tags = [];
    while (story.canContinue) {
        newText += `<p>${story.Continue()}</p>`;
        tags.push(...story.currentTags);
    }

    // Apply background changes before fading out
    tags.forEach(tag => {
        if (tag.startsWith("changeBackground: ")) {
            let bgImage = tag.replace("changeBackground: ", "");
            changeBackground(bgImage);
        }
    });

    // Fade out, replace text, fade in
    fadeOut(storyContainer, () => {
        storyContainer.innerHTML = newText;
        fadeIn(storyContainer);

        // Display new choices
        choicesContainer.innerHTML = "";
        for (let i = 0; i < story.currentChoices.length; i++) {
            let choice = story.currentChoices[i];
            let button = document.createElement("button");
            button.innerHTML = choice.text;
            button.onclick = function () {
                story.ChooseChoiceIndex(i);
                saveGame(story);
                showStory(story);
            };
            choicesContainer.appendChild(button);
        }
    });
}

// ✅ Save function: Stores game state in localStorage
function saveGame(story) {
    let saveData = story.state.toJson();
    localStorage.setItem("inkSave", saveData);
}

// ✅ Load function: Restores game state from localStorage
function loadGame(story) {
    let saveData = localStorage.getItem("inkSave");
    if (saveData) {
        story.state.LoadJson(saveData);
        showStory(story, true);
    } else {
        alert("No save found!");
    }
}

function resetGame(story) {
    // Ask the user for confirmation before resetting
    let confirmReset = confirm("Are you sure you want to start a new game? This will erase your progress.");

    if (confirmReset) {
        // Overwrite save game and restart
        saveGame(story);
        // Restart the story from the beginning
        showStory(story, true); // Reload story from start
    }
}


// Function to change background without affecting scrolling
function changeBackground(image) {
    console.log("changeBackground: " + image)
    document.body.style.backgroundImage = `url(${image})`;
    document.body.style.backgroundSize = "cover";
    document.body.style.backgroundPosition = "center center";
    document.body.style.backgroundAttachment = "fixed"; // Prevents movement
    document.body.style.transition = "background 1s ease-in-out"; // Smooth transition
}


// Fade Out Effect (clears text after fade)
function fadeOut(element, callback) {
    let opacity = 1;
    let fadeEffect = setInterval(function () {
        if (opacity <= 0.1) {
            clearInterval(fadeEffect);
            element.style.opacity = 0;
            if (callback) callback(); // Execute callback after fade-out
        } else {
            opacity -= 0.1;
            element.style.opacity = opacity;
        }
    }, 50);
}

// Fade In Effect (shows text smoothly)
function fadeIn(element) {
    let opacity = 0;
    element.style.opacity = opacity;
    let fadeEffect = setInterval(function () {
        if (opacity >= 1) {
            clearInterval(fadeEffect);
        } else {
            opacity += 0.1;
            element.style.opacity = opacity;
        }
    }, 50);
}
