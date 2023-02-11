# Place the .lms file in the sub directory it should be in ./inputs/.../
# From there call this script with the file name as parameter
# Get the file name without extension
file_name="${1%.*}"
# Make a folder with the file name
mkdir ${file_name}
# Move the file into the folder
mv $1 "${file_name}/${1}"
# Go into the folder
cd ${file_name} || return
# Unzip the file
unzip $1
# Unzip the scratch file
unzip "scratch.sb3"
# Remove all but the .lms, .json and .svg
shopt -s extglob
rm -v !("project.json"|"${1}"|"icon.svg")