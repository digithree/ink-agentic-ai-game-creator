from orchestrator import Orchestrator  # Import the Orchestrator class
import os
import shutil

# Stub class to simulate AI agents by logging responses
class StubTeam:
    def __init__(self, name):
        self.name = name

    def print_response(self, prompt, stream=True, show_full_reasoning=True):
        """Logs the task being performed instead of calling AI."""
        print(f"[{self.name}] Task: {prompt}")

# Create stubbed teams
stubbed_teams = {
    "project_planning": StubTeam("Project Planning Team"),
    "requirements_gathering": StubTeam("Requirements Gathering Team"),
    "development": StubTeam("Development Team"),
    "quality_assurance": StubTeam("Quality Assurance Team"),
    "acceptance_testing": StubTeam("Acceptance Testing Team"),
}

# Pre-populated test file content
OUTPUT_FOLDER = "test_output/"
SPRINT_PLAN_FILE = "sprint_plan.md"
TEST_SPRINT_PLAN_CONTENT = """
# Sprint plan

## Sprint 1
- Implement core narrative logic
- Define branching choices

## Sprint 2
- Develop UI assets
- Playtest and iterate

## Sprint 3
- Polish and finalize release build
"""

# Function to create test files if they don't exist
def setup_test_files():
    """Creates necessary test files for the test harness."""
    if os.path.exists(OUTPUT_FOLDER):
        shutil.rmtree(OUTPUT_FOLDER)  # Remove all files and subdirectories

    os.makedirs(OUTPUT_FOLDER)  # Recreate an empty test output folder

    if not os.path.exists(f"{OUTPUT_FOLDER}{SPRINT_PLAN_FILE}"):
        with open(f"{OUTPUT_FOLDER}{SPRINT_PLAN_FILE}", "w", encoding="utf-8") as f:
            f.write(TEST_SPRINT_PLAN_CONTENT)

    for sprint in ["Sprint 1", "Sprint 2", "Sprint 3"]:
        sprint_file_prefix = sprint.lower().replace(" ", "_")
        with open(f"{OUTPUT_FOLDER}{sprint_file_prefix}_requirements.md", "w", encoding="utf-8") as f:
            f.write(f"Requirements for {sprint}")
        with open(f"{OUTPUT_FOLDER}{sprint_file_prefix}_deliverables.md", "w", encoding="utf-8") as f:
            f.write(f"Deliverables for {sprint}")
        with open(f"{OUTPUT_FOLDER}{sprint_file_prefix}_qa_report.md", "w", encoding="utf-8") as f:
            f.write(f"QA report for {sprint}")
        with open(f"{OUTPUT_FOLDER}{sprint_file_prefix}_acceptance_report.md", "w", encoding="utf-8") as f:
            f.write(f"Acceptance report for {sprint}")

def evaluate_report(report_file):
    """Stub function to simulate report evaluation for testing, prints the length of the file."""
    
    if not os.path.exists(report_file):
        print(f"[TEST HARNESS] ❌ Error: report file `{report_file}` not found.")
        return "PASS"  # Default to PASS if file is missing to keep test running
    
    with open(report_file, "r", encoding="utf-8") as file:
        content = file.read()
    
    print(f"[TEST HARNESS] Evaluating report: {report_file} (Length: {len(content)} characters)")
    
    return "PASS"  # Always return "PASS" for test harness consistency


# Run the test harness
if __name__ == "__main__":
    setup_test_files()  # Ensure test files exist
    
    # Initialize Orchestrator with stubbed teams
    orchestrator = Orchestrator(
        teams=stubbed_teams,
        evaluate_report=evaluate_report,
        output_folder=OUTPUT_FOLDER,
        use_agno_logger=False
    )

    print("\n🎬 Starting test run for Orchestrator...\n")
    result = orchestrator.run_project("Develop a text-based narrative game using Ink.")

    print("\n✅ Test run complete. Final result:")
    print(result)
