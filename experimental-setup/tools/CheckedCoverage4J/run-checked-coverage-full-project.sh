#!/bin/bash

cd "$(dirname "$0")"

rm -r output/$PROJECT_NAME

TEST_CLASS_UNDER_TEST="<TEST_CLASS_PACKAGE>"


export JAVA_HOME=$JDK_17

PROJECT_NAME=$1
JAR_PATH=projects/$PROJECT_NAME/$2
mkdir projects/$PROJECT_NAME/logs/
mkdir -p output/$PROJECT_NAME

CC_HOME=$PWD
LOG_DIR=projects/$PROJECT_NAME/logs/
OUT_DIR=output/$PROJECT_NAME

rm -rf slicingCriteria.csv

echo
echo "---------------------------------------"
echo " Get slicing criterion -"
echo "---------------------------------------"

TEST_DIR=projects/$PROJECT_NAME/src/test/java/
TEST_CLASSES_DIR=projects/$PROJECT_NAME/target/test-classes/
DEPENDENCIES=projects/$PROJECT_NAME/target/dependency/

mvn -f projects/$PROJECT_NAME dependency:build-classpath -Dmdep.outputFile=cp.txt -Denforcer.skip=true test -Drat.skip=true -Dcheckstyle.skip
export CLASSPATH=$CLASSPATH:$(<projects/$PROJECT_NAME/cp.txt)

java -cp $CLASSPATH:$TEST_CLASSES_DIR/*:$DEPENDENCIES/* -jar resources/criteria-gen/build/libs/cc-criteria-gen-1.0-SNAPSHOT.jar $TEST_DIR $TEST_CLASSES_DIR > $LOG_DIR/assertion_generation_log


echo
echo "---------------------------------------"
echo " Create .jar file including tests"
echo "---------------------------------------"

sh ./scripts/create_jar_with_tests.sh $PROJECT_NAME > $LOG_DIR/create_jar_with_tests.log

echo
echo "---------------------------------------"
echo " Slice from assertion"
echo "---------------------------------------"

DEPENDENCIES=projects/$PROJECT_NAME/target/dependency/


while IFS="," read -r SLICING_CRITERION TEST_CLASS_NAME TEST_METHOD_NAME JUNIT_VERSION
do
   echo "$TEST_CLASS_UNDER_TEST vs $TEST_CLASS_NAME" 

   if [ "$TEST_CLASS_UNDER_TEST" = "$TEST_CLASS_NAME" ]; then
      echo $SLICING_CRITERION
      echo $TEST_CLASS_NAME
      echo $TEST_METHOD_NAME
      echo $JUNIT_VERSION

      python3 resources/Slicer4J/scripts/slicer4j.py -j $JAR_PATH -o $OUT_DIR/work -b $SLICING_CRITERION -tc $TEST_CLASS_NAME -tm $TEST_METHOD_NAME -dep $DEPENDENCIES -u $JUNIT_VERSION
      
      if [ -s $OUT_DIR/work/slice.log ]; then
         echo "criterion: $(cat $OUT_DIR/work/slice.log)" > $OUT_DIR/work/slice.log
         wait
         cat $OUT_DIR/work/slice.log >> $OUT_DIR/slice.txt
      fi

      wait
      rm -rf $OUT_DIR/work
   fi
done < slicingCriteria.csv
