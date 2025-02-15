# Narrative Game Builder

## DISCLAIMER AND NOTE

This project was created using ChatGPT and Copilot, and is the first project I have created 'assisted' by LLM tools in this way. It is primarily an investigation of the state of the art of so-called agentic systems, particularly how they might replace software developer effort, and even that of an entire project development team.

The example case I have chosen here is the one that got me into coding as a kid – making a computer game. And, like when I was a kid, it is for a text adventure. While I created this software using AI systems, the idea was to see if it could create an automated system to create something automatically given just a one line idea. The tools were chosen based on ease of use, terseness of coding and 'comprehension' by ChatGPT as development 'copilot'.

The project is set up using [Agno](https://github.com/agno-agi/agno) with 3 agents (acutally 5, two are wrapped on teams):

1. Narrative game story writer
2. Ink Script Developer (Development Team)
3. Software Tester (Test Team)

> Side bar: [Ink](https://www.inklestudios.com/ink/) is an interactive narrative language and engine developed by [Inkle Studios](https://www.inklestudios.com). Check out their Time Game of the Year 2014 winning game [80 days](https://www.inklestudios.com/80days/).

The narrative writer (1) always runs just once, and then the dev (2) and tester (3) run in a loop until the results satisfy the criteria minimum criteria of the game (which is very forgiving, but necessarily limited in scope or the bar is too high): no syntax error or lint warnings, longest choice path at least 5 deep, at least 500 words total and at least 10 'knots' (what Ink calls the story branch points).

Note that Agno seems to do file read and write better when an agent is on a team, so the dev and tester are wrapped in another agent to set it to a team. Teams are generally intended for more than one assigned agent, which can work, but for closed purpose tasks like the on I have created here we need more predictability.

There was also an 'artist' to work with AI image generation tool DALL-E but this was expensive on credit to test, and I didn't bother completing it. It would be simple enough as a small project for you to integrate this, there is some commented out code and web front end for InkJS expects it (though is tolerant for it not being there).

---

The results are mixed. I have been able to create something which in most cases will output a functioning game, but it is a very short game, very generic and uninteresting to play. I had to build the agentic runner to retry steps at every level if either the quality wasn't good or if the task simply failed to yield a result, even though the system outputed it was done (i.e. check for file changes). In many cases, the system simply fails entirely, or does not create a game to the desired spec. In all cases I've tested so far, it also struggles and ultimately fails to set up any actual stakes or failure cases, making the game, short as it is, too easy.

However, there are some interesting features:

- it does use the agentic system correctly, which interestingly has file access, though this often fails and needs a retry loop
- the generated Ink script can have a minimal level of hidden tracking logic, like flags and 'level' tracking, e.g. relationship tracking
- the Ink game path permutation runner was particularly fun to write, and I had to write a lot of it myself by hand as it was too complex for ChatGPT to figure out how to do. It also detects infinite choice loops!
- the InkJS custom runner, with a feature to automatically save progress. The games are super short so this is not an important feature for this use, but actually this will run much larger Ink games so it might be useful on its own

I'm particularly sensitive to the concerns of artists regarding AI, in many different aspects, particularly in job replacement, theft of work through scrapping for training data, and the lowing of the quality and substance of art. My project here is an experiment, just a toy really, not a tool that _actually_ aspires to replace game designers. I think it is important for us all to understand where the state of the art is today regarding these tools since, if it can be easily done, then people will be doing it and we should be aware of that.

What I see today (writing in Feb 2025) at least is that **self-direction is not yet viable for complex agentic systems.** They need much hand-holding and even then the results are mediocre. My first attempts were just to set up some agent with 'job' descriptions and set a complex task, but this yielded virtually nothing. There is no yet "plz craete game" button. What this project demostrates really is the lengths you have to go just to get a very small amount of success.

---

Some prompts that were mostly successful:

- The journey of a wizard from the foot of a giant mountain to visit the very top, where they will find a secret magical treasure that can heal the world.
- The journey of an ant that becomes sentient and decides to leave the ant hill to discover the meaning of life.

Prompts that never worked for me:

- In a world of smog, air is a commodity. Make your way across the wasteland to find a new source of oxygen in the rocks.
- A game about escaping prison. There should be lots of chances to get caught which end the game in failure.

Example failure message (from last test failure):

```
INFO     ⚠️ Failed attempt 1 for task 🔍 Performing quality assurance. Retrying...
INFO     🔄 🔍 Performing quality assurance, attempt 2/5...                                               
INFO     Reading files in : output
INFO     ✅ No errors detected in 'output/adventure_game.ink'.
INFO     👀 Ink script features QA report for 'output/adventure_game.ink':
         ❌ FAIL Number of words 445 is below minimum of 500. REFACTOR CODE TO INCREASE WORD COUNT, EXPANDING THE NARRATIVE DETAIL!
INFO     ❌ Ink error report for 'output/adventure_game.ink':
         ➡️  Possible Story Paths Permutations: 18
         ❌ Longest Story Choice Depth: 3
         ❌ FAIL: CRITICAL ISSUES WITH INK SCRIPT, MUST FIX BUGS IMMEDIATELY
         ❌ FAIL: Longest length of story choice path is NOT enough; is 3 but should be at least 5.
         More story choice depth should be added to the story, it is not long enough. THIS IS CONSIDERED A BUG.
INFO     Saved: output/qa_report.md
...
INFO     ℹ️ Evaluating report in output/qa_report.md.
INFO     ❌ QA failed development iteration.
INFO     ⚠️ Failed attempt 5 for task 🚀 Development iteration. Retrying...
INFO     ❌ Failed task: 🚀 Development iteration
INFO     💀 Create game task failed with error. Task failed after 5 attempts.
INFO     ⏱️ Create game took 9:35
```

--- FROM BELOW, GENERATED BY CHATGPT

## Overview

Narrative Game Builder is an experimental tool for generating interactive narratives using Ink and large language models. This project is a work in progress and heavily depends on the quality of the language model used. The generation process is simple and often fails to produce successful results, but future improvements are planned.

## Requirements

The system officially supports macOS and requires the following:

- **Python**: Version 3.9+
- **Ink** and **Inklecate**: https://www.inklestudios.com/ink/
- **npm http-server**: Installed globally via `npm install -g http-server`
- **LLM API Key**: Either an OpenAI or Anthropic API key must be available in environment variables, or alternatively, [Ollama](https://ollama.com/) should be installed for local LLM use.

## Installation

To install the required dependencies:

```sh
pip install -r requirements.txt
```

Ensure `npm http-server` is installed globally:

```sh
npm install -g http-server
```

## Configuration

`config.yaml` contains many configuraiton options, such as:

- LLM provider and model, e.g. OpenAI, Anthropic, Ollama
- Ink script metric standard, e.g. a certain choice path depth, total number of words, etc.
- Auto-mode
- Output settings
- Debugging and logging information

## Running the Application

To run the narrative generation script, execute:

```sh
python app.py
```

You will be prompted to enter a description for the game, which will guide the Ink story generation.

## Running the Custom InkJS Server

The project includes a custom InkJS server to serve Ink stories. To set it up and run:

1. **Setup the InkJS environment:**

   ```sh
   ./setup_inkjs.sh
   ```

2. **Launch the server:**

   ```sh
   ./launch_inkjs.sh
   ```

3. **Access the game:**

   Open [http://localhost:8080](http://localhost:8080) in your browser to try the game.

Disable caching on your browser for testing multiple times to insure latest update is used.

### Alternative Testing Method

You can test the generated Ink story in pure text format in the terminal using:

```sh
inklecate -p output/your_file.ink
```

## Notes on Current Limitations

- The generation process **frequently fails** to produce a coherent output.
- The project is highly dependent on the LLM used, and results vary significantly.
- The current implementation is **a simple approach** that can be expanded and improved with more sophisticated logic and better model prompting.

This repository is an early-stage prototype, and contributions or suggestions for improvement are welcome!

