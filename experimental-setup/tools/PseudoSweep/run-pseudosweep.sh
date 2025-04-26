echo "$1"
cd "$1"

export JAVA_HOME=$JDK_17
export PSWCP=$PWD/../PseudoSweep/lib/build/libs/pseudosweep-0.0.1-SNAPSHOT.jar   
echo $PSWCP

sed -i '' 's/<\/dependencies>/<!--PseudoSweep-->\n<dependency>\n<groupId>org.pseudosweep<\/groupId>\n<artifactId>pseudosweep<\/artifactId>\n<version>0.0.1<\/version>\n<scope>system<\/scope>\n<systemPath>${env.PSWCP}<\/systemPath>\n<\/dependency>\n<\/dependencies>\n/g' pom.xml 
sed -i '' '/<profiles>/,/<\/profiles>/d' pom.xml

var=$(pwd)
basename $(pwd)
PROJECT_NAME="$(basename $PWD)"
echo "$PROJECT_NAME"
# RESET
rm -r ../project-data/$PROJECT_NAME
java -cp $PSWCP org.pseudosweep.Launch restore -p src/main/java/ -sdl

# CLASSPATH FOR PSEUDOSWEEP
mvn dependency:build-classpath -Dmdep.outputFile=cp.txt
export CLASSPATH=$CLASSPATH:$(<cp.txt)
echo $CLASSPATH
rm -r target/

# PSEUDOSWEEP - SDL
echo "RUNNING PSEUDOSWEEP SDL"
rm -r ps-data/
java -cp $PSWCP org.pseudosweep.Launch restore -p src/main/java/ -sdl
java -cp $PSWCP org.pseudosweep.Launch instrument -f <SRC_FILE> -sdl

mvn clean -l log_sdl-compile.log -Dcheckstyle.skip -Drat.skip=true package
if grep "BUILD FAILURE" log_sdl-compile.log; then
    exit 1
fi
java -cp target/classes/:target/test-classes/:$PSWCP:$CLASSPATH org.pseudosweep.Launch sweep -f <TEST_CLASS_CLASS> -sdl 
if grep "FATAL" ps-data/sweep.log; then
    exit 1
fi
java -cp $PSWCP org.pseudosweep.Launch analyze -sdl 


zip -r ps-data.zip PS-data/
mkdir -p ../project-data/$PROJECT_NAME && mv ps-data.zip ../project-data/$PROJECT_NAME/

cd ..
