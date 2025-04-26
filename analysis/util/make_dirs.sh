#!/bin/bash

# Array of project_class names
project_classes=(
  bvolpato_inutils4j_MyMapUtils
  CycloneDX_cyclonedx-core-java_BomXmlGenerator
  decorators-squad_eo-yaml_Skip
  EXIficient_exificient_EXIficientCMD
  facebook_facebook-java-business-sdk_BatchProcessor
  heroku_heroku-jvm-application-deployer_PathUtils
  schloepke_jbasics_XOrCryptCodec
  tabulapdf_tabula-java_Table
  tdebatty_java-string-similarity_SorensenDice
  timols_java-gitlab-api_Query
  bvolpato_inutils4j_MyReflectionUtils
  CycloneDX_cyclonedx-core-java_Version
  decorators-squad_eo-yaml_ReadYamlStream
  facebook_facebook-java-business-sdk_HashedListAdaptor
  tdebatty_java-string-similarity_RatcliffObershelp
  bvolpato_inutils4j_MyNumberUtils
  CycloneDX_cyclonedx-core-java_BomLink
  decorators-squad_eo-yaml_JsonYamlDump
  facebook_facebook-java-business-sdk
  tdebatty_java-string-similarity_OptimalStringAlignment
)

# Loop through the array and create directories
for project_class in "${project_classes[@]}"; do
  mkdir -p "$project_class" # -p creates parent directories if needed
  if [ $? -eq 0 ]; then
    echo "Created directory: $project_class"
  else
    echo "Failed to create directory: $project_class"
  fi
done

echo "Folder creation complete."