# Sabre Verification Tool Benchmarks

This tool contains some benchmarks for [Sabre Verification Tool](https://github.com/gsbirch/sabre-verification-tool). It works by reading csv files containing tests, then generating an executable shell program that runs each test. Each test contains an input plan and an expected solution. If the output from running the verification tool on an input plan with the given parameters matches the expected solution, a test passes. Otherwise, it fails.

# Building and Running the Tests

To run the already included tests is simple. First, you will need to place a compiled jar of the verification tool into the same directory as build.py. Then generate the shell program by running the python file:
```
python build.py
```
Then allow execution and run the program:
```
chmod +x run_tests.sh
./run_tests.sh
```

