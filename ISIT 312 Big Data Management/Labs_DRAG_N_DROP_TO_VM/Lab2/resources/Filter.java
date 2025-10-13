import java.io.IOException;
import java.util.StringTokenizer;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;
import org.apache.hadoop.util.GenericOptionsParser;

public class Filter {

    public static void main(String[] args) throws Exception {
        Configuration conf = new Configuration();
        String[] otherArgs = new GenericOptionsParser(conf, args).getRemainingArgs();
        conf.set("limit", otherArgs[0]);
	Job job = new Job(conf, "Distributed Filter");
	job.setJarByClass(Filter.class);
	job.setMapperClass(FilterMapper.class);
	job.setOutputKeyClass(Text.class);
	job.setOutputValueClass(IntWritable.class);
	job.setNumReduceTasks(0); // Set number of reducers to zero
	FileInputFormat.addInputPath(job, new Path(args[1]));
	FileOutputFormat.setOutputPath(job, new Path(args[2]));
	System.exit(job.waitForCompletion(true) ? 0 : 1);
    }

 public static class FilterMapper
     extends Mapper<Object, Text, Text, IntWritable>{

     private final static IntWritable counter = new IntWritable(0);
     private Text word = new Text();
     private Integer total;
     private Integer limit;
     public void map(Object key, Text value, Context context
		     ) throws IOException, InterruptedException {
	 StringTokenizer itr = new StringTokenizer(value.toString());

	 limit = Integer.parseInt( context.getConfiguration().get("limit") );

	 while (itr.hasMoreTokens()) {
	     word.set(itr.nextToken());
             total = Integer.parseInt(itr.nextToken());
	     if ( total > limit )    
	     { counter.set( total );
	       context.write(word, counter); }
	 }
     }
 }

}
