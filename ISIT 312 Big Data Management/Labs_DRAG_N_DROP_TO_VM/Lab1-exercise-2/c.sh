export HADOOP_CLASSPATH=$($HADOOP_HOME/bin/hadoop classpath)
javac -classpath ${HADOOP_CLASSPATH} Grep.java
