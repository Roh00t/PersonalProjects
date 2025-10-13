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
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;

public class WordCountToolRunner extends Configured implements Tool {


    public int run(String[] args) throws Exception {

        // complete the run method //

    }

    public static void main(String[] args) throws Exception {
        // complete the main //
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

}