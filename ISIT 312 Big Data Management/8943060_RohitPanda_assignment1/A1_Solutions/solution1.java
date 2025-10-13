// Student Name: Rohit Panda
// Student UOW ID: 8943060

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.FSDataInputStream;
import org.apache.hadoop.fs.FSDataOutputStream;
import org.apache.hadoop.fs.FileSystem;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.IOUtils;

public class solution1 {
    public static void main(String[] args) throws Exception {
        // Check if correct number of arguments provided
        if (args.length != 3) {
            System.err.println("Usage: solution1 <input_file1> <input_file2> <output_file>");
            System.exit(1);
        }

        // Get command line arguments
        String inputFile1 = args[0];
        String inputFile2 = args[1];
        String outputFile = args[2];

        // Create configuration and file system objects
        Configuration conf = new Configuration();
        FileSystem fs = FileSystem.get(conf);

        // Create Path objects for input and output files
        Path path1 = new Path(inputFile1);
        Path path2 = new Path(inputFile2);
        Path pathOut = new Path(outputFile);

        // Check if input files exist
        if (!fs.exists(path1)) {
            System.err.println("Error: First input file does not exist: " + inputFile1);
            System.exit(1);
        }
        if (!fs.exists(path2)) {
            System.err.println("Error: Second input file does not exist: " + inputFile2);
            System.exit(1);
        }

        // Delete output file if it already exists
        if (fs.exists(pathOut)) {
            System.out.println("Output file already exists. Deleting: " + outputFile);
            fs.delete(pathOut, false);
        }

        // Create output stream for writing merged file
        FSDataOutputStream out = fs.create(pathOut);

        System.out.println("Merging files...");
        System.out.println("Input file 1: " + inputFile1);
        System.out.println("Input file 2: " + inputFile2);
        System.out.println("Output file: " + outputFile);

        // Read and copy first input file to output
        System.out.println("\nCopying first file...");
        FSDataInputStream in1 = fs.open(path1);
        IOUtils.copyBytes(in1, out, conf, false);
        in1.close();
        System.out.println("First file copied successfully.");

        // Read and copy second input file to output
        System.out.println("Copying second file...");
        FSDataInputStream in2 = fs.open(path2);
        IOUtils.copyBytes(in2, out, conf, false);
        in2.close();
        System.out.println("Second file copied successfully.");

        // Close output stream
        out.close();
        fs.close();

        System.out.println("\nFiles merged successfully!");
        System.out.println("Merged file created at: " + outputFile);
    }
}
