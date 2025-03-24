ifconfig | grep 'ether' | awk '{print $2}'  
#ifconfig print all the infos of mac adresses but we only need the adress
# grep is used to search a word here we search ether  because it is just before the adress it return all the line with the word
# we pipe this to awk who slect the second word in the line and print it
