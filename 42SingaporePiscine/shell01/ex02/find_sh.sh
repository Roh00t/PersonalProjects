#!/bin/bash
find . -type f -name "*.sh" -exec basename {} '.sh' \;
# {} is the placeholder it represent the data for each entry
#  -exec execute the folowing comand on each entry 
