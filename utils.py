from agno.utils.log import logger
from inklecate_permutation_play_tester import test_ink_playthrough, playthrough_data_report
import openai
import os
import re

def ink_files_log_stats(folder_path):
    """Return detailed stats on all .ink files in the given folder."""
    output = ""

    for file_name in os.listdir(folder_path):
        if file_name.endswith(".ink"):
            file_path = os.path.join(folder_path, file_name)
            output += f"--- {file_name}\n"
            output += playthrough_data_report(
                data=test_ink_playthrough(file_path),
                verbose=True
            ) + "\n"
            output += subprocess.run(
                ["inklecate", "-s", file_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                check=False
            ).strip() + "\n"

    return output

def extract_change_background_filenames(filename):
    """Extracts unique filenames from lines starting with '# changeBackground: ' in a given file."""
    filenames = set()  # Use a set to ensure uniqueness within a file
    with open(filename, 'r', encoding='utf-8') as file:
        for line in file:
            match = re.match(r"^# changeBackground:\s*(.+)", line)
            if match:
                filenames.add(match.group(1))  # Add to set to remove duplicates
    return filenames  # Return as a set

def ink_files_extract_change_background_filenames(folder_path):
    """Processes all .ink files in the given folder and returns a unique list of filenames."""
    all_filenames = set()  # Use a set to collect unique filenames across all files

    for file_name in os.listdir(folder_path):
        if file_name.endswith(".ink"):
            file_path = os.path.join(folder_path, file_name)
            all_filenames.update(extract_change_background_filenames(file_path))  # Merge unique filenames

    return list(all_filenames)  # Convert final set to a list


def get_folder_snapshot(path):
    """Returns a snapshot of the folder containing file names, their modification times, and sizes."""
    return {
        f: (os.path.getmtime(os.path.join(path, f)), os.path.getsize(os.path.join(path, f)))
        for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))
    }

def start_monitor_folder(path):
    """Takes an initial snapshot of the folder."""
    return get_folder_snapshot(path)

def stop_monitor_folder(path, initial_snapshot):
    """
    Compares the folder's current state with the initial snapshot.
    Returns True if:
    - Any files were added or removed.
    - Any files had their modification timestamp updated.
    - Any files changed in size.
    """
    current_snapshot = get_folder_snapshot(path)

    if current_snapshot != initial_snapshot:
        return True  # Changes detected

    return False  # No changes detected

# Example Usage
'''
folder_path = "test_output"

initial_snapshot = start_monitor_folder(folder_path)

# Simulate other work
time.sleep(2)  # Replace with actual work that might modify files

if stop_monitor_folder(folder_path, initial_snapshot):
    print("📂 Folder has changed! Running foo_bar()...")
    # foo_bar()  # Call your function here
else:
    print("✅ No changes detected.")
'''

def retry_until_success(task_func, success_check_func, max_retries, task_desc, log_func):
    """
    Executes a task function repeatedly until the success check function returns True 
    or the maximum retry count is reached.

    :param task_func: Function to execute.
    :param success_check_func: Function that returns True if the task succeeded.
    :param max_retries: Maximum number of attempts before failing.
    :param task_desc: A human readable description of the task.
    :param log_func: Logging function to use for messages.
    :raise Exception: If the task fails after the maximum number of retries.
    """
    for attempt in range(1, max_retries + 1):
        log_func(f"{'🔄 ' if attempt > 1 else ''}{task_desc}, attempt {attempt}/{max_retries}...")
        task_func()  # Execute the task
        if success_check_func():  # Check if it succeeded
            return
        log_func(f"⚠️ Failed attempt {attempt} for task {task_desc}. Retrying...")
    
    log_func(f"❌ Failed task: {task_desc}")
    raise Exception(f"Task failed after {max_retries} attempts.")  # Task ultimately failed

def retry_until_success_result(task_func, success_check_func, max_retries, task_desc, log_func, do_between_reties_func=None):
    """
    Executes a task function repeatedly until the success check function returns True 
    or the maximum retry count is reached.

    :param task_func: Function to execute.
    :param success_check_func: Function that returns True if the task succeeded.
    :param max_retries: Maximum number of attempts before failing.
    :param task_desc: A human readable description of the task.
    :param log_func: Logging function to use for messages.
    :raise Exception: If the task fails after the maximum number of retries.
    """
    for attempt in range(1, max_retries + 1):
        if attempt > 1 and do_between_reties_func:
            do_between_reties_func()
        log_func(f"{'🔄 ' if attempt > 1 else ''}{task_desc}, attempt {attempt}/{max_retries}...")
        result = task_func()  # Execute the task
        if success_check_func(result):  # Check if it succeeded
            return
        log_func(f"⚠️ Failed attempt {attempt} for task {task_desc}. Retrying...")
    
    log_func(f"❌ Failed task: {task_desc}")
    raise Exception(f"Task failed after {max_retries} attempts.")  # Task ultimately failed

def retry_until_folder_changes(task_func, folder_path, max_retries, task_desc, log_func):
    """
    Executes a task function repeatedly until changes are detected in a folder 
    or the maximum retry count is reached.

    :param task_func: Function to execute that is expected to modify the folder.
    :param folder_path: Path of the folder to monitor for changes.
    :param max_retries: Maximum number of attempts before failing.
    :param task_desc: A human readable description of the task.
    :param log_func: Logging function to use for messages.
    :return: True if successful, False if max retries were reached.
    """
    initial_snapshot = get_folder_snapshot(folder_path)

    def folder_has_changed():
        """Check if the folder has changed since the initial snapshot."""
        return stop_monitor_folder(folder_path, initial_snapshot)

    return retry_until_success(task_func, folder_has_changed, max_retries, task_desc, log_func)

# --- Ink ---

import subprocess

def get_ink_error_report(ink_file) -> str:
    """
    Runs an Ink script using inklecate to generate an error report.
    Returns the error report as a string.
    
    :param ink_file: The Ink script file to check.
    :return: The error report as a string, or an empty string if no errors are found.
    """
    if not os.path.exists(ink_file):
        logger.error(f"❌ Error, could not open ink file {ink_file}")
        return f"❌ Error, could not open ink file {ink_file}"
    try:
        result = subprocess.run(
            ["inklecate", ink_file],  # Runs inklecate without -p to check for errors
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,  # Capture both stdout and stderr
            text=True,  # Ensures output is returned as a string
            check=False  # Don't raise an exception even if inklecate exits with an error
        )

        report = result.stdout.strip()
        
        if report:
            logger.info(f"⚠️ Ink error report for '{ink_file}':\n{report}")
        else:
            logger.info(f"✅ No errors detected in '{ink_file}'.")

        return report  # Return error report as a string

    except Exception as e:
        logger.error(f"❌ Error running inklecate: {e}")
        return "❌ Error running inklecate."

def get_ink_playtest_report(ink_file) -> str:
    """
    Runs an Ink script using inklecate to playtest all possible story paths to search for errors.
    Returns the playtest report as a string, with a summary of path length and issues encountered.
    
    :param ink_file: The Ink script file to check.
    :return: The playtest report as a string.
    """
    if not os.path.exists(ink_file):
        logger.error(f"❌ Error, could not open ink file {ink_file}")
        return f"❌ Error, could not open ink file {ink_file}"
    try:
        result = test_ink_playthrough(ink_file, debug_log=False)

        report = playthrough_data_report(result, warnings_as_errors=False)
        
        if report.find("FAIL") != -1:
            logger.info(f"❌ Ink error report for '{ink_file}':\n{report}")
        else:
            logger.info(f"✅ No errors detected in '{ink_file}'.")

        return report  # Return error report as a string

    except Exception as e:
        logger.error(f"❌ Error running inklecate: {e}")
        return "❌ Error running inklecate."

# Example usage
'''
error_report = get_ink_error_report("my_script.ink")
if error_report:
    print("Errors found:\n", error_report)
else:
    print("No errors detected.")
'''

def get_ink_stats_report(ink_file) -> str:
    """
    Extracts statistics from an Ink script using inklecate, such as number of words, number of knots (labels),
    number of choices, etc.
    Returns the statistics as a string, with each stat on a new line.

    inklecate -s {ink_file} returns
    ```
    Words: 493
    Knots: 15
    Stitches: 0
    Functions: 0
    Choices: 10
    Gathers: 0
    Diverts: 21
    ```
    which we can extract the stats we care about and evaluate.
    
    :param ink_file: The Ink script file to extract stats from.
    :return: Ink script stats as a string.
    """
    if not os.path.exists(ink_file):
        logger.error(f"❌ Error, could not open ink file {ink_file}")
        return f"❌ Error, could not open ink file {ink_file}"
    try:
        result = subprocess.run(
            ["inklecate", "-s", ink_file],  # Runs inklecate with -s to extract stats
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,  # Capture both stdout and stderr
            text=True,  # Ensures output is returned as a string
            check=False  # Don't raise an exception even if inklecate exits with an error
        )

        stats = result.stdout.strip()
        output = f"⚠️ Could not extract Inks script stats for '{ink_file}'."
        
        if stats:
            words_match = re.search(r"Words:\s+(\d+)", stats)
            knots_match = re.search(r"Knots:\s+(\d+)", stats)
            word_count = int(words_match.group(1)) if words_match else None
            knot_count = int(knots_match.group(1)) if knots_match else None
            word_fail_msg = None
            knot_fail_msg = None
            if word_count < 500:
                word_fail_msg = f"Number of words {word_count} is below minimum of 500. REFACTOR CODE TO INCREASE WORD COUNT, EXPANDING THE NARRATIVE DETAIL!"
            if knot_count < 10:
                knot_fail_msg = f"Number of knots (labels) {knot_count} is below minimum of 10. REFACTOR CODE TO ADD MORE KNOTS (LABELS), I.E. TO ADD MORE CHOICE POINTS!"
            output = f"👀 Ink script features QA report for '{ink_file}':\n"
            if word_fail_msg or knot_fail_msg:
                output += "❌ FAIL " + "\n❌ FAIL ".join(msg for msg in [word_fail_msg, knot_fail_msg] if msg is not None)
            else:
                output += "✅ PASS"
        logger.info(output)
        return output

    except Exception as e:
        logger.error(f"❌ Error running inklecate: {e}")
        return "❌ Error running inklecate."

# --- General ---

def find_potential_reports(directory, report_type):
    """
    Lists files in a folder and identifies which ones are likely reports of the given type using an LLM.
    
    :param directory: The folder to search for potential reports.
    :param report_type: The type of report to filter for (e.g., "QA report", "User Acceptance Testing report").
    :return: A list of filenames that are likely reports of the specified type, or an empty list if none are found or an error occurs.
    """
    logger.info(f"ℹ️ Finding {report_type}s in `{directory}`.")
    if not os.path.exists(directory) or not os.path.isdir(directory):
        logger.error(f"❌ Error: Directory `{directory}` not found or is not a folder.")
        return []

    # Get the list of all files in the directory
    all_files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]

    if not all_files:
        logger.info(f"ℹ️ No files found in `{directory}`.")
        return []

    # Construct the AI prompt
    prompt = (
        f"You are an AI system that classifies files based on their filenames.\n"
        f"Given a list of filenames, determine which ones are most likely to be {report_type}s.\n"
        f"{report_type}s typically contain terms related to their purpose. Identify files that match the naming pattern.\n"
        "Return ONLY the filenames that match as a Python list, like this:\n"
        "['file1.md', 'file2.txt']\n\n"
        f"List of filenames:\n{all_files}\n\n"
        f"Filtered {report_type}s:"
    )

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "system", "content": prompt}],
            max_tokens=100,  # Allow enough space for multiple filenames
            temperature=0  # Ensures consistent, deterministic output
        )

        result = response["choices"][0]["message"]["content"].strip()

        # Validate that the response is a Python list
        try:
            report_files = eval(result)  # Safely parse the AI output
            if isinstance(report_files, list) and all(isinstance(f, str) for f in report_files):
                logger.info(f"📂 Identified {len(report_files)} potential {report_type}(s): {report_files}")
                return report_files
            else:
                logger.error(f"⚠️ Unexpected AI response format: {result}")
                return []
        except Exception as e:
            logger.error(f"⚠️ Error parsing AI response: {e}")
            return []

    except Exception as e:
        logger.error(f"❌ Error querying OpenAI API: {e}")
        return []

# Example Usage
# qa_reports = find_potential_reports("test_output", "QA report")
# logger.info(f"Likely QA Reports: {qa_reports}")

# uat_reports = find_potential_reports("test_output", "User Acceptance Testing report")
# logger.info(f"Likely UAT Reports: {uat_reports}")


def evaluate_report(report_file):
    """Reads a QA report file and determines whether the result is PASS or FAIL using OpenAI."""
    logger.info(f"ℹ️ Evaluating report in {report_file}.")
    
    if not os.path.exists(report_file):
        logger.error(f"❌ Error: report file `{report_file}` not found, failing by default.")
        return "FAIL"

    with open(report_file, "r", encoding="utf-8") as file:
        report_content = file.read()

    prompt = (
        "You are an AI system that strictly evaluates a assessment report.\n"
        "Read the following QA report and determine if the final outcome is PASS or FAIL.\n"
        "Respond with strictly either the word PASS or FAIL, and nothing else.\n\n"
        f"QA Report:\n{report_content}\n\n"
        "Final Evaluation:"
    )

    client = openai.OpenAI()

    # Make a chat completion request
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "system", "content": prompt}],
        max_tokens=5,  # Ensures only "PASS" or "FAIL" is returned
        temperature=0  # Ensures deterministic output
    )

    # Extract response text
    result = response.choices[0].message.content.strip()
    
    if result not in ["PASS", "FAIL"]:
        raise ValueError(f"Unexpected AI response: {result}")

    return result

# Example usage
# print(evaluate_qa_report("sprint_1_qa_report.md"))  # Should return either "PASS" or "FAIL"