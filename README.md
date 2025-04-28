# Replication Package for "Where Tests Fall Short: Empirically Analyzing Oracle Gaps in Covered Code"

## Project Set

| Project                               | Git Hash                                 |
| ------------------------------------- | ---------------------------------------- |
| BlueObelisk / euclid                  | 3e2c1a351f670376e2aaa26813642c19da76dbcf |
| bvolpato / inutils4j                  | 8af0f143bfd4ef979892df314dec7858fa6e11af |
| decorators-squad / eo-yaml            | ad4f2bd1d9c8a14ab22b49f48bdd295c8cb13b3e |
| facebook / facebook-java-business-sdk | e6e76a07b5a03fd6fecffa0f81850786b42a31b0 |
| tabulapdf / tabula-java               | 5d91f1d733c4895d31854a641c152220f8c5f341 |
| tdebatty / java-string-similarity     | 93240df9aab3ecea98b869c9536aa7ebc555b281 |

## Data

### Project Data from Tool Execution 
`analysis/project_data` contains the execution data from each of the tools used to conduct this study.

### Negotiated Agreement Data
`analysis/negotiated-agreement-data` contains the agreed purposes of the statements in the oracle gaps reached through negotiated agreement.

## Tools

The following tools were used to evaluate the project set.

### CheckedCoverage4J
We created CheckedCoverage4J on top of the [Slicer4J](https://github.com/resess/Slicer4J) tool.
CheckedCoverage4J includes setup instructions and addtional JUnit5 test runner required alongside Slicer4J. 
Tool repo will be made public on acceptance.
Problems identified with the Slicer4J tool in the build process will be reported as issues to the project owners upon acceptance.

### PseudoSweep
PseudoSweep is available at [https://github.com/PseudoTested/PseudoSweep](https://github.com/PseudoTested/PseudoSweep).
To remove the decision instrumentation and analysis, we adjusted the code and example run script as found in `tools/PseudoSweep`. 
Problems identified with the tool will be reported as issues to the project owners upon acceptance. 

### PORBS
PORBS is currently available at [https://syed-islam.github.io/research/program-analysis/#observation-based-program-slicing-orbs](https://syed-islam.github.io/research/program-analysis/#observation-based-program-slicing-orbs).
Our configuration files are available in `tools/PORBS`.
Our script for collecting the deleted lines is under `scripts/get_deleted_lines.py`.

### PIT
PIT is currently available at [https://pitest.org/](https://pitest.org/)

### Criticality Score
We used the [OSSF's Criticality Score](https://github.com/ossf/criticality_score) to identify projects. 


## Executing tools on project set
To execute each tool on the projects, use the scripts in the `experimental-setup` directory. 
The zip file of the project under test must be added to `experimental-setup/projects`.
The tools will be executed on all classes in the args.csv files where `run-project_1.sh` will run all classes in the `args_1.csv` file and `run-project-mt.sh` will run all classes in the `args_mt.csv`.

## Analysing the results
The `analysis` directory contains the scripts and notebooks used to collate and analyze the data.
First, install requirements.txt and run `analysis/collate_class_info.py` to collate the tool output data in `project_data`.
Next, run each notebook in `notebooks` to analyze the data and produce plots used in paper.
