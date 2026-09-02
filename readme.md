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

The `build.py` does a few things to get ready to run the suite of test cases. It reads in all the test cases packed into csv files, creates files containing the plans to test, and commands to test those files. Finally, it generates a shell script which runs each test generated, and reports whether each plan in the test suite was verified by the tool. 

Each test is given a name, based on its parameters from its CSV entry. A test is uniquely identified by its `problem` (with the `.txt` removed), `goal` (cast to an integer), and `solution_index` entries. Thus, for the purposes of this tool, each test receives the name `{problem}_{goal}_{solution_index}`

## `build.py` parameters

There are a couple parameters that you can easily modify within the `build.py` file. Most of them are folder/file locations. You do not need to modify these for the program to run successfully.

- `OUTPUT_PROGRAM` - The name (and location) of the shell file to be generated
- `CSV_DIR` - The directory containing all the csv files describing tests
- `PLANS_DIR` - The directory where generated plans will be placed
- `DOMAINS_DIR` - The directory where domain txt files can be found
- `OUTPUT_DIR` - The directory where tool output will be placed
- `NODE_LIMIT` - The node limit for each search. See documentation of verification tool for more details on this limit.
- `JAR` - The path of the jar of the verification tool

# Running the Tests

Running `build.py` will output a shell file (default name `run_tests.sh`). This shell file will run each generated test and then print one of two things.