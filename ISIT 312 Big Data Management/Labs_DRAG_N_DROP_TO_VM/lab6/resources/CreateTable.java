import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.hbase.HBaseConfiguration;
import org.apache.hadoop.hbase.HColumnDescriptor;
import org.apache.hadoop.hbase.HTableDescriptor;
import org.apache.hadoop.hbase.TableName;
import org.apache.hadoop.hbase.client.HBaseAdmin;

public class CreateTable {
    public static void main(String[] args) throws Exception {
        Configuration conf = HBaseConfiguration.create();
        HBaseAdmin admin = new HBaseAdmin(conf);
// Create HBase table MYTABLE with column familes ADDRESS and NAME
        HTableDescriptor tableDescriptor = new HTableDescriptor(TableName.valueOf("MYTABLE"));
        tableDescriptor.addFamily(new HColumnDescriptor("ADDRESS"));
        tableDescriptor.addFamily(new HColumnDescriptor("NAME"));
        admin.createTable(tableDescriptor);
    }
}
