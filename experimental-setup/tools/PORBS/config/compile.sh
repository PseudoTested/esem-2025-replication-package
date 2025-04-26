pwd
cd $1
rm -r target
timeout -s KILL 600s mvn clean package -DskipTests -Drat.skip=true -Denforcer.skip=true -Dcheckstyle.skip=true > test.log

if [ -d target/classes/ ]; then
    for f in $(find target/classes/ -name '*.class'); do

        # check successful compilation and create signature
        if [ -f $f ]; then
            # The signature must be created from anything that actually
            # influences the execution which is affected by the slicing
            # operation. Usually it is any executed part, binaries and
            # scripts.
            md5sum $f >> ../debug.log
        else
            # In case compilation fails, "FAIL" must be returned.
            echo FAIL
        fi

    done
else
    # In case compilation fails, "FAIL" must be returned.
    echo FAIL
fi

if [ -d target/test-classes/ ]; then
    for f in $(find target/test-classes/ -name '*.class'); do
        # check successful compilation and create signature
        if [ -f $f ]; then
            # The signature must be created from anything that actually
            # influences the execution which is affected by the slicing
            # operation. Usually it is any executed part, binaries and
            # scripts.
            md5sum $f >> ../debug.log
        else
            # In case compilation fails, "FAIL" must be returned.
            echo "compile fail current_dir: $1" >> ../debug.log
            echo FAIL
        fi

    done
else
    # In case compilation fails, "FAIL" must be returned.
    echo FAIL
fi
