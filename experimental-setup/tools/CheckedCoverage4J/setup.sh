#!/bin/bash

set -e

# Clean up 
rm -rf resources/DynamicSlicingCore
rm -rf resources/Slicer4J
rm -rf resources/criteria-gen
rm -rf resources/SingleJUnit5TestRunner
wait

# Java Version - point to JDK 1.8
export JDK_1_8=/Library/Java/JavaVirtualMachines/openlogic-openjdk-8.jdk/Contents/Home
export JAVA_HOME=$JDK_1_8

echo "#################################################################"
echo "Clone and install Resources"
# Clone Slicer4J and DyanmicSlicingCore
git clone git@github.com:resess/DynamicSlicingCore.git resources/DynamicSlicingCore
git clone git@github.com:resess/Slicer4J.git resources/Slicer4J
git clone git@github.com:MgnMtn/criteria-gen.git resources/criteria-gen
git clone git@github.com:MgnMtn/SingleJUnit5TestRunner.git resources/SingleJUnit5TestRunner


# Build Slicer4J and DynamicSlicingCore
mvn -f resources/DynamicSlicingCore/core -Dmaven.test.skip=true clean install 
mvn -f resources/Slicer4J/Slicer4J -Dmaven.test.skip=true clean install 

cd resources/criteria-gen
./gradlew clean build -x test
cd ../..

echo "#################################################################"
echo "Building JUnit4 Runner"

javac resources/Slicer4J/scripts/SingleJUnitTestRunner.java -cp "resources/Slicer4J/scripts/junit-4.8.2.jar"
jar -cf resources/Slicer4J/scripts/SingleJUnitTestRunner.jar -C resources/Slicer4J/scripts SingleJUnitTestRunner.class
rm resources/Slicer4J/scripts/SingleJUnitTestRunner.class

echo "#################################################################"
echo "Building JUnit5 Runner"
mvn -f resources/SingleJUnit5TestRunner -Dmaven.test.skip=true clean dependency:copy-dependencies install 

cp resources/slicer4j_custom.py resources/Slicer4J/scripts/slicer4j.py