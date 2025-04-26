#!/bin/sh
ElapsedTimeLimit=600s
cd $1 # move to directory 

time timeout -s KILL $ElapsedTimeLimit sh orbstest.sh > run.log
grep "BUILD SUCCESS" run.log > output.orbs #execute

# Usually, the execution will be much more complicated as it has to
# deal with timeouts and crashes.

# Extract projected trajectory from the captured output.

rc=$? #capture return code
COUNT=$(grep -c "BUILD SUCCESS" output.orbs)
echo Count: $COUNT >> ../debug.log

if grep -q "BUILD SUCCESS" output.orbs ; then
    # echo ${<"output.orbs"} >> ../debug.log
    grep "$2" output.orbs | md5sum >> ../debug.log #capture hash of return
    echo "BUILD SUCCESS"
else
    echo FAIL
fi

rm -rf output.orbs run.log # clear output file

echo $rc >> ../debug.log
exit $rc # return
