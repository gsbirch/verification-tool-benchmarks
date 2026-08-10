import csv
from pathlib import Path

# This sets the sh file that is generated to run the tests
OUTPUT_PROGRAM = "run_tests.sh"
# The directory containing all the csv files describing tests
CSV_DIR = "csv"
# The directory where generated plans and solutions will be placed
PLANS_DIR = "plans"
# The directory where domain txt files can be found
DOMAINS_DIR = "domains"

folder = Path(CSV_DIR)

fileNames = [file.name for file in folder.glob("*.csv")]

search_to_m = { "astar": "bf" }
cost_to_c = { "temporal": "t" }

with open(OUTPUT_PROGRAM, "w") as out:
    out.write("#!/bin/bash\n")

    # generate tests for each csv file
    for fileName in fileNames:
        with open(f"csv/{fileName}", "r") as f:
            data = csv.DictReader(f)

            # generate one test for each row
            for row in data:
                # the file where the plan will be generated
                plan_file = f"{PLANS_DIR}/{row['problem'][:-4]}_{int(float(row['goal']))}_{row['solution_index']}.txt"
                # write the plan to a txt file
                with open(plan_file, "w") as plan:
                    str = row['author_signature'].replace(") ", ")\n")
                    plan.write(str)

                # the file where the solution will be generated
                solution_file = f"{PLANS_DIR}/{row['problem'][:-4]}_{int(float(row['goal']))}_{row['solution_index']}_SOLUTION.txt"
                # write the solution to a txt file
                with open(solution_file, "w") as plan:
                    str = row['plan'].replace(") |", ")\n")
                    plan.write(str)

                # the command to be ran
                output = f"java -jar sabre.jar -p {DOMAINS_DIR}/{row['problem']} -pl {plan_file} -g {row['goal']} -vl {10000} -atl {row['atl']} "
                output += f"-ctl {row['ctl'] + 1} -el {row['el'] + 1} -m {search_to_m[row['search']]} -c {cost_to_c[row['cost']]} -h {row['heuristic']}"
                print(output)

                out.write(f"if diff -q <({output}) {solution_file}> /dev/null; then\n")
                out.write(f"    echo \"Test {plan_file} Passed!\"\n")
                out.write(f"else\n")
                out.write(f"    echo \"Test {plan_file} Failed!\"\n")
                out.write(f"fi\n\n")

#if diff -q <(./my_program input1.txt) solution1.txt > /dev/null; then
#    echo "Test 1: Passed!"
#else
#    echo "Test 1: Failed!"
#fi
