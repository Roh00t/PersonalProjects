import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.hbase.HBaseConfiguration;
import org.apache.hadoop.hbase.HColumnDescriptor;
import org.apache.hadoop.hbase.HTableDescriptor;
import org.apache.hadoop.hbase.TableName;
import org.apache.hadoop.hbase.client.HBaseAdmin;

public class ListTables {
    public static void main(String[] args) throws Exception {
        Configuration conf = HBaseConfiguration.create();
        HBaseAdmin admin = new HBaseAdmin(conf);
// Get all the list of tables using HBaseAdmin object
      HTableDescriptor[] xtableDescriptor = admin.listTables();

// Display the names of all tables
      System.out.println("HBase tables:");
      for (int i=0; i<xtableDescriptor.length;i++ ){
	  System.out.println(xtableDescriptor[i].getNameAsString());}

    }
}
