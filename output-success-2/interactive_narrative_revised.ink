// Variables
VAR player_name = "Traveler"
VAR has_key = false
VAR cafe_name = "Unnamed Cafe"

// Start of the game
# changeBackground: room.png
You wake up in a dimly lit room. A figure stands before you, his features obscured by the flickering candlelight. His long robes sweep the dusty floor as he studies you in silence.

"You are awake at last," the old man says, his voice reverberating in the stillness. "Do you know who I am?"

+ "Yes, you are... the Watcher?" -> lie_answer_watcher
+ "Yes, you are the Old Sage." -> lie_answer_sage
+ "No, I'm afraid I don't..." -> honest_answer

=== lie_answer_watcher ===
"You are... the Watcher, aren't you?"

\n

A frown etches his face. "Too eager to please, I see. Lies, even small ones, twist the very fabric of truth."

# changeBackground: room.png
-> ask_reason

=== lie_answer_sage ===
"I have heard tales. You must be the Old Sage."

\n

He chuckles softly, the sound echoing strangely. "More myth than man, that one. You seek knowledge wrapped in falsehood."

# changeBackground: room.png
-> ask_reason

=== honest_answer ===
He nods approvingly. "Honesty is wisdom's first step."

# changeBackground: room.png
-> ask_reason

=== ask_reason ===
The old man folds his arms, his eyes piercing yet kind. "You are in a place between worlds, where lost souls gather."

He gestures around the dim chamber. "Listen, traveler, you must decide your path."

+ "What path should I choose?" -> choose_path
+ "I want to leave this place." -> deciding_to_leave
+ "Why am I here?" -> question_purpose

=== choose_path ===
"The paths are many, as are the hurdles," he intones wisely.

\n

+ "Tell me more about these paths." -> paths_detailed
+ "I just want to find a way home." -> choosing_home
+ "I am ready to face whatever comes." -> ready_to_face

=== deciding_to_leave ===
"Desire to leave speaks more than fear, speaks of yearning," he suggests.

\n

+ "I must return to my time." -> time_return
+ "Is this realm so inhospitable?" -> inhospitable_realm
+ "Teach me what I must know before I go." -> teaching_before

=== question_purpose ===
"Purpose? A seeker of truth, maybe, a bearer of change, certainly."

\n

+ "I seek knowledge above all." -> knowledge_path
+ "I wish to forge my destiny." -> forge_destiny
+ "I am drawn to mysteries." -> drawn_to_mysteries

=== paths_detailed ===
"The roads unravel, each revealing truths concealed," he explains, his voice full of tacit mysteries.

You ponder as the room seems to shift, shadows bending and the air thick with tension.

-> decide_action

=== choosing_home ===
His eyes soften, a trace of melancholy hidden in his gaze. "Ah, but what defines home? A place or a state of mind?"

\n

He gestures around. "The journey leads to places unexpected, and therein lies home."

-> decide_action

=== ready_to_face ===
"Fearlessness is a virtue, yet calm determination triumphs best," he advises, his tone level.

\n

# changeBackground: room.png
"Be prepared. Ahead are choices, each with weight unseen."

-> decide_action

=== time_return ===
# changeBackground: room.png
The air shimmers as your determination falters, and yet the image of home burns brightly within.

"The threads of time are vexingly stubborn."

-> decide_action

=== inhospitable_realm ===
"This realm reflects not hostility but self-exploration," he replies, gently challenging your assumptions.

\n

# changeBackground: room.png
"You may learn much here, and from yourself."

-> decide_action

=== teaching_before ===
He nods, folds his robed arms, and prepares to impart wisdom. "Listen well then, for truths will come disguised."

\n
Your mind readies itself to absorb wisdom, the surroundings echoing silent encouragement.

-> decide_action

=== knowledge_path ===
Your quest to learn fuels a fire within, the old man's approval almost palpable. "Then know you must bear resilience to grasp such knowledge."

\n
"Understand the riddles of the heart and soul, and doors shall open."

-> choose_next

=== forge_destiny ===
"Like a smith hunched over anvil, so must you shape your own will to create the unforeseen."

\n
# changeBackground: room.png
"Destiny is but choices lain bare. Forge onward, but with wisdom in choice."

-> choose_next

=== drawn_to_mysteries ===
"A pursuit of shadow and light," the old man muses. "Few seek mysteries openly, yet they lead to fascination eternal."

\n
# changeBackground: room.png
"The shadowy paths conceal what others overlook."

-> choose_next

=== decide_action ===
As his speech winds down, a rustling sound draws your attention to a small table bearing a key. 

+ "Inspect the key." -> inspect_key
+ "Look away." -> glance_away

=== choose_next ===
He motions towards the room's door, once hidden, now manifest.

+ "Open the door." -> go_forest
+ "Search the room further." -> search_room

=== inspect_key ===
You kneel and take the key, its cold weight familiar. The old man's eyes twinkle knowingly as he watches your decision.

~ has_key = true
"You have chosen a path," he speaks, an undercurrent of approval in his words.

-> prepare_deeper_journey

=== glance_away ===
Feeling unease, you turn away, and the old man's knowing gaze lingers over your hesitation.

"Haste often conceals truth," he warns, the stress in his tone undeniable.

-> choose_next

=== search_room ===
"You are wise to look before you leap," the old man says.

\n
# changeBackground: room.png
As you scan the room, the dust-covered surfaces reveal hidden stories within their gleam. Beneath is a small, rusted key.

~ has_key = true
The weight of possibilities hangs in the air as you hold it.

-> go_forest

=== prepare_deeper_journey ===
# changeBackground: forest_entry.png
The old wood door creaks open as you step into the fog-laden realm, the transition between room and forest seamless yet starkly clear.

"The mist conceals yet guards what lies beyond." 

{has_key:
  He eyes the key. "It may guide you, should you deem it worthy."
- else:
  "Empty your hands may be, yet choices unmade rest within."
}

-> go_forest

=== go_forest ===
# changeBackground: forest.png
You're enveloped by a dense forest, the air alive with the scent of earth and mystery. Shadows reach across the path, gestures of welcome and caution alike.

The old man stands, a presence neither near nor far, forever watchful as you traverse the unknown, now with possibilities spiraling in infinite directions.

{has_key:
    His gaze falls to your key, "Hold it near. It might show you paths unseen."
- else:
    An echo of uncertainty lingers, a feeling as though answers remain just out of reach. "Remember, exploration feeds the soul as much as it teaches the mind." 
}

# changeBackground: forest.png
-> END