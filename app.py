from agno.agent import Agent
from agno.utils.log import logger
from agno.tools.file import FileTools
#from agno.tools.dalle import DalleTools
#from agno.models.ollama import Ollama
from agno.models.openai import OpenAIChat
#from agno.models.anthropic import Claude
from utils import get_ink_error_report, get_ink_playtest_report, get_ink_stats_report, find_potential_reports, evaluate_report, retry_until_folder_changes, retry_until_success, retry_until_success_result
from pathlib import Path
import os
import glob

enable_debug=False
enable_reasoning=False

# "Develop a high-quality text-based narrative game using Ink, incorporating branching storylines and engaging player choices."
user_input = input("Write your customer project directive statement: ")
if user_input == "":
    user_input = "Create a game prototype with the following idea: A romance between a hardworking cafe owner (female) and a spirit that haunts the new cafe building she inherited from a relative. The player plays the cafe owner."
    print(f"Using default input: {user_input}")

openai_model = "gpt-4o"

#llm=Ollama(id="mistral")
#llm=OpenAIChat(id=openai_model)
#llm=Claude(id="claude-3-5-sonnet-latest")

output_path = Path("output/")

with open('ink_guide.md', 'r') as f:
    ink_guide = f.read()


# Example individual agent definition
'''
agent_name = Agent(
    name="Agent Name",
    role="A expert agent in some domain, such as writing, coding, etc. (Be specific and treat like a human job description)",
    expected_output="Specific output expected from the agent, specifying format if needed but not filenames, etc.",
    # none or more of the following tools
    tools=[
        FileTools(base_dir=output_path), # IMPORTANT: can read and write files, e.g. read documentation, write documents, code, etc.
        DalleTools(), # ESSENTIAL: genrate images with DALL-E
        DuckDuckGoTools(), # web search
        PythonTools(), # write Python files, run Python code, use pip to install packages
        ShellTools(), # run a shell command
        SpiderTools(), # search web, scrape webpage at URL, crawl (explore) website for given starting URL
        CsvTools(), # CSV file read and write
        WikipediaTools(), # get summary of a topic from Wikipedia (i.e. search Wikipedia)
        YouTubeTools(), # get video captions for a given YouTube video URL (cannot search YouTube, use websearch for that)
        # and you can even simply add custom tools as Python function references, such as running a linter, executing code, get a quality metric for an image, etc.
    ],
    # don't change the below
    model=OpenAIChat(id=openai_model),
)
'''

# ---- PROJECT PLANNING AGENTS ----
narrative_writer = Agent(
    name="Narrative game story writer",
    role="The narrative game story writer creates immersive, interactive stories, developing characters, dialogue, and branching narratives that adapt to player choices. The write in complete scenes in a high level of detail.",
    expected_output="A series of scene overviews, with each scene about 200 words each",
    tools=[FileTools(base_dir=output_path)],
    model=OpenAIChat(id=openai_model),
    #reasoning=enable_reasoning,
    markdown=True,
    structured_outputs=True,
    show_tool_calls=True,
)

game_designer = Agent(
    name="Game Designer",
    role="Provides a structured plan on how game mechanics should be implemented in the Ink scripting system. Advises on scene structuring, branching choices, and interactive pacing.",
    expected_output="""A structured plan of each scene, based on the narrative game story. Consider this format:
```
# Narrative Structure for a Slice-of-Life Fetch Quest  

## Scene 1: The Coffee Shop  
- The player arrives at their favorite coffee shop on a chilly morning.  
- The smell of fresh espresso fills the air, and the usual hum of conversation surrounds them.  
- Mia, the barista, is behind the counter, but she looks unusually stressed.  
- A choice: **Talk to Mia or Order a coffee first**.  
  - If the player talks to Mia, she sighs and hesitates before sharing what's wrong.  
  - If the player orders coffee first, she tries to hide her frustration but still seems distracted.  

## Scene 2: Mia's Problem  
- If the player engages Mia, she admits she's run out of oat milk, and one of the regulars is waiting on their usual order.  
- She explains that her supplier won't restock until tomorrow, and she doesn't want to disappoint the customer.  
- A choice: **Offer to get oat milk or just sympathize**.  
  - If the player offers to help, she looks relieved and suggests trying the corner store.  
  - If the player sympathizes but does nothing, she thanks them but continues to look stressed. The player goes about their day as usual.  

## Scene 3: Finding the Oat Milk  
- If the player takes the quest, they head to the corner store, a small, cluttered shop a few blocks away.  
- The shelves are half-empty, and the store is unusually busy.  
- A choice: **Check the dairy section or ask the cashier**.  
  - If they check the shelves, they might find the last carton of oat milk.  
  - If they ask the cashier, they learn that oat milk sold out earlier that morning, but there might be some at the supermarket.  

## Scene 4: The Decision at the Store  
- If the player finds oat milk, they can take it and return to Mia immediately.  
- If the store is out, the player must decide:  
  - **Go to the supermarket**: It's further away but almost guaranteed to have oat milk.  
  - **Give up and return to Mia empty-handed**.  
- If they go to the supermarket, they find plenty of oat milk but have spent extra time.  

## Scene 5: Returning to Mia  
- If the player brings back oat milk, Mia lights up with relief. She thanks them enthusiastically and hands them a free coffee as a reward.  
- If the player returns without oat milk, Mia sighs but nods in appreciation for the effort.  
- If the player never tried to help, Mia makes do without and the scene simply moves on.  

## End of Story  
- The player leaves the coffee shop, either feeling like they made a difference or simply going about their usual routine.  
- The scene ends based on their level of involvement in Mia's problem.  
```
""",
    tools=[FileTools(base_dir=output_path)],
    model=OpenAIChat(id=openai_model),
    #reasoning=enable_reasoning,
    markdown=True,
    structured_outputs=True,
    show_tool_calls=True,
)

ink_script_developer = Agent(
    name="Ink Script Developer",
    role="Writes structured Ink scripts to implement the game's branching narrative. Ensures logical flow, proper state management, and engaging player choices while adhering to requirements. Ink coding guide (customise for the theme):\n\n" + ink_guide,
    expected_output="A well-structured Ink script (.ink) implementing interactive narrative and state logic. Always saves its .ink file to disk.",
    tools=[FileTools(base_dir=output_path)],
    model=OpenAIChat(id=openai_model),
    #reasoning=enable_reasoning,
    markdown=True,
    structured_outputs=True,
    show_tool_calls=True,
)

development_team = Agent(
    name="Development Team",
    team=[ink_script_developer], #background_artist
    instructions=[
        "Read the game scene overview document by opening the .md file with the tools. Understand the story and scenes described in the document. "
        f"Bear in mind the user prompt: \"{user_input}\". "
        "Ink Script Developer must create well-structured, interactive scripts that match design specifications. "
        "The game script must cover all scenes in the narrative overview. "
        "All scenes should be written in detailed prose of several lines, not being too brief, of about a paragraph in length. "
        "The game script must be at least 10 choices deep in structure. "
        "The game script must be based on the design doc. "
        "Must save script to .ink file. ",
        #"Background Artist should create environment visuals that match the tone and aesthetic of the game.",
    ],
    model=OpenAIChat(id=openai_model),
    reasoning=enable_reasoning,
    markdown=True,
    structured_outputs=True,
    show_tool_calls=True,
    debug_mode=enable_debug,
)

# background_artist = Agent(
#     name="Background Artist",
#     role="Creates detailed 2D background art for the game, ensuring consistency with its visual style. Works closely with Ink Script Developer to obtain filenames for graphics assets deliverables, and with writers to align visual storytelling with narrative tone.",
#     expected_output="A set of rendered background images adhering to the game's art style and scene requirements.",
#     tools=[FileTools(base_dir=output_path), DalleTools()],
#     model=OpenAIChat(id=openai_model),
# )

solo_software_tester = Agent(
    name="Software Tester",
    role="Tests Ink scripts and game code for functional correctness, syntax errors, and running test tools, and looking for unintended narrative flows or logical errors. Do not comment on positive aspects of the game, only on any issues. If no issues found, keep note brief.",
    tools=[FileTools(base_dir=output_path), get_ink_error_report, get_ink_stats_report, get_ink_playtest_report],
    model=OpenAIChat(id=openai_model),
    instructions=[
        "Thoroughly test all deliverables to ensure functionality, quality, and adherence to requirements.",
        "Software Tester must check for logic errors, syntax issues, and unintended narrative breaks in the Ink script.",
        "Always saves report to file. Saving a report to file is a MANDATORY part of the this job."
    ],
    expected_output="""A report in the following format and save to disk as `qa_report.md`:
```
# QA report

## Bugs

[List errors]

## Warnings

[List errors]

## Narrative quality

[Detail narrative quality]

## Conclusion

Result: [PASS|FAIL]
```
    """,
    ##reasoning=enable_reasoning,
    markdown=True,
    structured_outputs=True,
    show_tool_calls=True,
    debug_mode=enable_debug,
)

output_folder="output/"
max_task_retry=5

def development_iteration():
    """Runs a single iteration of the development cycle."""
    qa_feedback = ""
    if os.path.exists(output_folder + "qa_report.md"):
        with open(output_folder + "qa_report.md", 'r') as f:
            qa_feedback = f"QA feedback: {f.read()}\n"
        old_ink_files = glob.glob(f"{output_folder}*.old")
        for old_file in old_ink_files:
            with open(old_file, 'r') as f:
                qa_feedback += f"\n--- OLD file to fix, {os.path.basename(old_file)}:\n\n```ink\n{f.read()}```"
    retry_until_folder_changes(
        task_func=lambda: (
            development_team.print_response(
                f"Develop Ink script for game, given the narrative overview already created (check files in folder). "
                f"Save the resulting script to a .ink file. "
                f"{qa_feedback}",
                stream=True,
                show_full_reasoning=True
            )
        ),
        folder_path=output_folder,
        max_retries=max_task_retry,
        task_desc="🛠️ Writing Ink script",
        log_func=logger.info
    )

    # remove previous QA and acceptance testing reports
    [os.remove(output_folder + f) for f in ['qa_report.md', 'acceptance_testing_report.md'] if os.path.exists(output_folder + f)]

    retry_until_success(
        task_func=lambda: (
            solo_software_tester.print_response(
                f"Test Ink script .ink file. Identify any functional issues, narrative inconsistencies, or usability problems. "
                f"Generate a QA report and save the file `qa_report.md`. ",
                stream=True,
                show_full_reasoning=True
            )
        ),
        success_check_func=lambda: os.path.exists(os.path.join(output_folder, "qa_report.md")),
        max_retries=max_task_retry,
        task_desc="🔍 Performing quality assurance",
        log_func=logger.info
    )

    qa_status = evaluate_report(output_folder + "qa_report.md")
    if qa_status == "FAIL":
        logger.info(f"❌ QA failed development iteration.\n")
        return "FAIL"

    logger.info(f"✅ Quality Assurance Passed.\n")

    logger.info(f"✅ Development is completed.\n")

    return "PASS"

if __name__ == "__main__":
    print("\n🚀 Starting Process...\n")

    retry_until_folder_changes(
        task_func=lambda: (
            narrative_writer.print_response(
                f"Write a narrative overview given the following brief: {user_input}"
                f"Save the narrative overview to a file. ",
                stream=True,
                show_full_reasoning=True
            )
        ),
        folder_path=output_folder,
        max_retries=max_task_retry,
        task_desc="✏️ Writing narrative overview",
        log_func=logger.info
    )

    retry_until_success_result(
        task_func=lambda: development_iteration(),
        success_check_func=lambda result: result == "PASS",
        max_retries=max_task_retry,
        task_desc="🚀 Development iteration",
        log_func=logger.info,
        do_between_reties_func=lambda: (
            [os.remove(f) for f in glob.glob(f"{output_folder}*.old")],
            [os.remove(f) for f in glob.glob(f"{output_folder}*.ink.json")],
            [os.rename(f,f.replace(".ink", ".old")) for f in glob.glob(f"{output_folder}*.ink")]
        )
    )

    print(f"\n✅ Run complete. Check output folder: {output_folder}")

