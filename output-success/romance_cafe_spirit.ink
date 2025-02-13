// Variables
VAR player_name = "Cafe Owner"
VAR has_secret_recipe = false
VAR friendliness_with_spirit = 0

// Start of the game
# changeBackground: cafe.png
You are the owner of a quaint little cafe on the edge of town. The building has a rich history, and lately, you have felt an unexplainable presence accompanying you.

As you brew your first coffee of the day, you hear a soft whisper, almost like a breeze.

+ "Who's there?" -> ask_presence
+ "I'm just hearing things..." -> dismiss_whisper

=== ask_presence ===
Your voice echoes in the silence, and a shimmering figure slowly comes into view. It's a spirit, adorned in gentle light.

"I am a fragment of this place, a spirit who has lingered too long," the presence murmurs.

+ "Can you tell me why you're here?" -> inquire_spirit_intent
+ "Is there something you need from me?" -> offer_help

=== dismiss_whisper ===
You brush it off, focusing on your work. Yet, the sensation lingers, warm and watchful.
-> cafe_customers

=== inquire_spirit_intent ===
The spirit smiles softly. "I was bound here long ago, seeking something lost. Companionship... understanding."

~ friendliness_with_spirit += 1

# changeBackground: cafe.png
-> cafe_customers

=== offer_help ===
The spirit's form flickers with an ethereal glow. "Kindness in the form of mortal flesh. Perhaps there's a way for both of us to find peace."

~ friendliness_with_spirit += 2

# changeBackground: cafe.png
-> cafe_customers

=== cafe_customers ===
The morning rush begins. Customers start filling in, and you're back to serving warm cups of comfort.
Suddenly, the familiar spirit appears by your side again, visible only to you.

+ "Help me serve," you whisper to the spirit. -> spirit_helps
+ "Stay out of sight," you say cautiously. -> spirit_observes

=== spirit_helps ===
The spirit assists you in small, wondrous ways—cups seem to float and fill effortlessly as you work.
# changeBackground: cafe.png
-> meet_regular

=== spirit_observes ===
You sense the spirit lingering in the background, observing silently, waiting for a more opportune time.
# changeBackground: cafe.png
-> meet_regular

=== meet_regular ===
Among the patrons, a regular, Mr. Thompson, approaches the counter. He's a man of few words but always orders the same: black coffee with a hint of mystery.

+ "Can I interest you in trying something different today?" -> new_suggestion
+ "The usual it is," you say warmly. -> prepare_usual

=== new_suggestion ===
"Why not try our new blend? It's called Enchanted Brew," you offer with a smile.

Mr. Thompson ponders. "I'll trust your judgment today, miss."

# changeBackground: cafe.png
-> serve_special_drink

=== prepare_usual ===
You prepare his usual order with care, grateful for such steady customers.

# changeBackground: cafe.png
-> cafe_closing

=== serve_special_drink ===
You brew the special blend, sensing the spirit's amused approval as you serve Mr. Thompson.

# changeBackground: cafe.png
-> cafe_closing

=== cafe_closing ===
As you turn the open sign to closed, you feel the spirit's presence more keenly. Its longing gaze is undeniable. 

"It's lonely when the lights go out, isn't it?" the spirit whispers. 

+ "Yes, it is," you confide. -> spirit_connection
+ "I cherish the quiet moments," you reply thoughtfully. -> savor_calm

=== spirit_connection ===
The spirit draws closer, an inexplicable warmth radiating from its form. "Perhaps we can fill the void together," it suggests.

~ friendliness_with_spirit += 2

# changeBackground: cafe_night.png
-> reflect_day

=== savor_calm ===
The spirit understands and drifts closer quietly, respecting your solace. Yet, you feel its presence weaving comfort around you.

# changeBackground: cafe_night.png
-> reflect_day

=== reflect_day ===
As the moon rises, you ponder the peculiar companionship you've found— a blend of human and ethereal.

{friendliness_with_spirit > 2:
    The spirit hovers near, its gaze gentle and full of promise. Together, you sense the beginnings of something transcendent.
- else:
    The spirit lingers, and though silent, there is a mutual curiosity bridging your worlds.
}

# changeBackground: cafe_night.png
-> END