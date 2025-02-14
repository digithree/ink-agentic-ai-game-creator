// Variables
VAR player_name = "Owner"
VAR heartwarming_moments = 0
VAR cafe_open = true
VAR mystery_solved = false
VAR romantic_interest = 0
VAR memories_uncovered = 0
VAR decisions_taken = 0

// Start of story
# changeBackground: cafe_day.png
The aroma of freshly ground coffee fills your bustling café, an intricate dance of breakfast orders and clinking cups merging into the morning symphony. Yet, amid the vibrant activity, there's a peculiar chill in the air, as though a whisper of the past slips through the present.

A figure, ethereal and serene, materializes with an enigmatic smile. Her presence is both foreign and comfortingly familiar.

"Good morning, {player_name}," the spirit greets, her voice like the rustle of autumn leaves. "Do you recognize who I am?"

+ "Yes, you're the guardian spirit of the café." -> know_spirit
+ "No, should I have heard of you before?" -> no_spirit

=== know_spirit ===
"Ah, you have heard the whispers of my existence," she replies, a soft glow radiating from her presence. "This café is filled with cherished memories."

~ heartwarming_moments += 1

# changeBackground: cafe_day.png
-> ask_reason

=== no_spirit ===
The spirit chuckles, her laughter like the tinkling of bells. "Not all are aware of my presence, but perhaps as time passes, curiosity will lead you to clarity."

# changeBackground: cafe_day.png
-> ask_reason

=== ask_reason ===
A delicate wisp of moonlight even in day, she glides through the air, her gaze taking in the customers and the faded piano forlorn in the corner. "What do you think draws me to this place?"

+ "To aid me in my quest to revitalise the café, I hope?" -> help_cafe
+ "To unnerve me with your haunting visage?" -> haunt_cafe
+ "To unveil the stories the walls hold secret." -> learn_past

=== help_cafe ===
"Indeed, part of my essence is entwined with this place," the spirit nods. Her aura suffuses warmth and assurance.

~ romantic_interest += 1

# changeBackground: cafe_day.png
-> cafe_day_activities

=== haunt_cafe ===
Her musical laughter fills the air. "A spirit I am, yet a benevolent one. Fear not the mischief I might bring, for it masks the goodwill beneath."

# changeBackground: cafe_day.png
-> cafe_day_activities

=== learn_past ===
Her gaze becomes wistful, as if leafing through the pages of time. "A tapestry of tales is woven here. Perhaps, together, we might glimpse its vivid threads."

~ heartwarming_moments += 1
~ romantic_interest += 1

# changeBackground: cafe_day.png
-> cafe_day_activities

=== cafe_day_activities ===
The day unfolds, a vivid canvas of clangor and chatter, your duties ever-present yet your mind is drawn back to the spirit's presence. She seems an anchoring force amidst the chaos. What will you do?

+ "Seek her wisdom on dealing with a customer dilemma." -> customer_advice
+ "Request her to recount the café's vibrant history." -> hear_stories
+ "Encourage her to express herself through music." -> piano_duet
+ "Ask her about the mysteries of her own past." -> inquire_her_past

=== customer_advice ===
The spirit listens intently as you describe the troubles with a vexed patron.

~ cafe_open = false
"Let kindness guide your actions," she advices, her ethereal aura lending tranquility to the situation.

+ "You've been a tremendous support." -> gratitude
+ "Join me for a brew?" -> coffee_invite

=== hear_stories ===
Her voice is the brush, painting vivid scenes of the past—a romance kindled by this very hearth, warming lives through winters long past.

~ heartwarming_moments += 1

+ "What became of those lovers?" -> learn_lovers
+ "Did my grandmother feature in such tales?" -> grandmother_past

=== piano_duet ===
A melody unfolds under her adept fingers, notes echoing through the room like ripples on a pond. The air tingles with the music's ethereal beauty, eliciting awe from the crowd.

+ "Accompany her with a serenade of your own." -> duet_song
+ "Enjoy the resonance of the moment." -> savor_moment

=== inquire_her_past ===
The spirit sits, thoughtful. "My own story is as much a mystery. In centuries past, I watched over families, celebrated joys, mourned losses."

+ "And your own heart? Has it known love?" -> spirit_romance
+ "Do you miss the world of touch, of surface and sense?" -> spirit_regrets

=== spirit_romance ===
A gentle sigh escapes her. "Yes, the echoes of my own heart's affections once danced in the starlight unsheltered by walls."

~ romantic_interest += 1

# changeBackground: cafe_evening.png
-> cafe_closing

=== spirit_regrets ===
"The tangible leaves its imprint on the essence of the soul," she admits, a poignant nostalgia emanating from her form.

~ memories_uncovered += 1

# changeBackground: cafe_evening.png
-> cafe_closing

=== gratitude ===
# changeBackground: cafe_evening.png
A light bow conveys her appreciation. "In these expressions of gratitude lies the nurturing of the spirit."

-> cafe_closing

=== coffee_invite ===
# changeBackground: cafe_evening.png
The spirit contemplates the fragrant cup. "Even spirits yearn to savor life's essence," she murmurs, a flicker of longing evident.

~ heartwarming_moments += 1
~ romantic_interest += 1

-> cafe_closing

=== learn_lovers ===
# changeBackground: cafe_evening.png
"Fragments of their story linger still, echoing within every echo of laughter, every heartwarming greeting shared."

+ "Can those stories change my present?" -> mystery_unfolds
+ "Does the café still hold their energy?" -> energy_hopes

=== grandmother_past ===
# changeBackground: cafe_evening.png
"Her love infused this place with life. The devotion remains, a guiding light for all who follow."

~ heartwarming_moments += 1
-> mystery_unfolds

=== mystery_unfolds ===
"Each story both echoes and changes with each telling. Some call it magic, others the spirit weaving of time."

~ mystery_solved = true
-> cafe_closing

=== energy_hopes ===
"Their passion, now a part of this place, enlivens the walls with each heartbeat, each clock tick."

-> cafe_closing

=== duet_song ===
The harmony we create is pure magic, weaving our voices into a vibrant tapestry of sound that fills the café to every corner.

~ heartwarming_moments += 1
~ romantic_interest += 1

# changeBackground: cafe_evening.png
-> cafe_closing

=== savor_moment ===
The echoes of her melody become a tender embrace for all who listen, the pause they never knew they needed.

# changeBackground: cafe_evening.png
-> cafe_closing

=== cafe_closing ===
With the day's end, the spirit lingers at the door—a departure less a farewell and more a promise of return.

{heartwarming_moments > 2 and romantic_interest > 0:
    Her voice softer than whispers: "Memories entwine; I shall walk with you on this journey."
- else:
    "May tranquility accompany you," she murmurs before fading with the falling dusk.
}

=== memories_flashback ===
# changeBackground: cafe_past.png
In a sudden, vivid flash, time unravels—a bustling café of yesteryears emerges, laughter resounding against walls...

-> END