import java.io.IOException;

import org.apache.hadoop.hbase.HBaseConfiguration;
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.hbase.client.HBaseAdmin;

public class DropTable {

   public static void main(String[] args) throws IOException {

      // Instantiating configuration class
      Configuration conf = HBaseConfiguration.create();

      // Instantiating HBaseAdmin class
      HBaseAdmin admin = new HBaseAdmin(conf);

      // disabling table named emp
      admin.disableTable("MYTABLE");

      // Deleting emp
      admin.deleteTable("MYTABLE");
      System.out.println("Table \"MYTABLE\" dropped");
   }
}
