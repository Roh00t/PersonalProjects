// Student Name: Rohit Panda
// Student UOW ID: 8943060
// Solution 3

import java.io.IOException;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;

import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;

import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;


public class solution3 {

    // Mapper Class
    public static class SalesMapper extends Mapper<LongWritable, Text, Text, IntWritable> {
        private Text item = new Text();
        private IntWritable amount = new IntWritable();

        @Override
        public void map(LongWritable key, Text value, Context context) throws IOException, InterruptedException {
            String[] parts = value.toString().split("\\s+");
            if (parts.length == 2) {
                try {
                    item.set(parts[0]);
                    amount.set(Integer.parseInt(parts[1]));
                    context.write(item, amount);
                } catch (NumberFormatException e) {
                    // skip malformed lines
                }
            }
        }
    }

    // Reducer Class
    public static class StatsReducer extends Reducer<Text, IntWritable, Text, Text> {
        @Override
        public void reduce(Text key, Iterable<IntWritable> values, Context context) throws IOException, InterruptedException {
            int max = Integer.MIN_VALUE;
            int min = Integer.MAX_VALUE;
            int sum = 0;
            int count = 0;

            for (IntWritable val : values) {
                int v = val.get();
                if (v > max) max = v;
                if (v < min) min = v;
                sum += v;
                count++;
            }

            int avg = (count == 0) ? 0 : sum / count;  // Integer division
            String result = String.format("Max:%d\tMin:%d\tAvg:%d\tTotal:%d", max, min, avg, sum);

            context.write(key, new Text(result));
        }
    }

    // Driver Method
    public static void main(String[] args) throws Exception {
        if (args.length != 2) {
            System.err.println("Usage: solution3 <input path> <output path>");
            System.exit(-1);
        }

        Configuration conf = new Configuration();
        Job job = Job.getInstance(conf, "Sales Statistics");

        job.setJarByClass(solution3.class);
        job.setMapperClass(SalesMapper.class);
        job.setReducerClass(StatsReducer.class);

        job.setMapOutputKeyClass(Text.class);
        job.setMapOutputValueClass(IntWritable.class);

        job.setOutputKeyClass(Text.class);
        job.setOutputValueClass(Text.class);

        FileInputFormat.addInputPath(job, new Path(args[0]));
        FileOutputFormat.setOutputPath(job, new Path(args[1]));

        System.exit(job.waitForCompletion(true) ? 0 : 1);
    }
}