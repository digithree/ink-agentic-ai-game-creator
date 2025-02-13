from orchestrator import Orchestrator  # Import the Orchestrator class
from utils import find_potential_reports
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

# Function to create test files if they don't exist
def setup_test_files():
    """Creates necessary test files for the test harness."""
    if os.path.exists(OUTPUT_FOLDER):
        shutil.rmtree(OUTPUT_FOLDER)  # Remove all files and subdirectories

    os.makedirs(OUTPUT_FOLDER)  # Recreate an empty test output folder

    with open(f"{OUTPUT_FOLDER}requirements.md", "w", encoding="utf-8") as f:
        f.write(f"Requirements")
    with open(f"{OUTPUT_FOLDER}game_design_doc.md", "w", encoding="utf-8") as f:
        f.write(f"Deliverable for game design")
    with open(f"{OUTPUT_FOLDER}game.ink", "w", encoding="utf-8") as f:
        f.write(f"Deliverable for game code")
    with open(f"{OUTPUT_FOLDER}background.png.txt", "w", encoding="utf-8") as f:
        f.write(f"Deliverable for background image")
    with open(f"{OUTPUT_FOLDER}qa_report.md", "w", encoding="utf-8") as f:
        f.write(f"QA report")
    with open(f"{OUTPUT_FOLDER}acceptance_report.md", "w", encoding="utf-8") as f:
        f.write(f"Acceptance report")

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
        find_potential_reports=find_potential_reports, # use real find potential reports, to test this
        evaluate_report=evaluate_report,
        output_folder=OUTPUT_FOLDER,
        use_agno_logger=False
    )

    print("\n🎬 Starting test run for Orchestrator...\n")
    result = orchestrator.run_project("Develop a text-based narrative game using Ink.")

    print("\n✅ Test run complete. Final result:")
    print(result)
