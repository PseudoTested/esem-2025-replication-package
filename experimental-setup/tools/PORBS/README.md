PORBS SSYSTEM REQUIREMENTS
-----------------------------------
PORBS comes as an executable jar file with all the dependencies bundled. 
It requires JAVA 1.8 or above to run.
 
EXAMPLE PROGRAM SYSTEM REQUIREMENTS
-----------------------------------
1. The example program is a multi-language system and can be executed with default configuration on most Linux distributions.
2. The example program requires JDK, GCC and PYTHON to build and execute the system.
3. The execute script for the example program uses utility commands "time", "timeout", "KILL", "md5sum" and "sed" which needs to be 
available for the example to run correctly.
NOTE: On MAC OS most of these utilities are not available by default. You may need to adapt the script to equivalent commands.

RUNNING THE EXAMPLE WITH PORBS
---------------------------------
1. Move to inside the Example directory, there you will find 3 directories, code, config and dist
2. Type the following command 
	bash dist/orbs.sh	
3. The script should setup the system and start the PROBS slicer on the system

PORBS OUTPUT
----------------------------------
1. Once the slicing completes a new directory will be created inside 'regression' directory where the sliced program will be made available along with log files and statistics.
2. Statistics about the run will be output to "iterationLevelStat.csv" and "windowLevelStat.csv". 
3. A log file will be created showing the details of PORBS run including statistics at orbs.log.
4. A detailed log file will show details of the parallel window attempts during the PORBS run at trace.log. 
This is used for debugging and detailed analysis. This file is usually very large!

TROUBLESHOOTING
---------------------------------
If the slicer does not seems to operate correctly, please do the following in sequential steps:
1. JAVA 1.8 is installed. 'java -version' can be used to identify the default JVM version.
2. cleanup rediual files with 
	bash -x config/cleanup.sh
3. Setup script is behaving correctly by typing 
	bash -x config/setup.sh orig
The output should look like the following:
	+ rm -rf orig
	+ cp -r code orig
	+ cd orig
	+ cat
4. Compile script is behaving correctly by typing
	bash -x config/compile.sh orig
The output should look like the following:
	+ cd orig
	+ rm -f reader checker.class
	+ gcc -o reader reader.c
	+ javac checker.java
	+ '[' -f reader -a -f checker.class ']'
	++ md5sum reader
	++ md5sum checker.class
	++ md5sum glue.py
	+ echo af64994ab103604cb78f621f6478cc50 reader cb2a449bfb633a73f1d63112ed973336 checker.class 073576653feca7bbdd25fc24c87642a2 glue.py
	af64994ab103604cb78f621f6478cc50 reader cb2a449bfb633a73f1d63112ed973336 checker.class 073576653feca7bbdd25fc24c87642a2 glue.py
5. Execute the PORBS Script to check its working correctly and PORBS is started correctly
 	bash -x dist/orbs.sh
The output should look like -
	+ rm -rf orig
	+ cp -r code orig
	+ cd orig
	+ cat
	+ cat config/OrbsFramework.properties
	+ sed -e '3s@.*@PATH = /opt/ucl/bin:/usr/sbin:/sbin:/usr/bin:/bin:/usr/bin/X11:/opt/UCLCSdefunct/bin:/cs/research/crest/home0/sislam/bin.intel:/cs/research/crest/home0/sislam/bin:.;@'
	+ mv config/tmp_file config/OrbsFramework.properties
	+ rm -rf work logs time.log run.log
	+ echo 'Starting PORBS'
	Starting PORBS
	...
	...

SUPPORT
-------------------------------
For any support with installation or running the tool please refer to http://syedislam.com or contact syed.islam@uel.ac.uk 


    
