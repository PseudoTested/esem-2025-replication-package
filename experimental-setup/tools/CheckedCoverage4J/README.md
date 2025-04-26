# ☑️ CheckedCoverage4J

This project calculates checked coverage for Java projects up to Java 9. The
tool uses Slicer4J to calculate dynamic slices from each assertion in
the tool. 

## Table of Contents

1. [Setup](#setup)
2. [Running the tool](#running-the-tool)
3. [References](#references)

---
## Requirements

## Setup

To use this repo, first clone the project and `cd` into the directory:

```bash
git clone git@github.com:MgnMtn/checked-coverage.git
cd checked-coverage
```

On first use of the repo, you will need to run `setup.sh` to retrieve and build
the additional required resources. 

```bash
sh setup.sh
```
### Preparing project
As CheckedCoverage4J depends on [Slicer4J](https://github.com/resess/Slicer4J) for slicing, the user's project must be packaged into a single uber jar that includes the tests and test dependencies. 
The user is responsible for setting up their project for this, but some links to helpful resources are provided [here](resources/creating-an-uber-jar.md).

## Running the tool

To run the tool

```bash
sh run-checked-coverage.sh <project-name> <path-to-jar>
```
The `.jar` file will be re-packaged during the running process, but as each
project is different, the user needs to provide the relative path from this
directory. 


## References

- Khaled Ahmed, Mieszko Lis, and Julia Rubin. Slicer4J: A Dynamic Slicer for
  Java. The ACM Joint European Software Engineering Conference and Symposium on
  the Foundations of Software Engineering (ESEC/FSE), 2021.
- S. B. Hossain, M. B. Dwyer, S. Elbaum and A. Nguyen-Tuong, "Measuring and
  Mitigating Gaps in Structural Testing," 2023 IEEE/ACM 45th International
  Conference on Software Engineering (ICSE), 2023.


