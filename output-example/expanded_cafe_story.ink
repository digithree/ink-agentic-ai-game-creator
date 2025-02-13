// Variables
VAR cafe_name = "Unnamed Cafe"
VAR has_ghost_interacted = false

// Start of the game
# changeBackground: cafe_exterior.png
Welcome to the tiny, charming town of Elmswood. The sun glints over "The Twisted Brew" cafe as you, Amelia Parker, stand at the threshold of your newfound legacy.

+ [Enter the cafe] -> enter_cafe

=== enter_cafe ===
# changeBackground: cafe_interior.png
The cafe greets you with the scent of dust and nostalgia. The wooden floors creak underfoot, and a strange chill dances in the shadows.

"Here's to new beginnings," you whisper. But soon, you realize it's not just yourself you are speaking to...

+ [Inspect the counter] -> inspect_counter
+ [Approach the corner table] -> corner_table

=== inspect_counter ===
The counter is worn but comfy. Amongst old receipts, you find an old family photo—a man, Nathaniel, beside your aunt.

~ has_ghost_interacted = true

\n
"You must be curious," a quiet voice murmurs—a hint of laughter in the echo.

+ [Ignore and continue cleaning.] -> cafe_cleaning
+ [Respond to the voice.] -> ghost_interaction

=== corner_table ===
You sense someone watching. Then you see him—a translucent figure in vintage attire.

~ has_ghost_interacted = true

A pang of nostalgia, the ghost named Nathaniel, smiles softly.

+ "Who are you?" -> ghost_interaction
+ "This cannot be real!" -> cafe_cleaning

=== ghost_interaction ===
"I am Nathaniel," he replies, his words tinged with ethereal warmth.

+ "Why are you here?" -> story_time
+ "How can I help you?" -> help_ghost

=== cafe_cleaning ===
You decide there are more pressing matters—such as revitalizing the cafe.

# changeBackground: cafe_cleaning.png
You spend the day cleaning, your mind sequestered in thought. Shadows dance in corners as you dust and sweep.

+ [Go back to the corner table.] -> corner_table
+ [Focus on renovating.] -> renovation_plans

=== story_time ===
# changeBackground: cafe_history.png
Nathaniel reveals old tales and old dreams—a writer, there’s poetry unread, words unshared.

"You and your aunt shared kindness," he mentions, with wistful eyes.

+ [Listen more.] -> listen_more
+ [Plan a memorial.] -> help_ghost

=== help_ghost ===
You've decided to aid Nathaniel in his unfulfilled dreams. The cafe is not just yours; it’s part of this community, living and otherwise.

# changeBackground: cafe_evening.png
+ [Host a literary evening.] -> literary_evening
+ [Dive into the hidden cellar.] -> hidden_cellar

=== listen_more ===
# changeBackground: cafe_evening.png
Each evening, over brewed coffee, Nathaniel whispers stories. His compassion draws you, and bonds form with words.

+ "I’ll fulfill your dream of a public reading." -> literary_evening
+ "What binds you here?" -> hidden_cellar

=== renovation_plans ===
Determined, you begin crafting new visions for the cafe. Every corner needs the promise of life.

+ [Include heritage decor.] -> heritage_decor
+ [Focus on the modern look.] -> modern_look

=== literary_evening ===
# changeBackground: cafe_event.png
You prepare for a gathering. Words once lost rekindle through the laughter of a captivated crowd.

Nathaniel stands at the back, smiling—a peace settling.

+ [Read the letters.] -> farewell_scene
+ [Invite the town's historian.] -> farewell_scene

=== hidden_cellar ===
# changeBackground: cellar.png
Below dust-covered nooks, you uncover countless letters of love never confessed between Nathaniel and your aunt.

You resolve to see his dreams fulfilled.

+ [Hold a ceremony to free him.] -> farewell_scene
+ [Write his story for locals.] -> farewell_scene

=== heritage_decor ===
Every object tells a story; the narrative is as full of laughter as it is of gentle memories.

+ [Plan a grand opening.] -> farewell_scene
+ [Invite Nathaniel's distant relatives.] -> farewell_scene

=== modern_look ===
Sleek designs blended with old stories; Nathaniel whispers suggestions that resonate with your soul.

+ [Plan a launch event.] -> farewell_scene
+ [Feature local artists.] -> farewell_scene

=== farewell_scene ===
# changeBackground: sunrise.png
As dawn breaks over the Elmswood horizon, peace descends. Nathaniel appears one last time before you. It’s a farewell woven in smiles and gratitude.

+ "Thank you, Nathaniel." -> end_scene
+ "I’ll keep your memory alive." -> end_scene

=== end_scene ===
The Twisted Brew cafe, now full of life and whispered tales, stands as a testament to bridging worlds—a romance entwining past and present.

# changeBackground: cafe_exterior.png
-> END