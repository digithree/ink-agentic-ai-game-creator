from agno.agent import Agent
from agno.utils.log import logger
from agno.tools.file import FileTools
#from agno.tools.dalle import DalleTools
from agno.models.openai import OpenAIChat
from agno.models.ollama import Ollama
from agno.models.anthropic import Claude
from utils import get_ink_error_report, get_ink_playtest_report, get_ink_stats_report, evaluate_report, retry_until_folder_changes, retry_until_success, retry_until_success_result, ink_files_log_stats, load_config
from pathlib import Path
from datetime import datetime
import os
import glob
import shutil
import time


config = load_config()

if config['enable_ask_user_for_prompt']:
    prompt = input("Write your customer project directive statement: ")
if prompt == "":
    prompt = config['sample_prompt'].strip()
    if prompt == "":
        print("No prompt, check config.yaml")
        exit()
    print(f"Using default config prompt: {prompt}")


def create_llm():
    if config['llm_provider'] == "openai":
        return OpenAIChat(id=config['llm_model'])
    elif config['llm_provider'] == "openai":
        return OpenAIChat(id=config['llm_model'])
    elif config['llm_provider'] == "openai":
        return OpenAIChat(id=config['llm_model'])
    else:
        print("No valid LLM config, check in config.yaml")
        exit()
    return Ollama(id="llama3.2")

output_path = Path(config['output_folder_for_build'])

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
    model=create_llm(),
)
'''

# ---- Agent 1: story writer ----
# Simple output to `overview.md` with ideas for narrative to try to solidify that for Ink code
narrative_writer = Agent(
    name="Narrative game story writer",
    role="The narrative game story writer creates immersive, interactive stories, developing characters, dialogue, and branching narratives that adapt to player choices. The write in complete scenes in a high level of detail.",
    expected_output="A scene overview, with each scene about 200 words. Save to file `overview.md`",
    tools=[FileTools(base_dir=output_path)],
    model=create_llm(),
    markdown=True,
    structured_outputs=True,
    show_tool_calls=config['enable_detailed_logging'],
)

# ---- Agent 2: Ink script writer (on team of 1, for better file handling) ----
# Writes Ink script code. Will attempt to fix old code in development loop to improve stats
ink_script_developer = Agent(
    name="Ink Script Developer",
    role="Writes structured Ink scripts to implement the game's branching narrative. Ensures logical flow, proper state management, and engaging player choices while adhering to requirements. Ink coding guide (customise for the theme):\n\n" + ink_guide,
    expected_output="A well-structured Ink script (.ink) implementing interactive narrative and state logic. Always saves its .ink file to disk.",
    tools=[FileTools(base_dir=output_path)],
    model=create_llm(),
    markdown=True,
    structured_outputs=True,
    show_tool_calls=config['enable_detailed_logging'],
)

development_team = Agent(
    name="Development Team",
    team=[ink_script_developer], #background_artist
    instructions=[
        "Read the game scene overview document by opening `overview.md` file. Understand the story and scenes described in the document. "
        f"Bear in mind the user prompt: \"{prompt}\". "
        "Ink Script Developer must create well-structured, interactive scripts that match design specifications. "
        "The game script must cover all scenes in the narrative overview. "
        "All scenes should be written in detailed prose of several lines, not being too brief, of about a paragraph in length. "
        "The game script must be at least 10 choices deep in structure. "
        "The game script must be based on the design doc. "
        "Must save script to .ink file. ",
        #"Background Artist should create environment visuals that match the tone and aesthetic of the game.",
    ],
    model=create_llm(),
    reasoning=config['enable_agent_reasoning'],
    markdown=True,
    structured_outputs=True,
    show_tool_calls=config['enable_detailed_logging'],
    debug_mode=config['enable_debug_logging'],
)

# ---- Agent X: DISABLED, background artist (too expensive to run DALLE in testing ----
'''
background_artist = Agent(
    name="Background Artist",
    role="Creates detailed 2D background art for the game, ensuring consistency with its visual style. Works closely with Ink Script Developer to obtain filenames for graphics assets deliverables, and with writers to align visual storytelling with narrative tone.",
    expected_output="A set of rendered background images adhering to the game's art style and scene requirements.",
    tools=[FileTools(base_dir=output_path), DalleTools()],
    model=create_llm(),
)
'''

# ---- Agent 3: Software tester (on team of 1, for better file handling and tool use) ----
# Uses inklecate tools to get PASS or FAIL on key stats, and cause dev looping with below stats min
# Stats are errors, warnings, longest path too short, not enough words or knots (labels)
solo_software_tester = Agent(
    name="Software Tester",
    role="Tests Ink scripts and game code for functional correctness, syntax errors, and running test tools, and looking for unintended narrative flows or logical errors. Do not comment on positive aspects of the game, only on any issues. If no issues found, keep note brief.",
    tools=[FileTools(base_dir=output_path), get_ink_error_report, get_ink_stats_report, get_ink_playtest_report],
    model=create_llm(),
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
    markdown=True,
    structured_outputs=True,
    show_tool_calls=config['enable_detailed_logging'],
    debug_mode=config['enable_debug_logging'],
)

test_team = Agent(
    name="Test Team",
    team=[solo_software_tester],
    instructions=[
        "Software Tester must check for logic errors, syntax issues, and unintended narrative breaks in the Ink script.",
        "Must save script to `qa_report.md` file. "
    ],
    model=create_llm(),
    reasoning=config['enable_agent_reasoning'],
    markdown=True,
    structured_outputs=True,
    show_tool_calls=config['enable_detailed_logging'],
    debug_mode=config['enable_debug_logging'],
)

# ---- LOGGER ----

if config['enable_file_logging']:
    log_output_file = config['log_filename']
    f_log = open(log_output_file, 'a')
else:
    f_log = None

def log(text):
    logger.info(text)
    if config['enable_file_logging']:
        try:
            f_log.write(f"{text}\n")
        except IOError as e:
            print(f"Failed to log to file: {e}")

# -------------------------------------------------------
# ---- CREATE GAME ORCHESTRATION ----

def development_iteration():
    """Runs a single iteration of the development cycle."""
    qa_feedback = ""
    if os.path.exists(config['output_folder_for_build'] + "qa_report.md"):
        with open(config['output_folder_for_build'] + "qa_report.md", 'r') as f:
            qa_feedback = f"QA feedback: {f.read()}\n"
        old_ink_files = glob.glob(f"{config['output_folder_for_build']}*.old")
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
        folder_path=config['output_folder_for_build'],
        max_retries=config['max_task_retries'],
        task_desc="🛠️ Writing Ink script",
        log_func=log
    )

    # remove previous QA and acceptance testing reports
    [os.remove(config['output_folder_for_build'] + f) for f in ['qa_report.md', 'acceptance_testing_report.md'] if os.path.exists(config['output_folder_for_build'] + f)]

    retry_until_success(
        task_func=lambda: (
            test_team.print_response(
                f"Test Ink script .ink file. Identify any functional issues, narrative inconsistencies, or usability problems. "
                f"Generate a QA report and save the file `qa_report.md`. ",
                stream=True,
                show_full_reasoning=True
            )
        ),
        success_check_func=lambda: os.path.exists(os.path.join(config['output_folder_for_build'], "qa_report.md")),
        max_retries=config['max_task_retries'],
        task_desc="🔍 Performing quality assurance",
        log_func=log
    )

    qa_status = evaluate_report(config['output_folder_for_build'] + "qa_report.md")
    if qa_status == "FAIL":
        log(f"❌ QA failed development iteration.")
        return "FAIL"

    log(f"✅ Quality Assurance Passed.\n")

    log(f"✅ Development is completed.\n")

    return "PASS"

def run_task_iteration():
    log("\n🚀 Starting Process...\n")

    retry_until_folder_changes(
        task_func=lambda: (
            narrative_writer.print_response(
                f"Write a narrative overview given the following brief: \"{prompt}\". "
                f"Save the narrative overview to a file. ",
                stream=True,
                show_full_reasoning=True
            )
        ),
        folder_path=config['output_folder_for_build'],
        max_retries=config['max_task_retries'],
        task_desc="✏️ Writing narrative overview",
        log_func=log
    )

    retry_until_success_result(
        task_func=lambda: development_iteration(),
        success_check_func=lambda result: result == "PASS",
        max_retries=config['max_task_retries'],
        task_desc="🚀 Development iteration",
        log_func=log,
        do_between_reties_func=lambda: (
            [os.remove(f) for f in glob.glob(f"{config['output_folder_for_build']}*.old")],
            [os.remove(f) for f in glob.glob(f"{config['output_folder_for_build']}*.ink.json")],
            [os.rename(f,f.replace(".ink", ".old")) for f in glob.glob(f"{config['output_folder_for_build']}*.ink")]
        )
    )

    log(f"\n✅ Run complete. Check output folder: {config['output_folder_for_build']}")
    return "PASS"

def create_game():
    # WARNING! deletes all files before starting 😅
    if config['clear_output_folder_on_run_start']:
        shutil.rmtree(config['output_folder_for_build'])
        os.mkdir(config['output_folder_for_build'])
        log(f"💣 Cleared {config['output_folder_for_build']} folder")

    retry_until_success_result(
        task_func=lambda: run_task_iteration(),
        success_check_func=lambda result: result == "PASS" and any(file.endswith(".ink") for file in os.listdir(config['output_folder_for_build'])),
        max_retries=config['max_run_retries'],
        task_desc="✨ Task iteration",
        log_func=log,
        do_between_reties_func=lambda: (
            shutil.rmtree(config['output_folder_for_build']) if config['clear_output_folder_on_run_start'] else "",
            os.mkdir(config['output_folder_for_build'] if config['clear_output_folder_on_run_start'] else "")
        )
    )

def transfer_output_success():
    os.makedirs(config['output_folder_for_success_save'], exist_ok=True)

    for item in os.listdir(config['output_folder_for_build']):
        source_path = os.path.join(config['output_folder_for_build'], item)
        destination_path = os.path.join(config['output_folder_for_success_save'], item)

        if os.path.isdir(source_path):
            shutil.copytree(source_path, destination_path, dirs_exist_ok=True)
        else:
            shutil.copy2(source_path, destination_path)

if __name__ == "__main__":
    log("-------------------------------------------")
    log(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    log("Creating new game with instructions:")
    log(f"{prompt}\n")

    start_time = time.time()

    do_post_gen_logging = False
    try:
        create_game()

        log(f"\n✅ Run task iteration PASSed.")
        #log("TODO, files to get images for: ")
        #log(ink_files_extract_filenames(config['output_folder_for_build']))

        transfer_output_success()

        do_post_gen_logging = True
    except Exception as e:
        log(f"💀 Create game task failed with error. {e}")
    
    end_time = time.time()
    execution_time = end_time - start_time
    minutes = int(execution_time // 60)
    seconds = int(execution_time % 60)
    log(f"⏱️ Create game took {minutes}:{seconds}\n\n")

    if config['enable_post_success_ink_stats_logging'] and do_post_gen_logging:
        log("🚦 Please wait for game report to generate...")
        log(ink_files_log_stats(config['output_folder_for_build']))
    
    if f_log is not None:
        f_log.close()
