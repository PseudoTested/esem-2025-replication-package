#!/bin/bash
# #######################################
# Create .jar file including tests
# #######################################
set -e
export JAVA_HOME=$JDK_17


echo "- enter project directory"
cd projects/$1/


echo "- copy test files to main"
cp -r src/test/java/* src/main/java/
rm -r src/test/java/

echo "- ensure all dependencies from tests are in scope"
sed -i '' 's/<scope>test<\/scope>/<scope>provided<\/scope>/g' pom.xml
sed -i '' '/<profiles>/,/<\/profiles>/d' pom.xml

echo "- build extra fat jar"
echo $JAVA_HOME
mvn clean dependency:copy-dependencies package -Drat.skip=true -Djacoco.skip=true -Denforcer.skip -Dcheckstyle.skip

cd ../..
