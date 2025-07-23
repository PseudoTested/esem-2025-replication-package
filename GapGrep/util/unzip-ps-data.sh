#!/bin/bash

cd ./project_data || exit


for dir in */; do
    # Extract directory name

    echo $dir
    cd $dir || exit

    #!/bin/bash

    # Function to check if a directory exists
    directory_exists() {
        if [ -d "$1" ]; then
            return 0  # Directory exists
        else
            return 1  # Directory does not exist
        fi
    }

    # Function to check if a file exists
    file_exists() {
        if [ -f "$1" ]; then
            return 0  # File exists
        else
            return 1  # File does not exist
        fi
    }

    # Check for 'ps-data' directory
    if directory_exists "ps-data"; then
        echo "Directory 'ps-data' exists."
    elif file_exists "ps-data.zip"; then
        echo "File 'ps-data.zip' exists. Unzipping..."
        unzip -q "ps-data.zip"
        if [ $? -eq 0 ]; then
            echo "Unzip successful."
        else
            echo "Failed to unzip 'ps-data.zip'."
            exit 1
        fi
#    else
#        echo "Neither 'ps-data' directory nor 'ps-data.zip' file found. Removing current folder..."
#        rm -rf "$(pwd)"
#        if [ $? -eq 0 ]; then
#            echo "Current folder removed."
#        else
#            echo "Failed to remove current folder."
#            exit 1
#        fi
    fi

    cd ../

done