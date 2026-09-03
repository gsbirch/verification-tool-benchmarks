# Sabre Verification Tool Benchmarks

This tool contains some benchmarks for [Sabre Verification Tool](https://github.com/gsbirch/sabre-verification-tool). It works by reading csv files containing tests, then generating an executable shell program that runs each test. Each test contains an input plan and an expected solution. If the output from running the verification tool on an input plan with the given parameters matches the expected solution, a test passes. Otherwise, it fails.

# Usage

To run the already included tests is simple. First, compile the included version of the Sabre Verification Tool:
```
(cd sabre-verification-tool && mvn clean package)
```
Then generate the shell program by running the python file:
```
python build.py
```
Then allow execution and run the program:
```
chmod +x run_tests.sh
./run_tests.sh
```

Alternatively, do it all at once:
```
(cd sabre-verification-tool && mvn clean package)
python build.py
chmod +x run_tests.sh
./run_tests.sh
```

# Generating Tests

The `build.py` does a few things to get ready to run the suite of test cases. It reads in all the test cases which are packed into CSV files, creates new files containing the plans to test, and creates commands to test those files. Finally, it generates a shell script which runs each test generated, and reports whether each plan in the test suite was verified by the tool. It will also print out the java command necessary to run each tests if you wish to investigate one further.

Each test is given a name, based on its parameters from its CSV entry. A test is uniquely identified by its `problem` (with the `.txt` removed), `goal` (cast to an integer), and `solution_index` entries. Thus, for the purposes of this tool, each test receives the name `{problem}_{goal}_{solution_index}`

## `build.py` parameters

There are a couple parameters that you can easily modify within the `build.py` file. Most of them are folder/file locations. You do not need to modify these for the program to run successfully.

- `OUTPUT_PROGRAM` - The path of the shell file to be generated
- `CSV_DIR` - The directory containing all the csv files describing tests
- `PLANS_DIR` - The directory where generated plans will be placed
- `DOMAINS_DIR` - The directory where domain txt files can be found
- `OUTPUT_DIR` - The directory where tool output will be placed
- `NODE_LIMIT` - The node limit for each search. See documentation of verification tool for more details on this limit.
- `JAR` - The path of the jar of the verification tool

If they do not exist, the `OUTPUT_DIR` and `PLANS_DIR` directories will be generated automatically. Any other directories mentioned must exist before running `build.py`.

# Running the Tests

Running `build.py` will output a shell file (default name `run_tests.sh`). This shell file will run each generated test and then print the outcome of that test, whether or not the verification tool was able to generate an explanation for each action. The tests are also configured to print each solution to a file using the `-o` flag for the verification tool, with the path being `[OUTPUT_DIR]/[TEST_NAME]_OUT.txt`. See the verification tool documentation for more details.

# Adding Tests

It is possible to add new tests by simply adding CSV entries, with no modification necessary to `build.py`. First, if your test uses a domain not already included, it must be added to the `DOMAINS_DIR` folder (`domains/` by default). Then, you may add an entry with the following parameters to any existing CSV file, or may create a new one. By default, CSV files are organized by domain and desired utility value.

Each CSV entry must have the following entries:
- `domain` - The domain in which the plan exists.
- `problem` - The plain text file containing the domain. The path used to find the text file is the relative path `[DOMAINS_DIR]/[problem]`.
- `search` - The type of search desired for the tool (only `astar` is supported currently).
- `heuristic` - The heuristic desired for the tool.
- `goal` - A double represented the desired author utility.
- `atl` - The author temporal limit.
- `ctl` - The character temporal limit.
- `el` - The epistemic limit.
- `solution_index` - A number to uniquely identify this plan within all plans sharing the same domain and desired author utility value.
- `author_signature` - The plan to be tested. Actions must be on one line, separated by a space.
- `plan` - If you have an expected explanation, you may place it here, separating each action with spaces. Then `build.py` will print out this plan to a plain text file with the path `[PLANS_DIR]/[TEST_NAME]_SOLUTION.txt`. This is not used in benchmarking so it's okay to leave this blank.

Anytime you add or modify tests, you must rerun `build.py` to regenerate the tests.