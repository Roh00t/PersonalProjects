//import java.io.IOException;
import java.net.URI;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.FileStatus;
import org.apache.hadoop.fs.FileSystem;
import org.apache.hadoop.fs.Path;

public class ListFileNames {

    public static void main(String[] args) throws Exception {
        String uri = args[0];
        Configuration conf = new Configuration();
        FileSystem fs = FileSystem.get(URI.create(uri), conf);

        Path[] paths = new Path[args.length];
        for (int i = 0; i < paths.length; i++) {
            paths[i] = new Path(args[i]);
        }


            FileStatus[] status = fs.listStatus(paths);
            for (FileStatus s : status) {
                String p = s.getPath().toString();
                long m = s.getLen();
                boolean b = s.isDirectory();
                System.out.println(p + "\t length: " + m + "\t isDirectory: " + b);
            }

    }
}
