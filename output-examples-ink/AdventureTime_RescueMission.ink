// Variables
VAR has_sword = false
VAR has_map = false
VAR defeated_monster = false
VAR free_jake = false

// Start of Adventure
# changeBackground: grassy_knoll.png
You are Finn the Human, and today you find yourself standing at the edge of a dense, mysterious forest. Standing beside you is Princess Bubblegum, who seems worried.

"Finn, Jake's been kidnapped by the dark creatures of the Dungeons of Despair! You have to rescue him."

+ "I won't let Jake down!" -> head_to_forest
+ "Can you help me?" -> ask_for_help

=== ask_for_help ===
Princess Bubblegum hands you a map. "Here, this will show you the most treacherous paths."

~ has_map = true
# changeBackground: grassy_knoll.png
-> head_to_forest

=== head_to_forest ===
# changeBackground: forest_entrance.png
The forest looms ahead, shadows dancing beneath the thick canopy. With each step, the air grows thicker, and the sounds of distant creatures reach your ears.

+ "Head deeper into the forest." -> deeper_forest
+ "Look around for useful items." -> search_forest

=== search_forest ===
# changeBackground: forest_clearing.png
You scour the area, pushing aside thick vines and peering beneath moss-covered rocks. Suddenly, you spot something glinting in the shadows.

You reach down to discover a surprisingly sturdy sword stuck in the underbrush.

~ has_sword = true
# changeBackground: forest_entrance.png
-> deeper_forest

=== deeper_forest ===
# changeBackground: forest_path.png
As you navigate the winding path, a rustling in the bushes stops you in your tracks. A grotesque creature emerges, eyes gleaming maliciously.

+ "Fight the creature!" -> fight_creature
+ "Try to sneak around it." -> sneak_past

=== sneak_past ===
# changeBackground: forest_path.png
You take cautious steps, your heart pounding in your chest. The creature's gaze flickers over the shadows, but it doesn't seem to notice you.

-> continue_path

=== fight_creature ===
# changeBackground: creature_battle.png
The creature lunges at you with a snarl. It's now or never!

{has_sword:
    You wield your sword deftly, defending yourself with skill. After a fierce battle, the creature is defeated, and you feel a sense of accomplishment.
    ~ defeated_monster = true
- else:
    You brace yourself with makeshift weapons, but the creature is relentless. It manages to injure you before you escape. You'll need to be more careful.
}

# changeBackground: forest_path.png
-> continue_path

=== continue_path ===
# changeBackground: dungeon_entrance.png
You emerge from the forest to find the foreboding entrance to the Dungeons of Despair. The air is damp and heavy, and the echo of distant screams hints at danger within.

+ "Enter the dungeon." -> enter_dungeon
+ "Prepare before going in." -> prepare_outside

=== prepare_outside ===
# changeBackground: dungeon_entrance.png
You take a moment to catch your breath, reviewing the map once more, ensuring you know the twists and turns that await.

-> enter_dungeon

=== enter_dungeon ===
# changeBackground: dungeon_hallway.png
The narrow hallways of the dungeon are dimly lit, with flickers of torchlight casting eerie shadows. You hear the sound of chains rattling in the distance.

+ "Investigate the sound." -> investigate_sound
+ "Move cautiously further into the dungeon." -> cautious_exploration

=== investigate_sound ===
# changeBackground: dungeon_chamber.png
In a small chamber, you find Jake the Dog shackled against a stone wall. He looks weary but manages a small smile when he sees you.

"Finn! You have to find the key to these chains!"

+ "Search the room for a key." -> search_chamber
+ "Reassure Jake." -> reassure_jake

=== reassure_jake ===
"Hang tight, buddy. I'll get you out of here."

Jake nods, his trust in you unwavering.

-> search_chamber

=== search_chamber ===
# changeBackground: dungeon_search.png
You scour the chamber, your hands brushing against the cold stone. Hidden under a pile of rusted armor, you find a key that seems to shimmer in the dim light.

~ free_jake = true
-> free_jake_dog

=== free_jake_dog ===
# changeBackground: dungeon_chamber.png
You unlock the chains with a satisfying click, and Jake falls into your arms, free at last.

"Thanks, Finn! Let's get out of this creepy place."

-> escape_dungeon

=== cautious_exploration ===
# changeBackground: dungeon_deeper.png
You tread carefully, each step echoing against the stone walls. The atmosphere grows tense, and you can sense a powerful presence ahead.

+ "Confront the presence." -> final_encounter
+ "Backtrack and find another way." -> backtrack

=== final_encounter ===
# changeBackground: dungeon_thrill.png
A shadowy figure looms large, its eyes burning with an unearthly glow. It blocks your path with a menacing stance.

+ "Use your sword to fight!" -> defeat_shadow
+ "Try to reason with the figure." -> reason_with_shadow

=== defeat_shadow ===
# changeBackground: shadow_fight.png
With a determined cry, you raise your sword, ready to defend both Jake and yourself. The battle is intense yet swift.

Whether it was your skill or luck, you stand victorious as the dark figure dissolves into mist.

-> escape_dungeon

=== reason_with_shadow ===
# changeBackground: shadow_conversation.png
Holding a hand out placatingly, you speak from the heart, trying to appeal to any humanity left within the shadowy creature.

After a moment, the creature lowers its guard and nods. There's a moment of peace as it fades away.

-> escape_dungeon

=== backtrack ===
# changeBackground: dungeon_backtrack.png
Realizing this path is too perilous, you quickly retrace your steps, seeking another way to find Jake.

-> investigate_sound

=== escape_dungeon ===
# changeBackground: dungeon_exit.png
With Jake at your side, you make your way towards the dungeon exit, the oppressive air lifting with each step.

Once outside, Princess Bubblegum greets you with relief. "You did it, Finn! Jake is safe, and the dark presence is gone."

The adventure comes to a close, but both you and Jake know that more tales await in the Lands of Ooo.

# changeBackground: grassy_knoll.png
-> END