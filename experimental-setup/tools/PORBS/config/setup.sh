#!/bin/sh
export JAVA_HOME=$JDK_1_8

rm -rf $1 #Remove existing setup
sed -i '' '/<profiles>/,/<\/profiles>/d' code/pom.xml
cp -r code $1 #Setup of the program
cd $1 #Move to the setup
#Setup of test script
cat > orbstest.sh <<EOF
#!/bin/sh
mvn clean test -Dtest=<TEST_NAME> -Drat.skip=true -Denforcer.skip=true -Dcheckstyle.skip
EOF
