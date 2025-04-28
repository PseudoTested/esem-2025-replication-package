#!/bin/bash

# set -e

#################################################
# Env
#################################################
JAVA_HOME=$JDK_17

#################################################
# Inputs
#################################################

CWD=$PWD

echo $CWD


# Loop through each line
while IFS=',' read -r PROJECT_NAME TEST_CLASS_PACKAGE SRC_FILE TEST_NAME TEST_CLASS_CLASS JAR_PATH ; do

    ZIP_NAME="${PROJECT_NAME%_*}".zip
    PROJECT_PATH=$CWD/projects/$ZIP_NAME
    echo $ZIP_NAME


    # logs
    if [ -d logs/$PROJECT_NAME ] ; then
        rm -rf logs/$PROJECT_NAME
    fi
    mkdir logs/$PROJECT_NAME

    # results
    if [ -d results/$PROJECT_NAME ] ; then
        rm -rf results/$PROJECT_NAME
    fi
    mkdir results/$PROJECT_NAME


    if [ -d tools_$PROJECT_NAME ] ; then
        rm -rf tools_$PROJECT_NAME
    fi
    cp -r tools/ tools_$PROJECT_NAME/
    # sed variable names
    sed -i '' 's+<TEST_CLASS_PACKAGE>+'"${TEST_CLASS_PACKAGE}"'+g' tools_$PROJECT_NAME/CheckedCoverage4J/run-checked-coverage-full-project.sh
    sed -i '' 's+<SRC_FILE>+'"${SRC_FILE}"'+g' tools_$PROJECT_NAME/PORBS/config/OrbsFramework.properties
    sed -i '' 's+<SRC_FILE>+'"${SRC_FILE}"'+g' tools_$PROJECT_NAME/PORBS/dist/orbs.sh
    sed -i '' 's+<SRC_FILE>+'"${SRC_FILE}"'+g' tools_$PROJECT_NAME/PseudoSweep/run-pseudosweep.sh
    sed -i '' 's+<TEST_CLASS_CLASS>+'"${TEST_CLASS_CLASS}"'+g' tools_$PROJECT_NAME/PseudoSweep/run-pseudosweep.sh
    sed -i '' 's+<TEST_NAME>+'"${TEST_NAME}"'+g' tools_$PROJECT_NAME/PORBS/config/setup.sh


    #################################################
    # Copy to each tool's working dir 
    #################################################

    # cc-slicer4j
    rm -rf $CWD/tools_$PROJECT_NAME/CheckedCoverage4J/projects/$PROJECT_NAME*
    wait
    cp $PROJECT_PATH $CWD/tools_$PROJECT_NAME/CheckedCoverage4J/projects/ && unzip $CWD/tools_$PROJECT_NAME/CheckedCoverage4J/projects/$ZIP_NAME -d $CWD/tools_$PROJECT_NAME/CheckedCoverage4J/projects/$PROJECT_NAME > logs/$PROJECT_NAME/copy.log

    # cc-porb
    rm -rf $CWD/tools_$PROJECT_NAME/PORBS/code
    rm -rf $CWD/tools_$PROJECT_NAME/PORBS/regression
    wait
    cp $PROJECT_PATH $CWD/tools_$PROJECT_NAME/PORBS/ && unzip $CWD/tools_$PROJECT_NAME/PORBS/$ZIP_NAME -d $CWD/tools_$PROJECT_NAME/PORBS/code/
    rm -rf $CWD/tools_$PROJECT_NAME/PORBS/code/$PROJECT_NAME/

    # pseudosweep
    rm -rf $CWD/tools_$PROJECT_NAME/PseudoSweep/$PROJECT_NAME*
    wait
    cp $PROJECT_PATH $CWD/tools_$PROJECT_NAME/PseudoSweep/ && unzip $CWD/tools_$PROJECT_NAME/PseudoSweep/$ZIP_NAME -d $CWD/tools_$PROJECT_NAME/PseudoSweep/$PROJECT_NAME
    rm $CWD/tools_$PROJECT_NAME/PseudoSweep/$ZIP_NAME

    #################################################
    # Call each tool
    # Move relevant outputs to output dir
    #################################################

    # cc-slicer4j
    cd $CWD/tools_$PROJECT_NAME/CheckedCoverage4J/
    echo "cc-slicer4j" >> $CWD/logs/$PROJECT_NAME/time.log
    { time sh run-checked-coverage-full-project.sh $PROJECT_NAME $JAR_PATH > $CWD/logs/$PROJECT_NAME/CheckedCoverage4J.log ; } 2>> $CWD/logs/$PROJECT_NAME/time.log
    cd $CWD

    if [ -f tools_$PROJECT_NAME/CheckedCoverage4J/output/$PROJECT_NAME/slice.txt ] ; then
        cp tools_$PROJECT_NAME/CheckedCoverage4J/output/$PROJECT_NAME/slice.txt $CWD/results/$PROJECT_NAME/slicer4j_cc_slice.txt
    fi

    # pseudosweep
    cd $CWD/tools_$PROJECT_NAME/PseudoSweep/
    pwd
    echo "pseudosweep" >> $CWD/logs/$PROJECT_NAME/time.log
    { time sh run-pseudosweep.sh $PROJECT_NAME > $CWD/logs/$PROJECT_NAME/pseudosweep.log ; } 2>> $CWD/logs/$PROJECT_NAME/time.log
    cd $CWD
    if [ -f $CWD/tools_$PROJECT_NAME/PseudoSweep/project-data/$PROJECT_NAME/ps-data.zip ] ; then
        cp $CWD/tools_$PROJECT_NAME/PseudoSweep/project-data/$PROJECT_NAME/ps-data.zip $CWD/results/$PROJECT_NAME/
    fi

    # cc-orbs
    cd $CWD/tools_$PROJECT_NAME/PORBS/
    rm -rf regression/*
    echo "cc-orbs" >> $CWD/logs/$PROJECT_NAME/time.log
    { time sh dist/orbs.sh $PROJECT_NAME > $CWD/logs/$PROJECT_NAME/PORBS.log ; } 2>> $CWD/logs/$PROJECT_NAME/time.log
    python3 get_deleted_lines.py
    cd $CWD
    if [ -f $CWD/tools_$PROJECT_NAME/PORBS/config/deleted_lines.txt ] ; then
        cp $CWD/tools_$PROJECT_NAME/PORBS/config/deleted_lines.txt $CWD/results/$PROJECT_NAME/orbs_deleted_lines.txt
    fi

    #################################################
    # Complete
    #################################################
    echo "Execution Complete for " $PROJECT_NAME

    wait 
    # rm -rf tools_$PROJECT_NAME

done < args_1.csv




