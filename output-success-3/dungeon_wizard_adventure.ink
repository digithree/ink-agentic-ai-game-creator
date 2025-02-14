// Variables
VAR player_name = "Adventurer"
VAR has_mana_stone = false
VAR learned_fire_spell = false

// Start of the game
# changeBackground: dungeon_entrance.png
You stand before the ancient entrance to the dungeon, a place whispered about with both fear and reverence. It is said that deep within resides a hermit wizard, a master of magic.

"Enter, if you dare," a voice echoes from within, challenging your resolve.

+ "I am ready." -> enter_dungeon
+ "Perhaps I should prepare more..." -> hesitate

=== enter_dungeon ===
# changeBackground: dark_halls.png
You step into the shadows, the cool air biting at your skin. As you proceed, odd symbols glow faintly along the walls, guiding your path.

+ "Examine the symbols." -> examine_symbols
+ "Continue forward." -> continue_forward

=== hesitate ===
You hesitate at the entrance, your heart pounding with uncertainty.

"Bravery is not the absence of fear, but the decision to press onward despite it," whispers an unseen presence.

-> enter_dungeon

=== examine_symbols ===
The symbols seem to pulse as your fingers trace over them. An ancient language, perhaps?

"These are words of power," you murmur to yourself, an inkling of understanding taking root.

# changeBackground: dark_halls.png
-> continue_forward

=== continue_forward ===
# changeBackground: chamber_door.png
Deeper still, you find yourself before a massive wrought iron door. Carved into its surface are scenes of mages wielding great power.

"What secrets lie beyond?" your breath fogs the air as you ponder.

+ "Open the door." -> open_door
+ "Look for another way." -> search_alternate

=== open_door ===
# changeBackground: magic_chamber.png
The door creaks open, revealing a chamber bathed in ethereal light. At its center, an old wizard stands, eyes closed in deep concentration, his staff glowing softly.

"You've come seeking knowledge," his voice resonates without moving his lips.

+ "Yes, teach me the ways of magic." -> learn_magic
+ "I seek a mana stone." -> seek_mana_stone

=== search_alternate ===
Behind a tapestry, you find a hidden passage leading further into the dungeon. Cryptic murals line the walls, telling tales of mages of old.

# changeBackground: secret_passage.png
-> explore_secret

=== learn_magic ===
With a nod, the wizard motions for you to sit.

"To control flame is to understand its nature. It hungers, yet brings warmth."

He traces a pattern in the air, and a small flame dances above his palm.

+ "Concentrate and mimic his gesture." -> learn_fire_spell
+ "Ask about other spells." -> inquire_spells

=== seek_mana_stone ===
The wizard opens his eyes, considering your request.

"Such stones are rare. You may find one in the depths of this very dungeon."

~ has_mana_stone = true

# changeBackground: hidden_altar.png
The wizard points you toward a hidden altar, where a mana stone gleams faintly.

+ "Take the mana stone." -> take_stone
+ "Leave the altar untouched." -> leave_altar

=== explore_secret ===
# changeBackground: hidden_cavern.png
You follow the passage into a vast cavern, the ceiling twinkling like the night sky.

"Here, beneath the earth, magic flows freely," the wizard's voice echoes.

+ "Draw upon the ambient magic." -> channel_magic
+ "Search the area." -> cavern_search

=== learn_fire_spell ===
~ learned_fire_spell = true

You focus intently, and a small spark ignites above your hand.

"Well done," the wizard smiles, "Remember, with great power comes great responsibility."

# changeBackground: magic_chamber.png
-> conclude

=== inquire_spells ===
The wizard chuckles softly.

"There is time to learn other arts, but first, you must master this one."

-> learn_fire_spell

=== take_stone ===
Taking the mana stone, you feel a surge of energy coursing through you.

"Use this wisely," the wizard advises.

# changeBackground: hidden_altar.png
-> conclude

=== leave_altar ===
You leave the stone upon the altar, a sense of peace settling within you.

# changeBackground: hidden_altar.png
-> conclude

=== channel_magic ===
You close your eyes and draw upon the magic that thrums beneath you, feeling its ancient wisdom fill your senses.

# changeBackground: hidden_cavern.png
-> conclude

=== cavern_search ===
As you search the cavern, you stumble upon an old staff, its surface etched with runes.

"A gift to aid you," the wizard's voice is a mere whisper now.

~ has_mana_stone = true

# changeBackground: hidden_cavern.png
-> conclude

=== conclude ===
As your journey within the dungeon draws to a close, you reflect upon the knowledge and relics gained.

The wizard's parting words linger in your mind, "Magic is not a tool, but a path. Walk it wisely."

# changeBackground: dungeon_entrance.png
Your adventure continues beyond the dungeon's shadowed halls, for magic is a journey with no end.

-> END