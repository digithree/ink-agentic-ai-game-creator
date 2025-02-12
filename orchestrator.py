# ---- Project Orchestration Diagram ---

'''
📌 Project Planning Team  ➝  📌 Requirements Gathering Team  ➝  📌 Development Team  
                         ⬇️                                     ⬇️
         (Sprint restarts if needed)          (Redo if requirements are unclear)
                         ⬇️                                     ⬇️
🛠️ Quality Assurance Team  
  ➝ ✅ Pass ➝ 🛠️ Acceptance Testing Team ➝ ✅ Pass ➝ 📍 Plan Orchestrator ➝ (Next Sprint)
  ⬇️ ❌ Fail                                       ⬇️ ❌ Fail  
(Back to Development)                        (Back to Development)
'''

# ---- Project Orchestration Pseudo-code ----
'''
FUNCTION run_project(brief):
    sprints = project_planning_team.plan_sprints(brief)  # Plan all sprints using the directive from the CEO
    
    FOR sprint IN sprints:
        ATTEMPTS = 0
        WHILE ATTEMPTS < MAX_TASK_RETRY:
            RESULT = run_sprint(sprint)
            IF RESULT == "PASS":
                BREAK  # Move to next sprint
            ATTEMPTS += 1
        
        IF ATTEMPTS == MAX_TASK_RETRY:
            project_planning_team.report_failure(sprint)  # Generate failure report

    RETURN bundle(getArtifacts(), getReports())  # Collect all deliverables and reports

FUNCTION run_sprint(sprint):
    REQUIREMENTS = requirements_gathering_team.gather(sprint)
    DELIVERABLES = development_team.develop(REQUIREMENTS)
    
    ATTEMPTS = 0
    WHILE ATTEMPTS < MAX_TASK_RETRY:
        QA_REPORT = quality_assurance_team.test(DELIVERABLES, REQUIREMENTS)
        IF QA_REPORT.status == "FAIL":
            DELIVERABLES = development_team.revise(DELIVERABLES, QA_REPORT)
            ATTEMPTS += 1
            CONTINUE
        
        ACCEPTANCE_REPORT = acceptance_testing_team.evaluate(DELIVERABLES, REQUIREMENTS, sprint)
        IF ACCEPTANCE_REPORT.status == "FAIL":
            DELIVERABLES = development_team.revise(DELIVERABLES, ACCEPTANCE_REPORT)
            ATTEMPTS += 1
            CONTINUE
        
        RETURN "PASS"  # Both QA and Acceptance passed

    RETURN "FAIL"  # Max retries exceeded

'''

# Example team interaction trigger
'''
team_name.print_response(
    "Prompt for the specific task the team is assigned to do, in a high-level of detail, but no more than 50 words. List expected input documents it should look for on the file system.",
    # don't change the below
    stream=True,
    show_full_reasoning=True
)
'''

TEST_SPRINT_PLAN_CONTENT = """
```
# Sprint plan

## Sprint 1
- Implement core narrative logic
- Define branching choices

## Sprint 2
- Develop UI assets
- Playtest and iterate

## Sprint 3
- Polish and finalize release build
```
"""

from agno.utils.log import logger
import os
import shutil
import glob
import re

MAX_SPRINTS = 5

def exists_any_file_with_prefix(prefix, directory='.'):
    """Checks if any file in the given directory (or subdirectories) starts with the specified prefix."""
    search_pattern = os.path.join(directory, f"{prefix}*")  # Create a proper wildcard pattern
    return any(glob.glob(search_pattern, recursive=True))  # Check if any file matches

class Orchestrator:
    def __init__(self, teams, evaluate_report, output_folder="output/", max_task_retry=3, use_agno_logger=True):
        """Initialize the orchestrator with a dictionary of team agents."""
        self.teams = teams  # Dictionary: {"team_name": team_agent}
        self.evaluate_report = evaluate_report
        self.output_folder = output_folder
        self.max_task_retry = max_task_retry
        self.use_agno_logger = use_agno_logger
        self.sprint_plan_file = "sprint_plan.md"
    
    def log(self, message):
        if self.use_agno_logger:
            logger.info(message)
        else:
            print(message)

    def run_project(self, brief):
        attempts = 0
        while attempts < self.max_task_retry:
            if not os.path.exists(self.output_folder + self.sprint_plan_file):
                """Orchestrates the project execution based on the CEO's brief."""
                self.log(f"📌 Planning sprints based on the CEO's brief (Attempt {attempts + 1}/{self.max_task_retry})...\n")
                self.teams["project_planning"].print_response(
                    f"Break down the project based on the CEO's brief: {brief}. Define a list of sprints and their deliverables to a maximum of {MAX_SPRINTS} sprints. "
                    f"Use Markdown format with `# Sprint name` as headings ONLY. Save the result to `{self.sprint_plan_file}`. "
                    f"The plan should consist only of headings and bullet points, do not add extraneous details. "
                    f"Example plan file content, copy this format EXACTLY:\n{TEST_SPRINT_PLAN_CONTENT}",
                    stream=True,
                    show_full_reasoning=True
                )
            # Read the sprint plan file and extract sprint names
            sprints = self.parse_sprint_plan()
            if len(sprints) > 0:
                break  # Move to next sprint
            if os.path.exists(self.output_folder):
                shutil.rmtree(self.output_folder)  # Remove all files and subdirectories
                os.makedirs(self.output_folder)  # Recreate an empty test output folder
            attempts += 1
        
        if attempts == self.max_task_retry:
            self.log(f"❌ Failed after {self.max_task_retry} attempts to generate a sprint plan.\n")
            return {}

        for sprint in sprints:
            attempts = 0
            while attempts < self.max_task_retry:
                self.log(f"\n🚀 Running {sprint['title']} (Attempt {attempts + 1}/{self.max_task_retry})...\n")
                result = self.run_sprint(sprint)
                if result == "PASS":
                    break  # Move to next sprint
                logger.error(f"❌ {sprint['title']} runner has failed.\n")
                attempts += 1

            if attempts == self.max_task_retry:
                failure_report_file = f"{sprint['title']}_failure_report.md"
                self.log(f"❌ {sprint['title']} has failed after {self.max_task_retry} attempts. Generating failure report ({failure_report_file})...\n")
                self.teams["project_planning"].print_response(
                    f"Generate a project failure report for {sprint['title']}. Explain what went wrong and suggest potential improvements. "
                    f"Save the report to `{failure_report_file}`. ",
                    stream=True,
                    show_full_reasoning=True
                )

        return self.bundle(self.get_artifacts(), self.get_reports())

    def run_sprint(self, sprint):
        """Runs a single sprint, gathering requirements, developing deliverables, and ensuring quality assurance."""
        sprint_title = sprint["title"].split(":")[0]  # Take substring before ':' if it exists
        sprint_file_prefix = re.sub(r'[^a-zA-Z0-9_]', '', sprint_title.lower().replace(" ", "_"))
        deliverables_file_prefix = f"{sprint_file_prefix}_deliverables"

        attempts = 0
        while attempts < self.max_task_retry:
            requirements_file = f"{sprint_file_prefix}_requirements.md"
            self.log(f"📜 Gathering requirements for {sprint['title']} (Attempt {attempts + 1}/{self.max_task_retry})...\n")
            self.teams["requirements_gathering"].print_response(
                f"Define detailed feature requirements for {sprint['title']}. Ensure alignment with user expectations, technical feasibility, and project goals. "
                f"Make sure to capture the filenames of all deliverables, noting that the deliverables filename prefix should be {deliverables_file_prefix}. "
                f"Save the result to `{requirements_file}`. "
                f"Use the following details for the sprint: {sprint['details']} ",
                stream=True,
                show_full_reasoning=True
            )
            # check file was written, otherwise retry
            if os.path.exists(self.output_folder + requirements_file):
                break  # Move to next step
            logger.error(f"⚠️ No requirements file found for {sprint['title']}.")
            attempts += 1
        if attempts == self.max_task_retry:
            self.log(f"❌ Gathering requirements failed for {sprint['title']}.\n")
            return "FAIL"
        
        attempts = 0
        while attempts < self.max_task_retry:
            self.log(f"🛠️ Developing deliverables for {sprint['title']} (Attempt {attempts + 1}/{self.max_task_retry})...\n")
            self.teams["development"].print_response(
                f"Develop all deliverables for {sprint['title']}, including Ink scripts, game mechanics, and background assets. "
                f"Use requirement document `{requirements_file}` to ensure alignment. Save the result to file(s) prefixed with `{deliverables_file_prefix}`. ",
                stream=True,
                show_full_reasoning=True
            )
            if exists_any_file_with_prefix(deliverables_file_prefix, self.output_folder):
                break  # Move to next step
            logger.error(f"⚠️ No deliverables files found for {sprint['title']}.")
            attempts += 1
        if attempts == self.max_task_retry:
            self.log(f"❌ Development failed for {sprint['title']}.\n")
            return "FAIL"

        attempts = 0
        while attempts < self.max_task_retry:
            qa_report_file = f"{sprint_file_prefix}_qa_report.md"
            inner_attempts = 0
            while inner_attempts < self.max_task_retry:
                self.log(f"🔍 Performing quality assurance for {sprint['title']} (Attempt {inner_attempts + 1}/{self.max_task_retry})...\n")
                self.teams["quality_assurance"].print_response(
                    f"Test all deliverables for {sprint['title']}. Identify any functional issues, narrative inconsistencies, or usability problems. "
                    f"Use the requirement document `{requirements_file}` and deliverables file(s) prefixed with `{deliverables_file_prefix}` for reference. "
                    f"Generate a QA report and save it to `{qa_report_file}`. ",
                    stream=True,
                    show_full_reasoning=True
                )
                if os.path.exists(self.output_folder + qa_report_file):
                    break
                logger.error(f"⚠️ No QA report file found for {sprint['title']}.")
                inner_attempts += 1
            if inner_attempts == self.max_task_retry:
                self.log(f"❌ Quality Assurance report writing failed for {sprint['title']}.\n")
                return "FAIL"

            qa_status = self.evaluate_report(self.output_folder + qa_report_file)
            if qa_status == "FAIL":
                self.log(f"❌ QA failed for {sprint['title']}. Revising deliverables...\n")
                self.teams["development"].print_response(
                    f"Revise the deliverables based on the QA report for {sprint['title']}. Address the identified issues and re-submit. "
                    f"Use requirement document `{requirements_file}` to ensure alignment. Save the result to file(s) prefixed with `{deliverables_file_prefix}`. ",
                    stream=True,
                    show_full_reasoning=True
                )
                attempts += 1
                continue

            self.log(f"✅ Quality Assurance Passed for {sprint['title']}. Proceeding to Acceptance Testing...\n")

            acceptance_report_file = f"{sprint_file_prefix}_acceptance_report.md"
            inner_attempts = 0
            while inner_attempts < self.max_task_retry:
                self.log(f"🧪 Performing Acceptance Testing for {sprint['title']} (Attempt {inner_attempts + 1}/{self.max_task_retry})...\n")
                self.teams["acceptance_testing"].print_response(
                    f"Evaluate deliverables for {sprint['title']}. Ensure they meet user expectations, match project goals, and function correctly in the overall system. "
                    f"Use the requirement document `{requirements_file}` and deliverables file(s) prefixed with `{deliverables_file_prefix}` for reference. "
                    f"Save the report to `{acceptance_report_file}`. ",
                    stream=True,
                    show_full_reasoning=True
                )
                if os.path.exists(self.output_folder + acceptance_report_file):
                    break
                logger.error(f"⚠️ No Acceptance Testing report file found for {sprint['title']}.")
                inner_attempts += 1
            if inner_attempts == self.max_task_retry:
                self.log(f"❌ Acceptance Testing report writing failed for {sprint['title']}.\n")
                return "FAIL"

            acceptance_status = self.evaluate_report(self.output_folder + acceptance_report_file)
            if acceptance_status == "FAIL":
                self.log(f"❌ Acceptance Testing failed for {sprint['title']}. Revising deliverables...\n")
                self.teams["development"].print_response(
                    f"Revise the deliverables based on the acceptance test report for {sprint['title']}. Address the identified issues and re-submit. "
                    f"Use requirement document `{requirements_file}` to ensure alignment. Save the result to file(s) prefixed with `{deliverables_file_prefix}`. ",
                    stream=True,
                    show_full_reasoning=True
                )
                attempts += 1
                continue

            self.log(f"✅ Acceptance Testing Passed for {sprint['title']}. Sprint is completed.\n")

            return "PASS"  # Both QA and Acceptance passed

        return "FAIL"  # Max retries exceeded

    def parse_sprint_plan(self):
        """Reads the sprint plan file and extracts sprint names along with their details, accommodating H2 headings for sprints."""
        sprint_file_path = os.path.join(self.output_folder, self.sprint_plan_file)
        
        if not os.path.exists(sprint_file_path):
            self.log(f"❌ Error: Sprint plan file `{self.sprint_plan_file}` not found.")
            return []

        sprints = []
        current_sprint = None
        sprint_details = []
        is_first_heading = True  # Tracks if we've encountered the first H1 heading

        with open(sprint_file_path, "r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()

                # Ignore the first H1 heading (assumed to be "# Sprint plan")
                if is_first_heading and line.startswith("# "):
                    is_first_heading = False  # Mark that we've processed the first heading
                    continue

                # Identify new sprints from H2 headings (## Sprint Name)
                if line.startswith("## "):  
                    if current_sprint:  # Save the previous sprint before starting a new one
                        sprints.append({"title": current_sprint, "details": sprint_details})

                    current_sprint = line.strip("# ").strip()  # Extract sprint name
                    sprint_details = []  # Reset details for new sprint
                
                elif current_sprint and line:  # Collect details under current sprint
                    sprint_details.append(line)

        # Add the last sprint if it exists
        if current_sprint:
            sprints.append({"title": current_sprint, "details": sprint_details})

        self.log(f"📋 Extracted {len(sprints)} sprints from `{self.sprint_plan_file}`: {sprints}")
        return sprints



    def get_artifacts(self):
        """Placeholder function to return final deliverables."""
        # TODO : implement
        return "Final deliverables"

    def get_reports(self):
        """Placeholder function to return final reports."""
        # TODO : implement
        return "Final reports"

    def bundle(self, artifacts, reports):
        """Combines artifacts and reports for project completion."""
        return {"artifacts": artifacts, "reports": reports}

# TODO : use this
'''
def verify_output_files(output_dir, num_scenes):
    required_files = ["design_doc.md"] + [f"scene_{i}.md" for i in range(1, num_scenes + 1)] + [f"scene_{i}.ink" for i in range(1, num_scenes + 1)]
    for file in required_files:
        if not (output_dir / file).exists():
            return False
    return True

def create_narrative_game():
    try:
        reasoning_agent.print_response(f"Create a narrative game, to the following spec: {user_input}", stream=True, show_full_reasoning=True)
        return True
    except Exception as e:
        print(f"An error occurred: {e}")
        return False
    
MAX_ATTEMPTS = 5
attempt_count = 0

# verify output path has the following files:
while not verify_output_files(output_dir, num_scenes):
    print("Attempting to create game")
    if attempt_count >= MAX_ATTEMPTS:
        print("Max attempts reached. Exiting.")
        break
    attempt_count += 1
    if not create_narrative_game():
        print("Create game crashed")
    # Clear the output directory and retry until all files are present
    for file in output_dir.iterdir():
        if file.is_file():
            file.unlink()
'''
