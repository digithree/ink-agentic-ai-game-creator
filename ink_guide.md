# Ink Narrative Game Development Notes

## Preamble

We have chosen **Ink** as the narrative scripting engine for our interactive story projects.  
This decision is based on Ink's structured format, flexibility, and ability to integrate with a **custom InkJS render**.

Our **InkJS implementation** includes:
- **Background image display** for scene transitions.
- **Automatic save/load functionality** to preserve player progress.
- **A reset function** to restart the story when needed.

This document summarizes key **formatting strategies** and **best practices** for writing structured Ink scripts that work seamlessly with our InkJS-based game engine.

---

## Ink Narrative Formatting Strategy

### 1️⃣ Background Image Handling
- Use `# changeBackground: image.png` **before or after each choice resolution**.
- Always **set the background explicitly** to ensure it persists when saving/loading.
- **Game state should always be well-defined** at transition points.

### 2️⃣ Structuring Choices for Clarity
- **Ink appends choices to the next text block**, so structure responses carefully.
- Avoid **cutting off responses too suddenly** to maintain smooth dialogue flow.
- Example of a well-structured response:
  ```ink
  + "No..." -> honest_answer

  === honest_answer ===
  He nods. "Honesty. That is better."
  ```

### 3️⃣ Handling State & Inventory Items
- Always track variables **explicitly** (`VAR has_key = false`).
- If items affect the narrative, **check their state immediately after choices**.
- Example:
  ```ink
  === search_room ===
  You find a rusted key on the ground.
  ~ has_key = true
  ```

### 4️⃣ Save & Load Compatibility
- **InkJS only saves variables and visited nodes**, so we must **explicitly update backgrounds** in every section.

---

## 🚀 What to Do Next Time
1. **Follow these formatting strategies** when writing future stories.
2. **Be mindful of how Ink handles choices** so responses feel natural.
3. **Ensure backgrounds are explicitly set** after major transitions.
4. **Keep variable changes and conditions structured properly.**

---

This document ensures we follow a **consistent and effective approach** when developing **narrative games using Ink & InkJS**. 🚀

---

The following is an example Ink script:

``ink
// Variables
VAR player_name = "Traveler"
VAR has_key = false

// Start of the game
# changeBackground: room.png
You wake up in a dimly lit room. A figure stands before you, his features obscured by the flickering candlelight. His long robes sweep the dusty floor as he studies you in silence.

"You are awake at last," the old man says. "Do you know who I am?"

+ "Yes, you are... the Watcher?" -> lie_answer
+ "Yes, you are the Old Sage." -> lie_answer
+ "No..." -> honest_answer

=== lie_answer ===
"Yes, you are the Old Sage."

\n  // **Forces a new blank line before the next text**

He frowns. "The Watcher? The Old Sage? Lies, all of them." His voice is calm, but his eyes hold something unreadable. 

"You do not know me, yet you speak falsehoods so easily. Perhaps that is why you are here."

# changeBackground: room.png
-> ask_location

=== honest_answer ===
He nods approvingly. "Honesty. That is better. Few admit their own ignorance, yet that is the first step to wisdom."

# changeBackground: room.png
-> ask_location

=== ask_location ===
The old man folds his arms. "You are in a place between worlds. This is where lost souls gather."

He gestures around the dim chamber. "Listen, traveler, you must decide where to go next."

# changeBackground: room.png
+ "Leave immediately." -> go_forest
+ "Search the room first." -> search_room

=== search_room ===
"You are wise to look before you leap," the old man says.

As you scan the room, something glints beneath a pile of dust. You kneel and pull out a small, rusted key.

~ has_key = true
You turn it over in your hands. It is cold, heavier than you expected.

# changeBackground: room.png
-> go_forest

=== go_forest ===
# changeBackground: forest.png
You step into a dense, fog-covered forest. The air is thick with the scent of damp earth and something unfamiliar. Shadows shift between the towering trees, and an eerie silence blankets the world around you.

The old man follows behind, his gaze distant. "This path leads into the unknown. What lies ahead, only time will tell..."

{has_key:
    He glances at the key in your hand. "Keep that close. You may find yourself in need of it sooner than you think."
- else:
    He looks at you, then at your empty hands. "You feel the weight of uncertainty, do you not? Did you leave something behind?" 
}

# changeBackground: forest.png
-> END
```

## Troubleshooting and mistakes to avoid

### Proper variable setters

Note that to set a variable as the direct consequence of a choice, you have to do this on a new line, and jump to some label after, e.g.

```ink
VAR cafe_name = "Unnamed Cafe"

=== name_cafe ===
What would you like to name your cafe?
* [Rustic Beans]
    ~ cafe_name = "Rustic Beans"
    -> show_cafe_name
* [Modern Glow]
    ~ cafe_name = "Modern Glow"
    -> show_cafe_name

=== show_cafe_name
"Your cafe is now known as {cafe_name}."
-> choose_theme
```

### All choices must terminate with a _divert arrow_

Divert arrows `->` jumping to a knot (a labeled section) must be used to terminate all choices, whether using normal choices `*` or sticky choices `+`

INCORRECT:

```ink
+ [Search under the books] 
    Shuffling through the books, you uncover a worn journal filled with mysterious entries.
+ [Read the journal] -> read_journal

=== read_journal ===
// etc.
```

FIXED:

```ink
+ [Search under the books] 
    Shuffling through the books, you uncover a worn journal filled with mysterious entries.
    -> read_journal
+ [Read the journal] -> read_journal

=== read_journal ===
// etc.
```

### Knots (section labels) must use underscores and be in lower case

INCORRECT:

```ink
=== A NEW Section ===
```

FIXED:

```ink
=== a_new_section ===
```
