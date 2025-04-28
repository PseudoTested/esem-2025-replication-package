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
while IFS=',' read -r PROJECT_NAME TEST_CLASS_PACKAGE SRC_FILE TEST_NAME TEST_CLASS_CLASS JAR_PATH CLASS_PACKAGE ; do

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
    

    #################################################
    # Copy to each tool's working dir 
    #################################################

    # PIT
    rm -rf $CWD/tools_$PROJECT_NAME/PIT/$PROJECT_NAME*
    wait
    cp $PROJECT_PATH $CWD/tools_$PROJECT_NAME/PIT/ && unzip $CWD/tools_$PROJECT_NAME/PIT/$ZIP_NAME -d $CWD/tools_$PROJECT_NAME/PIT/$PROJECT_NAME
    rm $CWD/tools_$PROJECT_NAME/PIT/$ZIP_NAME

    echo $CLASS_PACKAGE

    # add PIT to pom
    sed -i '' 's+</plugins>+\
            <plugin>\
                <groupId>org.pitest</groupId>\
                <artifactId>pitest-maven</artifactId>\
                <version>1.19.0</version>\
                <configuration>\
                    <mutators>STRONGER</mutators>\
                    <timestampedReports>False</timestampedReports>\
                    <outputFormats>CSV,XML,HTML</outputFormats>\
                    <targetClasses>\
                        <param>'"${CLASS_PACKAGE}"'*</param>\
                    </targetClasses>\
                    <targetTests>\
                        <param>'"${TEST_CLASS_PACKAGE}"'*</param>\
                    </targetTests>\
                </configuration>\
            </plugin>\
            </plugins>+g' $CWD/tools_$PROJECT_NAME/PIT/$PROJECT_NAME/pom.xml


    #################################################
    # Call each tool
    # Move relevant outputs to output dir
    #################################################

    # pit
    cd $CWD/tools_$PROJECT_NAME/PIT/$PROJECT_NAME
    pwd
    echo "PIT" >> $CWD/logs/$PROJECT_NAME/pit_time.log
    { time mvn clean package dependency:copy-dependencies -Dtest=$TEST_NAME -Dcheckstyle.skip -Denforcer.skip -Djacoco.skip org.pitest:pitest-maven:mutationCoverage ; } 2>> $CWD/logs/$PROJECT_NAME/pit_time.log
    cd $CWD
    if [ -d $CWD/tools_$PROJECT_NAME/PIT/$PROJECT_NAME/target/pit-reports ] ; then
        cp -r $CWD/tools_$PROJECT_NAME/PIT/$PROJECT_NAME/target/pit-reports/ $CWD/results/$PROJECT_NAME/pit-reports/
    fi
    #################################################
    # Complete
    #################################################
    echo "Execution Complete for " $PROJECT_NAME

    wait 
    # rm -rf tools_$PROJECT_NAME

done < args_mt.csv




