#!/bin/bash
groups $FT_USER | cut -d ' ' -f3- | tr ' ' ',' | tr -d '\n' 
# cut -d ' ' -f3-
# -d ' ' => each thing beetween an ' ' will be an element
# -f3- => we will keep all after the 2nd element
# for 
# user : usergroup othergroup1 othergroup2
# it cut "user" and ":"
# do not forget to delete \n to match the exercise :clown:
