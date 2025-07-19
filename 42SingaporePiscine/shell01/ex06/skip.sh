#!/bin/bash
ls -l | awk 'NR % 2 == 1'
# NR  is the number of the  line 
# if the rest of the division of NR by 2  is equl to 1
# in others terms if the number of line isnt pair 
# it will let it out

