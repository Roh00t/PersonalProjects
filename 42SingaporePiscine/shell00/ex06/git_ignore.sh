git ls-files --others --ignored --exclude-standard

#--ignored to see all the files ignored
# -i need -c or -o to work 
# our files are ignored so they can't be tracked so ... => --others
# --others need a pattern exclusion so we use the one defined in the .git folder of our project so --exclude-standard
