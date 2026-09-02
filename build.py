import csv
import os
from pathlib import Path

# This sets the sh file that is generated to run the tests
OUTPUT_PROGRAM = "run_tests.sh"
# The directory containing all the csv files describing tests
CSV_DIR = "csv"
# The directory where generated plans and solutions will be placed
PLANS_DIR = "plans"
# The directory where domain txt files can be found
DOMAINS_DIR = "domains"
# The directory where tool output will be placed
OUTPUT_DIR = "out"
# The node limit for each search
NODE_LIMIT = 10000
# The path of the jar of the verification tool
JAR = "verify.jar"

# The messages that print out when the tool succeeds/fails in finding an explanation
SUCCESS_MESSAGE = "This plan can be explained by Sabre within the given constraints"
FAIL_MESSAGE = "This plan can not be explained by Sabre within the given constraints"

# generate the two needed folders if they don't exist
os.makedirs("out", exist_ok=True)
os.makedirs("plans", exist_ok=True)

csv_folder = Path(CSV_DIR)

fileNames = [file.name for file in csv_folder.glob("*.csv")]

# dictionaries for the different types of searches performed
# right now this is just astar search w/ temporal cost
search_to_m = { "astar": "bf" }
cost_to_c = { "temporal": "t" }

with open(OUTPUT_PROGRAM, "w") as out:
    out.write("#!/bin/bash\n")
    out.write("failures=0\n")

    # generate tests for each csv file
    for fileName in fileNames:
        with open(f"csv/{fileName}", "r") as f:
            data = csv.DictReader(f)

            # generate one test for each row
            for row in data:
                # the file where the plan will be generated
                test_name = f"{row['problem'][:-4]}_{int(float(row['goal']))}_{row['solution_index']}"
                plan_file = f"{PLANS_DIR}/{test_name}_PLAN.txt"
                # write the plan to a txt file
                with open(plan_file, "w") as plan:
                    str = row['author_signature'].replace(") ", ")\n")
                    plan.write(str)

                # the file where the solution will be generated
                solution_file = f"{PLANS_DIR}/{test_name}_SOLUTION.txt"
                # write the solution to a txt file
                with open(solution_file, "w") as plan:
                    str = row['plan'].replace(") |", ")\n")
                    plan.write(str)

                out_file = f"{OUTPUT_DIR}/{test_name}_OUT.txt"

                # the command to be ran
                command = f"java -jar {JAR} -p {DOMAINS_DIR}/{row['problem']} -pl {plan_file} -g {row['goal']} -vl {NODE_LIMIT} -atl {row['atl']} "
                command += f"-ctl {row['ctl']} -el {row['el']} -m {search_to_m[row['search']]} -c {cost_to_c[row['cost']]} -h {row['heuristic']} -o {out_file}"
                print(command)

                # store output in a variable, the solution will get written to a file
                out.write(f"output=$({command})\n")
                # get the last line of the output
                out.write(f"last_line=$(printf '%s\n' \"$output\" | tail -n 1)\n")
                # if it is a valid solution, the test passes
                out.write(f"if [[ \"$last_line\" == \"{SUCCESS_MESSAGE}\" ]]; then\n")
                out.write(f"    echo \"Test {test_name} explained!\"\n")
                # if it is not a valid solution, the test fails
                out.write(f"elif [[ \"$last_line\" == \"{FAIL_MESSAGE}\" ]]; then\n")
                out.write(f"    echo \"! - Test {test_name} not explained within these constraints!\"\n")
                out.write(f"    ((failures++))\n")
                out.write(f"else\n")
                out.write(f"    echo \"FAIL: unexpected last line: $last_line\"\n")
                out.write(f"fi\n\n")

    # at the end, the program will report how many tests were not explained
    out.write(f"echo \"Tests not explained: $failures\"")