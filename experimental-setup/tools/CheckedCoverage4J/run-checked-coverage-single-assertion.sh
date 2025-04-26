#!/bin/bash
set -e


PROJECT_NAME=$1
JAR_PATH=$2



mkdir -p projects/$PROJECT_NAME/logs/
mkdir -p output/$PROJECT_NAME

CC_HOME=$PWD
LOG_DIR=projects/$PROJECT_NAME/logs/
OUT_DIR=output/$PROJECT_NAME
rm -r $OUT_DIR
export JDK_1_8=/Library/Java/JavaVirtualMachines/openlogic-openjdk-8.jdk/Contents/Home
export JAVA_HOME=$JDK_1_8
echo
echo "---------------------------------------"
echo " Get slicing criterion"
echo "---------------------------------------"
SLICING_CRITERION=org.apache.commons.math3.fraction.FractionTest:346
TEST_CLASS_NAME=org.apache.commons.math3.fraction.FractionTest
TEST_METHOD_NAME=testAdd
JUNIT_VERSION=4
DEPENDENCIES=projects/commons-math/target/dependency

echo
echo "---------------------------------------"
echo " Create .jar file including tests"
echo "---------------------------------------"

# sh ./scripts/create_jar_with_tests.sh $PROJECT_NAME 

echo
echo "---------------------------------------"
echo " Slice from assertion"
echo "---------------------------------------"

python3 resources/Slicer4J/scripts/slicer4j.py -j $JAR_PATH -o $OUT_DIR/work -b $SLICING_CRITERION -tc $TEST_CLASS_NAME -tm $TEST_METHOD_NAME -dep $DEPENDENCIES -u $JUNIT_VERSION

if [ -s $OUT_DIR/work/slice.log ]; then
   echo "INFO: slice.log exists"
   echo -e "criterion: $(cat $OUT_DIR/work/slice.log)" > $OUT_DIR/work/slice.log
   wait
   cat $OUT_DIR/work/slice.log >> $OUT_DIR/slice.txt
fi

wait
# rm -rf $OUT_DIR/work
