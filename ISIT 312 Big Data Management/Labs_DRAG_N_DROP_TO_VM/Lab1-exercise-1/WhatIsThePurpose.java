import java.io.IOException;
import java.net.URI;


import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.FSDataInputStream;
import org.apache.hadoop.fs.FSDataOutputStream;
import org.apache.hadoop.fs.FileStatus;
import org.apache.hadoop.fs.FileSystem;
import org.apache.hadoop.fs.Path;


public class WhatIsThePurpose {

    public static void main(String[] args) throws IOException {

	// read in the first argument from the command line as the
	// localstr which is the local directory/path where the
	// file/files is present.
	String localStr = args[0];

	// read in the second argument from the command line as the
	// hdfs string, which is the address/path of the hadoop
	// distributed storage system.
     	String hdfsStr = args[1]; 

	// create an object of the configuration class, to specify
	// the order in which the files will be read and outputted
	// into the distributed file system.
  	Configuration conf = new Configuration();

	// create the instance of the distributed filesystem / 	
	// directory at the path defined by the user, with the
	// default configuration
    	FileSystem hdfs  = FileSystem.get(URI.create(hdfsStr), conf); 

	// Obtaining the local filesystem instance
	FileSystem local = FileSystem.getLocal(conf);

	// The local directory is named and passed as the input
	// directory, and a path for this input dir is created.
    	Path inputDir = new Path(localStr);

	// Name the folder where the local files are stored as the
	// same name of the inputdir
    	String folderName = inputDir.getName();

	// Create a new path based on the folderName resolved 
	// against the hdfs path
    	Path hdfsFile = new Path(hdfsStr, folderName);

        try {
		// check the status of the local files whether they 
		// are open, or closed.
          	FileStatus[] inputFiles = local.listStatus(inputDir);

		// Set the output stream to be to the hdfs file path
		// created above, where the local files will be 
		// written to
           FSDataOutputStream out = hdfs.create(hdfsFile);
			
		// for all the files present in the input directory
		// which is the local directory
           for (int i=0; i<inputFiles.length; i++) {
			// print out the first files name and path
                	System.out.println
				(inputFiles[i].getPath().getName());
			// get the input stream for the files present 
			// in the local directory
                	FSDataInputStream in =
				 local.open(inputFiles[i].getPath());
			// set a buffer of size 256 bytes which is 
			// more than enough for each file.
                	byte buffer[] = new byte[256];
			
			// set the bytes read to be 0 as initially 
			// we have not read any file yet, also help 
			// to refresh the bytesRead for the next file
                	int bytesRead = 0;
			
			// while the bytesRead is > than the buffer size
                	while( (bytesRead = in.read(buffer)) > 0) {
				// write the file onto the buffer 
                    	out.write(buffer, 0, bytesRead);
                	}
			
			// once the file is written close the input stream
                	in.close();
           	}
			
		// once all the files from the local directory are
		// written onto the hdfs files, close the output stream.
		out.close();
		
		// catch any error or exception during the file 
		// writing process
        } catch (IOException e) {
            e.printStackTrace();	// print where the error has
						// occurred so it can be easier
						// to debug and solve the error
        }
    }
}

// What is the purpose of this program?
/* The purpose of this program is to write the local files present on your computer or any other local system on to the hadoop distributed storage system, where all the files in the local address provided will be written onto the hdfs filesystem. */
