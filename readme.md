# Sabre Verification Tool Benchmarks

This tool contains some benchmarks for [Sabre Verification Tool](https://github.com/gsbirch/sabre-verification-tool). It works by reading csv files containing tests, then generating an executable shell program that runs each test. Each test contains an input plan and an expected solution. If the output from running the verification tool on an input plan with the given parameters matches the expected solution, a test passes. Otherwise, it fails.

# Building and Running the Tests

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
