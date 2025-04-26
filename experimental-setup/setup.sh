#/bin/bash

# Env
rm -rf tools/CheckedCoverage4J
rm -rf tools/PseudoSweep/PseudoSweep
rm -rf logs/*

# Clone tools 
git clone git@github.com:MgnMtn/CheckedCoverage4J.git $PWD/tools/CheckedCoverage4J
git clone git@github.com:PseudoTested/PseudoSweep.git $PWD/tools/PseudoSweep/PseudoSweep

# Build tools
cd $PWD/tools/CheckedCoverage4J/
sh setup.sh
cd ../../


cd $PWD/tools/PseudoSweep/PseudoSweep/
./gradlew clean build
cd ../../..



