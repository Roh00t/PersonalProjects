import java.io.IOException;
//import java.util.StringTokenizer;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.conf.Configured;
import org.apache.hadoop.util.Tool;
import org.apache.hadoop.util.ToolRunner;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.Partitioner;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;

public class WordCountTRP extends Configured implements Tool {


    public int run(String[] args) throws Exception {

        Configuration conf = this.getConf();
        Job job = Job.getInstance(conf, "word count with toolrunner");
        job.setJarByClass(WordCountTRP.class);
        job.setMapperClass(WordCountMapper.class);
        job.setReducerClass(WordCountReducer.class);
        job.setOutputKeyClass(Text.class);
        job.setOutputValueClass(IntWritable.class);
        job.setPartitionerClass(WCPartitioner.class);
        FileInputFormat.addInputPath(job, new Path(args[0]));
        FileOutputFormat.setOutputPath(job, new Path(args[1]));
        return job.waitForCompletion(true) ? 0:1;

    }

    public static void main(String[] args) throws Exception {
       
    	int res = ToolRunner.run(new Configuration(), new WordCountTRP(), args);
    	System.exit(res);
    }

    public static class WordCountMapper extends Mapper<Object, Text, Text, IntWritable>
    {
        private final static IntWritable one = new IntWritable(1);
        private Text wordObject = new Text();

        @Override
        public void map(Object key, Text value, Context context)
                throws IOException, InterruptedException {

            String line = value.toString();
            for (String word : line.split("\\W+")) {
                if (word.length() > 0) {
                    wordObject.set(word.toLowerCase());
                    context.write(wordObject, one);
                }
            }
        }
    }

    public static class WordCountReducer extends Reducer<Text, IntWritable, Text, IntWritable>
    {
        private IntWritable wordCountWritable = new IntWritable();
        @Override
        public void reduce(Text key, Iterable<IntWritable> values, Context context)
                throws IOException, InterruptedException {
            int wordCount = 0;
            for (IntWritable value : values) {
                wordCount += value.get();
            }
            wordCountWritable.set(wordCount);
            context.write(key, wordCountWritable);
        }
    }
    
    public static class WCPartitioner extends Partitioner <Text, IntWritable> {
    	
    	@Override
    	public int getPartition(Text key, IntWritable value, int numReduceTasks ){
    		
    		String word = key.toString();
    		if (word.toLowerCase().matches("^[a-m].*$")) {
    			return 0;
    		} else {
    			return 1;
    		}
    	}
    }

}