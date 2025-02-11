from agno.agent import Agent
from agno.tools.shell import ShellTools
from agno.tools.file import FileTools
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.dalle import DalleTools
from agno.tools.csv_toolkit import CsvTools
from agno.tools.python import PythonTools
from agno.tools.wikipedia import WikipediaTools
#from agno.models.ollama import Ollama
from agno.models.openai import OpenAIChat
from pathlib import Path
from orchestrator import Orchestrator

# "Develop a high-quality text-based narrative game using Ink, incorporating branching storylines and engaging player choices."
user_input = input("Write your CEO project directive statement: ")

#llm=Ollama(id="llama3.2")
llm=OpenAIChat(id="gpt-4o")

output_dir = Path("output/")

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
        FileTools(), # IMPORTANT: can read and write files, e.g. read documentation, write documents, code, etc.
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
    model=llm,
)
'''

# ---- PROJECT PLANNING AGENTS ----
project_owner = Agent(
    name="Project Owner",
    role="Oversees the project's vision and defines high-level objectives. Ensures the direction aligns with business goals and creative intent, providing strategic guidance throughout development.",
    expected_output="A well-defined project goal with clear priorities, scope, and constraints.",
    tools=[FileTools(), DuckDuckGoTools()],
    model=llm,
)

project_manager = Agent(
    name="Project Manager",
    role="Breaks down the project into sprint milestones and ensures team coordination. Tracks dependencies, manages deadlines, and ensures deliverables align with the defined project roadmap.",
    expected_output="A structured sprint plan detailing milestones, deliverables, and dependencies.",
    tools=[FileTools(), CsvTools()],
    model=llm,
)

market_researcher = Agent(
    name="Market Researcher",
    role="Analyzes industry trends, competitor offerings, and player expectations. Synthesizes insights from external sources to refine product direction and identify unique selling points.",
    expected_output="A market research report including industry trends, competitor analysis, and user expectations.",
    tools=[DuckDuckGoTools(), WikipediaTools()],
    model=llm,
)

# ---- REQUIREMENTS GATHERING & ASSESSMENT AGENTS ----
product_owner_writer = Agent(
    name="Product Owner (Requirements Writer)",
    role="Translates high-level project goals into structured feature requirements. Works closely with designers and developers to ensure clarity and feasibility of implementation.",
    expected_output="A formal requirements document detailing features, constraints, and expected outcomes.",
    tools=[FileTools()],
    model=llm,
)

product_owner_evaluator = Agent(
    name="Product Owner (Evaluator)",
    role="Reviews completed deliverables against requirements. Ensures features meet project goals, adhere to specifications, and maintain consistency within the overall vision.",
    expected_output="An evaluation report comparing deliverables to original requirements with feedback on any gaps.",
    tools=[FileTools()],
    model=llm,
)

game_designer_requirements = Agent(
    name="Game Designer (Requirements Input)",
    role="Defines gameplay mechanics, narrative structure, and interaction systems. Ensures gameplay is engaging and aligns with the project's themes and goals.",
    expected_output="A game design document outlining core mechanics, balance considerations, and player interactions.",
    tools=[FileTools()],
    model=llm,
)

game_designer_code_advisor = Agent(
    name="Game Designer (Code Advisor)",
    role="Provides structured guidance on how game mechanics should be implemented in the Ink scripting system. Advises on scene structuring, branching choices, and interactive pacing.",
    expected_output="Annotated Ink script structure recommendations or pseudocode for implementing gameplay.",
    tools=[FileTools(), PythonTools()],
    model=llm,
)

user_focus_group_requirements = Agent(
    name="User Focus Group (Requirements Input)",
    role="Simulates a range of player perspectives to anticipate usability issues and engagement factors. Provides insights to refine requirements for an optimal player experience.",
    expected_output="A user perspective report suggesting refinements to gameplay and user experience requirements.",
    tools=[],
    model=llm,
)

user_focus_group_evaluator = Agent(
    name="User Focus Group (Evaluator)",
    role="Evaluates completed deliverables from a player perspective. Assesses if the content is engaging, intuitive, and aligns with user expectations based on initial goals.",
    expected_output="A usability evaluation report listing engagement strengths, pain points, and player reception insights.",
    tools=[],
    model=llm,
)

ux_designer = Agent(
    name="UX Designer",
    role="Designs interface flows, interactions, and player feedback systems. Ensures intuitive and accessible navigation across the game's narrative structure.",
    expected_output="A UX specification document with wireframes, interaction models, and accessibility considerations.",
    tools=[FileTools(), DalleTools()],
    model=llm,
)

# ---- DEVELOPMENT AGENTS ----
ink_script_developer = Agent(
    name="Ink Script Developer",
    role="Writes structured Ink scripts to implement the game’s branching narrative. Ensures logical flow, proper state management, and engaging player choices while adhering to requirements. Ink coding guide:\n\n" + ink_guide,
    expected_output="A well-structured Ink script implementing interactive narrative and state logic.",
    tools=[FileTools(), PythonTools(), ShellTools()],
    model=llm,
)

background_artist = Agent(
    name="Background Artist",
    role="Creates detailed 2D background art for the game, ensuring consistency with its visual style. Works closely with UX designers and writers to align visual storytelling with narrative tone.",
    expected_output="A set of rendered background images adhering to the game's art style and scene requirements.",
    tools=[FileTools(), DalleTools()],
    model=llm,
)

# ---- QUALITY ASSURANCE AGENTS ----
software_tester = Agent(
    name="Software Tester",
    role="Tests Ink scripts and game code for functional correctness, debugging syntax errors and unintended narrative flows. Ensures a smooth and error-free experience for players.",
    expected_output="A bug report detailing logic issues, script errors, and potential narrative inconsistencies.",
    tools=[FileTools(), PythonTools()],
    model=llm,
)

game_tester = Agent(
    name="Game Tester",
    role="Performs playtests to evaluate gameplay balance, progression flow, and overall experience. Identifies inconsistencies in storytelling, pacing, and player engagement.",
    expected_output="A gameplay test report with feedback on narrative cohesion, interaction pacing, and engagement quality.",
    tools=[FileTools()],
    model=llm,
)

# --- Teams ---

# Example team agent definition
'''
team_name = Agent(
    name="Team Name",
    team=[agent_1, agent_2, agent_3], # etc.
    instructions=[ # instructions should be written carefully so they apply to the whole team and any task can be picked up by the team generally
        "Team must do this task",
        "Team should pay attention to this",
        "Essential thing for team to know"
    ],
    # don't change the below
    model=llm,
    reasoning=True,
    markdown=True,
    structured_outputs=True,
    show_tool_calls=True,
)
'''

# ---- PROJECT PLANNING TEAM ----
project_planning_team = Agent(
    name="Project Planning Team",
    team=[project_owner, project_manager, market_researcher],
    instructions=[
        "Break down the high-level project goal into a structured plan with milestones and deliverables.",
        "Ensure the project roadmap aligns with market trends, business goals, and feasibility constraints.",
        "Gather relevant market data to support planning decisions and feature prioritization.",
    ],
    model=llm,
    reasoning=True,
    markdown=True,
    structured_outputs=True,
    show_tool_calls=True,
)

# ---- REQUIREMENTS GATHERING TEAM ----
requirements_gathering_team = Agent(
    name="Requirements Gathering Team",
    team=[product_owner_writer, game_designer_requirements, user_focus_group_requirements, ux_designer],
    instructions=[
        "Define detailed feature requirements based on the sprint milestone and project goals.",
        "Ensure that all requirements consider user experience, engagement, and feasibility of implementation.",
        "Game-specific requirements must include mechanics, progression, and narrative interaction details.",
        "User insights should be incorporated to refine and improve the requirement specifications.",
    ],
    model=llm,
    reasoning=True,
    markdown=True,
    structured_outputs=True,
    show_tool_calls=True,
)

# ---- DEVELOPMENT TEAM ----
development_team = Agent(
    name="Development Team",
    team=[ink_script_developer, game_designer_code_advisor, background_artist],
    instructions=[
        "Develop deliverables based on the approved requirements, ensuring alignment with project vision.",
        "Ink Script Developer must create well-structured, interactive scripts that match design specifications.",
        "Game Designer Code Advisor should provide structured guidance to ensure gameplay mechanics function correctly.",
        "Background Artist should create environment visuals that match the tone and aesthetic of the game.",
        "Ensure assets are created in a modular way to allow for iteration and expansion.",
    ],
    model=llm,
    reasoning=True,
    markdown=True,
    structured_outputs=True,
    show_tool_calls=True,
)

# ---- QUALITY ASSURANCE TEAM ----
quality_assurance_team = Agent(
    name="Quality Assurance Team",
    team=[software_tester, game_tester],
    instructions=[
        "Thoroughly test all deliverables to ensure functionality, quality, and adherence to requirements.",
        "Software Tester must check for logic errors, syntax issues, and unintended narrative breaks in the Ink script.",
        "Game Tester should playtest deliverables, providing feedback on pacing, interaction design, and engagement.",
        "Document all identified issues and ensure reports provide clear feedback for iterative improvements.",
    ],
    model=llm,
    reasoning=True,
    markdown=True,
    structured_outputs=True,
    show_tool_calls=True,
)

# ---- ACCEPTANCE TESTING TEAM ----
acceptance_testing_team = Agent(
    name="Acceptance Testing Team",
    team=[product_owner_evaluator, user_focus_group_evaluator],
    instructions=[
        "Evaluate whether deliverables meet requirements and align with the intended project vision.",
        "Product Owner Evaluator should compare deliverables against written specifications and identify discrepancies.",
        "User Focus Group Evaluator should assess usability, player engagement, and narrative coherence.",
        "Provide detailed feedback on improvements before final acceptance of the deliverables.",
    ],
    model=llm,
    reasoning=True,
    markdown=True,
    structured_outputs=True,
    show_tool_calls=True,
)

if __name__ == "__main__":
    teams = {
        "project_planning": project_planning_team,
        "requirements_gathering": requirements_gathering_team,
        "development": development_team,
        "quality_assurance": quality_assurance_team,
        "acceptance_testing": acceptance_testing_team,
    }

    orchestrator = Orchestrator(teams=teams)

    print("\n🚀 Starting production run for Orchestrator...\n")

    result = orchestrator.run_project(user_input)

    print("\n✅ Run complete. Final result:")
    print(result)
