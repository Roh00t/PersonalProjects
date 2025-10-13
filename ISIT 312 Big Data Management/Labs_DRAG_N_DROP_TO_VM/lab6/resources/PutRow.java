import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.hbase.HBaseConfiguration;
import org.apache.hadoop.hbase.client.HTable;
import org.apache.hadoop.hbase.client.Put;
import org.apache.hadoop.hbase.util.Bytes;

public class PutRow {
    public static void main(String[] args) throws Exception {
        Configuration conf = HBaseConfiguration.create();
        HTable table = new HTable(conf, "MYTABLE");
        Put put = new Put(Bytes.toBytes("009"));
        put.add(Bytes.toBytes("ADDRESS"), Bytes.toBytes("City"), Bytes.toBytes("Malbourne"));
        put.add(Bytes.toBytes("ADDRESS"), Bytes.toBytes("Street"), Bytes.toBytes("Victoria"));
        put.add(Bytes.toBytes("NAME"), Bytes.toBytes("First"), Bytes.toBytes("Robin"));
        put.add(Bytes.toBytes("NAME"), Bytes.toBytes("Last"), Bytes.toBytes("Hood"));
        table.put(put);
        table.flushCommits();
        table.close();
    }
}
