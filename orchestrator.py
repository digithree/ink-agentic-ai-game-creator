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

from agno.utils.log import logger
import os

class Orchestrator:
    def __init__(self, teams, output_folder="output/", max_task_retry=3, use_agno_logger=True):
        """Initialize the orchestrator with a dictionary of team agents."""
        self.teams = teams  # Dictionary: {"team_name": team_agent}
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
        """Orchestrates the project execution based on the CEO's brief."""
        self.log("📌 Planning sprints based on the CEO's brief...\n")
        self.teams["project_planning"].print_response(
            f"Break down the project based on the CEO's brief: {brief}. Define a list of sprints and their deliverables. "
            f"Use Markdown format with `# Sprint name` as headings. Save the result to `{self.sprint_plan_file}`.",
            stream=True,
            show_full_reasoning=True
        )

        # Read the sprint plan file and extract sprint names
        sprints = self.parse_sprint_plan()

        for sprint in sprints:
            attempts = 0
            while attempts < self.max_task_retry:
                self.log(f"\n🚀 Running {sprint} (Attempt {attempts + 1}/{self.max_task_retry})...\n")
                result = self.run_sprint(sprint)
                if result == "PASS":
                    break  # Move to next sprint
                attempts += 1

            if attempts == self.max_task_retry:
                failure_report_file = f"{sprint}_failure_report.md"
                self.log(f"❌ {sprint} has failed after {self.max_task_retry} attempts. Generating failure report ({failure_report_file})...\n")
                self.teams["project_planning"].print_response(
                    f"Generate a project failure report for {sprint}. Explain what went wrong and suggest potential improvements. "
                    f"Save the report to `{failure_report_file}`.",
                    stream=True,
                    show_full_reasoning=True
                )

        return self.bundle(self.get_artifacts(), self.get_reports())

    def run_sprint(self, sprint):
        """Runs a single sprint, gathering requirements, developing deliverables, and ensuring quality assurance."""

        requirements_file = f"{sprint}_requirements.md"
        self.log(f"📜 Gathering requirements for {sprint}...\n")
        self.teams["requirements_gathering"].print_response(
            f"Define detailed feature requirements for {sprint}. Ensure alignment with user expectations, technical feasibility, and project goals. "
            f"Save the result to `{requirements_file}`.",
            stream=True,
            show_full_reasoning=True
        )

        deliverables_file = f"{sprint}_deliverables.md"
        self.log(f"🛠️ Developing deliverables for {sprint}...\n")
        self.teams["development"].print_response(
            f"Develop all deliverables for {sprint}, including Ink scripts, game mechanics, and background assets. "
            f"Use requirement documents to ensure alignment. Save the result to `{deliverables_file}`.",
            stream=True,
            show_full_reasoning=True
        )

        attempts = 0
        while attempts < self.max_task_retry:
            qa_report_file = f"{sprint}_qa_report.md"
            self.log(f"🔍 Performing quality assurance for {sprint} (Attempt {attempts + 1}/{self.max_task_retry})...\n")
            self.teams["quality_assurance"].print_response(
                f"Test all deliverables for {sprint}. Identify any functional issues, narrative inconsistencies, or usability problems. "
                f"Generate a QA report and save it to `{qa_report_file}`.",
                stream=True,
                show_full_reasoning=True
            )

            qa_status = "PASS"  # Placeholder for real validation logic
            if qa_status == "FAIL":
                self.log(f"❌ QA failed for {sprint}. Revising deliverables...\n")
                self.teams["development"].print_response(
                    f"Revise the deliverables based on the QA report for {sprint}. Address the identified issues and re-submit. "
                    f"Save the revised deliverables to `{deliverables_file}`.",
                    stream=True,
                    show_full_reasoning=True
                )
                attempts += 1
                continue

            self.log(f"✅ Quality Assurance Passed for {sprint}. Proceeding to Acceptance Testing...\n")

            acceptance_report_file = f"{sprint}_acceptance_report.md"
            self.teams["acceptance_testing"].print_response(
                f"Evaluate deliverables for {sprint}. Ensure they meet user expectations, match project goals, and function correctly in the overall system. "
                f"Save the report to `{acceptance_report_file}`.",
                stream=True,
                show_full_reasoning=True
            )

            acceptance_status = "PASS"  # Placeholder for real validation logic
            if acceptance_status == "FAIL":
                self.log(f"❌ Acceptance Testing failed for {sprint}. Revising deliverables...\n")
                self.teams["development"].print_response(
                    f"Revise the deliverables based on the acceptance test report for {sprint}. Address the identified issues and re-submit. "
                    f"Save the revised deliverables to `{deliverables_file}`.",
                    stream=True,
                    show_full_reasoning=True
                )
                attempts += 1
                continue

            return "PASS"  # Both QA and Acceptance passed

        return "FAIL"  # Max retries exceeded

    def parse_sprint_plan(self):
        """Reads the sprint plan file and extracts sprint names based on `# Sprint name` headings."""
        if not os.path.exists(self.output_folder + self.sprint_plan_file):
            self.log(f"❌ Error: Sprint plan file `{self.sprint_plan_file}` not found.")
            return []

        sprints = []
        with open(self.output_folder + self.sprint_plan_file, "r", encoding="utf-8") as file:
            for line in file:
                if line.startswith("# "):  # Markdown heading for sprint name
                    sprint_name = line.strip("# ").strip()
                    sprints.append(sprint_name)

        self.log(f"📋 Extracted {len(sprints)} sprints from `{self.sprint_plan_file}`: {sprints}")
        return sprints

    def get_artifacts(self):
        """Placeholder function to return final deliverables."""
        return "Final deliverables"

    def get_reports(self):
        """Placeholder function to return final reports."""
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
