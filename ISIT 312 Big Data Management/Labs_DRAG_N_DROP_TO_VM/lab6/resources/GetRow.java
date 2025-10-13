import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.hbase.HBaseConfiguration;
import org.apache.hadoop.hbase.client.Get;
import org.apache.hadoop.hbase.client.HTable;
import org.apache.hadoop.hbase.client.Result;
import org.apache.hadoop.hbase.util.Bytes;

import java.util.Map;
import java.util.NavigableMap;

public class GetRow {
    public static void main(String[] args) throws Exception {
        Configuration conf = HBaseConfiguration.create();
        HTable table = new HTable(conf, "MYTABLE");
        Get get = new Get(Bytes.toBytes("007"));
        get.setMaxVersions(3);
        get.addFamily(Bytes.toBytes("ADDRESS"));
        get.addColumn(Bytes.toBytes("ADDRESS"), Bytes.toBytes("City"));
        get.addColumn(Bytes.toBytes("ADDRESS"), Bytes.toBytes("Street"));
        get.addFamily(Bytes.toBytes("NAME"));
        get.addColumn(Bytes.toBytes("NAME"), Bytes.toBytes("First"));
        get.addColumn(Bytes.toBytes("NAME"), Bytes.toBytes("Last"));
        Result result = table.get(get);
        String row = Bytes.toString(result.getRow());

        // Get the specific values
        String specificValue = Bytes.toString(result.getValue(Bytes.toBytes("ADDRESS"), Bytes.toBytes("City")));
        System.out.println("ADDRESS:City is: " + specificValue);
        specificValue = Bytes.toString(result.getValue(Bytes.toBytes("ADDRESS"), Bytes.toBytes("Street")));
        System.out.println("ADDRESS:Street is: " + specificValue);
        specificValue = Bytes.toString(result.getValue(Bytes.toBytes("NAME"), Bytes.toBytes("First")));
        System.out.println("NAME:First is: " + specificValue);
        specificValue = Bytes.toString(result.getValue(Bytes.toBytes("NAME"), Bytes.toBytes("Last")));
        System.out.println("NAME:Last is: " + specificValue);
        table.close();
    }
}

