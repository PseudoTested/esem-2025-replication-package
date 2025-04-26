# Project Setup

## Setting up projects for tools

### Commons-cli
#### CheckedCoverage4J
- Disable failing test - `TypeHandlerTest.testCreateDate:180`. Fails due to bug in java.util.Date: expected: <Thu Jan 01 01:00:00 GMT 1970> but was: <Thu Jan 01 02:00:00 GMT 1970>
- Comment out Jacoco minimum metric values in pom.xml (lines 99-106)

## Setting up projects for analysis

### Analysis Folder Structure

### Toggle project analysis
`project.csv`

