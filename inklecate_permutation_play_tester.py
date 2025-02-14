import subprocess
import hashlib

def test_ink_playthrough(ink_file, debug_log=False):
    """
    Runs the Ink script multiple times to explore all complete paths (ending in `-> END`).
    
    :param ink_file: The Ink script file to play.
    :return: A list of fully explored, completed story paths.
    """
    visited_paths = set()  # Track explored paths to avoid redundancy
    queue = [((), set())]  # Each entry is (path, hashes_seen)
    complete_paths = []  # Store only fully completed paths
    inf_paths = []

    while queue:
        path, path_hashes = queue.pop(0)  # Get the next unexplored path and its choice hashes

        if debug_log:
            print(f"\n🚀 Exploring new path: {path}")

        result = explore_story(ink_file, path, debug_log)  # Run Ink script with current path

        if not result:
            if debug_log:
                print("⚠️ No valid result, skipping...")
            continue  # Skip invalid runs

        final_path, next_choices, is_complete, choice_hash, issues = result  # Extract path data

        # ✅ Detect Infinite Loop by Checking for Repeated Hashes in the Path
        if choice_hash in path_hashes:
            if debug_log:
                print(f"⚠️ Infinite loop detected at {final_path}, stopping exploration.")
            #issues['warnings'] += 1
            inf_paths.append((final_path, issues))
            continue  # Stop exploring this path

        # ✅ Track choice hash for this path
        new_path_hashes = path_hashes | {choice_hash}  # Create a new set with the updated hash

        if final_path not in visited_paths:
            visited_paths.add(final_path)

            if is_complete:
                complete_paths.append((final_path, issues))  # Store only full completions
                if debug_log:
                    print(f"✅ Story fully completed at path: {final_path}")
            elif debug_log:
                print(f"🔄 Path not complete, exploring further: {final_path}")

            for choice in next_choices:
                new_path = final_path + (choice,)
                if new_path not in visited_paths:
                    queue.append((new_path, new_path_hashes))  # Track hashes along with path

    if debug_log:
        print("\n✅ All complete paths explored!\n")
    return (complete_paths, inf_paths)


def count_issues(output_log):
    return { "warnings": output_log.count("WARNING"), "errors": output_log.count("ERROR") }

def explore_story(ink_file, path, debug_log=False):
    """
    Runs inklecate in interactive mode (-p) and follows a given choice path.
    
    :param ink_file: The Ink script file to play.
    :param path: A tuple of choices that define the path to follow.
    :return: The final path, available choices at last step, and a completion flag.
    """
    try:
        if debug_log:
            print(f"\n🎭 Running story with path: {path}")

        # Start inklecate in interactive mode
        process = subprocess.Popen(
            ["inklecate", "-p", ink_file], 
            stdin=subprocess.PIPE, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=0
        )

        output_log = []  # Store full game output
        buffer = ""  # Temporary buffer for incoming output

        # Follow given path
        for choice in path:
            while True:
                char = process.stdout.read(1)  # Read one character at a time
                if not char:
                    break  # No more output
                
                buffer += char
                if debug_log:
                    print(char, end="", flush=True)  # Stream output
                if buffer.endswith("?> "):  # Detect input prompt
                    break  # Stop reading at prompt

            # Check if inklecate has exited before we send input
            if process.poll() is not None:
                if debug_log:
                    print("✅ Story reached a natural ending.")
                return path, [], True, -1, count_issues(buffer)  # Mark as complete

            if debug_log:
                print(f"📝 Sending predefined choice: {choice}")
            try:
                process.stdin.write(f"{choice}\n")
                process.stdin.flush()
                #time.sleep(0.5)  # Let Ink process input
            except BrokenPipeError:
                if debug_log:
                    print("✅ inklecate exited naturally. Story complete.")
                return path, [], True, -1, count_issues(buffer)  # Mark as complete

        # Read until next input prompt
        while True:
            char = process.stdout.read(1)
            if not char:
                if debug_log:
                    print("✅ inklecate exited naturally. Story complete.")
                return path, [], True, -1, count_issues(buffer)  # Mark as complete
            buffer += char
            if debug_log:
                print(char, end="", flush=True)
            if buffer.endswith("?> "):
                break

        # Extract remaining choices
        output_log.append(buffer.strip())
        choice_start_index = buffer.rfind("1:")  # Find the last occurrence of "1:"
        choice_parse_text = buffer[choice_start_index:] if choice_start_index != -1 else ""
        choice_hash = hashlib.md5(choice_parse_text.encode()).hexdigest()
        if debug_log:
            print("#️⃣ choice hash: " + str(choice_hash))
        choices = [line.split(":")[0].strip() for line in choice_parse_text.split("\n") if line.strip().startswith(tuple(str(i) + ":" for i in range(1, 10)))]

        process.terminate()  # Stop Ink process

        return path, choices, False, choice_hash, count_issues(buffer)  # Mark as incomplete

    except BrokenPipeError:
        if debug_log:
            print("✅ inklecate exited naturally. Story complete.")
        return path, [], True, -1, count_issues(buffer)  # Mark as complete
    except Exception as e:
        if debug_log:
            print(f"❌ Unexpected error running inklecate: {e}")
        return None

def issues_to_str(issues):
    if issues['warnings'] == 0 and issues['errors'] == 0:
        return "No issues"
    return f"Warnings: {issues['warnings']}, Errors: {issues['errors']}"

def playthrough_data_report(data, min_path_length=5, warnings_as_errors=False, inf_loops_as_errors=False, verbose=False):
    completed_path_data, inf_path_data = data
    verbose_output = ""
    default_output = ""
    acceptance = "✅ PASS, no syntax errors or warnings"
    path_length = "✅ Number of choices is enough to PASS"
    max_path_length = 0
    default_output += f"➡️  Possible Story Paths Permutations: {len(completed_path_data)}\n"
    count_paths_with_warnings = 0
    count_paths_with_errors = 0
    if len(completed_path_data) > 0:
        verbose_output += "➡️  Possible Story Paths:\n"
        for idx, path_data in enumerate(completed_path_data):
            path, issues = path_data
            if issues['errors'] > 0:
                acceptance = "❌ FAIL: CRITICAL ISSUES WITH INK SCRIPT, MUST FIX BUGS IMMEDIATELY"
                count_paths_with_errors += 1
            if issues['warnings'] > 0:
                count_paths_with_warnings += 1
                if warnings_as_errors:
                    acceptance = "❌ FAIL: CRITICAL ISSUES WITH INK SCRIPT, MUST FIX BUGS IMMEDIATELY"
            if len(path) > max_path_length:
                max_path_length = len(path)
            verbose_output += f"{idx + 1}. {list([int(choice) for choice in path])}, {issues_to_str(issues)}\n"
    else:
        verbose_output += "❌ FAIL: CRITICAL ISSUE, no story paths can be completed successful!\n"
        default_output += "❌ FAIL: CRITICAL ISSUE, no story paths can be completed successful!\n"
    if len(inf_path_data) > 0:
        if inf_loops_as_errors:
            verbose_output += "⚠️ Infinite Loop Story Paths:\n"
            default_output += f"⚠️ Infinite Loop Story Paths: {len(inf_path_data)}\n"
        else:
            verbose_output += "🔃 Infinite Loop Story Paths:\n"
            default_output += f"🔃 Infinite Loop Story Paths: {len(inf_path_data)}\n"
        for idx, path_data in enumerate(inf_path_data):
            path, issues = path_data
            if issues['errors'] > 0:
                count_paths_with_errors += 1
                acceptance = "❌ FAIL: CRITICAL ISSUES WITH INK SCRIPT, MUST FIX BUGS IMMEDIATELY"
            if issues['warnings'] > 0:
                count_paths_with_warnings += 1
                if warnings_as_errors:
                    acceptance = "❌ FAIL: CRITICAL ISSUES WITH INK SCRIPT, MUST FIX BUGS IMMEDIATELY"
            verbose_output += f"{idx + 1}. {list([int(choice) for choice in path])}, {issues_to_str(issues)}\n"
        if inf_loops_as_errors:
            verbose_output += "❌ FAIL: CRITICAL ISSUE, infinite loops are possible!\n"
            default_output += "❌ FAIL: CRITICAL ISSUE, infinite loops are possible!\n"
    if max_path_length < min_path_length:
        default_output += f"❌ Max Story Choice Depth: {max_path_length}\n"
        if acceptance.startswith("✅"):
            acceptance = "❌ FAIL: CRITICAL ISSUES WITH INK SCRIPT, MUST FIX BUGS IMMEDIATELY"
        path_length = f"❌ FAIL: Max length of story choice path is NOT enough; is {str(max_path_length)} but should be at least {str(min_path_length)}.\nMore story choice depth should be added to the story, it is not long enough. THIS IS CONSIDERED A BUG."
    else:
        default_output += f"✅ Max Story Choice Depth: {max_path_length}\n"
    if count_paths_with_warnings > 0 or count_paths_with_errors > 0:
        default_output += f"{'ℹ️' if count_paths_with_errors == 0 else '❌'} Paths with ERRORS: {count_paths_with_errors}\n"
        default_output += f"{'ℹ️' if count_paths_with_warnings == 0 else '⚠️ '} Paths with WARNINGS: {count_paths_with_warnings}\n"
    return (verbose_output if verbose else default_output) + "\n" + acceptance + "\n" + path_length + "\n"

# Example Usage
'''
# has bugs, too short
#final_paths_data = test_ink_playthrough("output-example/interactive_narrative.ink", debug_log=True)

# has inf loops, too short
#final_paths_data = test_ink_playthrough("output-example/inf-loop-test.ink")

# has no bug, is correct length, but does have inf loops
final_paths_data = test_ink_playthrough("output-example/expanded_cafe_story.ink")

# print out the summary with bug report
print(playthrough_data_report(final_paths_data, verbose=True)) #inf_loops_as_errors=False
print("\n---------------------------------------\n")
print(playthrough_data_report(final_paths_data)) #inf_loops_as_errors=False
'''
