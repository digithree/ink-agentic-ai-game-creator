// Variables
VAR player_name = "Adventurer"
VAR has_map = false

// Introduction
# changeBackground: castle.png
You find yourself standing at the gates of an ancient castle, its towering spires lost in the clouds above.

A mysterious figure, cloaked in shadows, approaches and speaks.

"Welcome, Adventurer. Do you seek the treasure hidden within these walls?"

+ "Yes, tell me more about the treasure." -> ask_about_treasure
+ "No, I'm just passing by." -> just_passing_by

=== ask_about_treasure ===
The figure nods approvingly. "The treasure is said to hold unfathomable power. However, it is guarded by ancient puzzles."

He hands you a map.
~ has_map = true

"This will guide you through the first corridor."

# changeBackground: corridor.png
-> explore_corridor

=== just_passing_by ===
The figure studies you for a moment, a hint of disappointment in their eyes.

"Very well, but remember, opportunities seldom come by."

# changeBackground: forest_path.png
You decide to take a detour, turning away from the castle.

-> END

=== explore_corridor ===
You enter the dimly lit corridor, following the path outlined on your map.

{has_map:
    The map reveals a hidden path behind a tapestry. You pull it aside, revealing a secret passage.
- else:
    With no guidance, you wander aimlessly, the dark shadows seeming to swallow your movements.
}

# changeBackground: secret_room.png
The secret passage leads you to an underground chamber.

+ "Search the room." -> search_room
+ "Return to the corridor." -> return_corridor

=== search_room ===
You find an ornate chest in the corner, its surface covered in dust and timeworn engravings.

=== open_chest ===
# changeBackground: treasure_room.png
The chest creaks open, revealing a trove of glittering jewels and a small key.

The small key feels cool in your hand.

# changeBackground: castle.png
-> END

=== return_corridor ===
You retrace your steps back to the corridor.

# changeBackground: castle.png
Returning to the corridor, you cannot shake the sense of unfinished business.

-> END