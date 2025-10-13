import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.hbase.HBaseConfiguration;
import org.apache.hadoop.hbase.client.Get;
import org.apache.hadoop.hbase.client.Scan;
import org.apache.hadoop.hbase.client.ResultScanner;
import org.apache.hadoop.hbase.client.HTable;
import org.apache.hadoop.hbase.client.Result;
import org.apache.hadoop.hbase.util.Bytes;

import java.util.Map;
import java.util.NavigableMap;

public class ScanTable {
    public static void main(String[] args) throws Exception {
        Configuration conf = HBaseConfiguration.create();
        HTable table = new HTable(conf, "MYTABLE");
        Scan scan = new Scan();
        scan.addColumn(Bytes.toBytes("ADDRESS"), Bytes.toBytes("City"));
        scan.addColumn(Bytes.toBytes("ADDRESS"), Bytes.toBytes("Street"));
        scan.addFamily(Bytes.toBytes("NAME"));
        scan.addColumn(Bytes.toBytes("NAME"), Bytes.toBytes("First"));
        scan.addColumn(Bytes.toBytes("NAME"), Bytes.toBytes("Last"));
        scan.setStartRow(Bytes.toBytes("007"));
        scan.setStopRow(Bytes.toBytes("010"));
        ResultScanner scanner = table.getScanner(scan);
	try{
	    for(Result result : scanner ) {
            // Get the specific values
                String specificValue = Bytes.toString(result.getValue(Bytes.toBytes("ADDRESS"), Bytes.toBytes("City")));
                System.out.println("ADDRESS:City is: " + specificValue);
                specificValue = Bytes.toString(result.getValue(Bytes.toBytes("ADDRESS"), Bytes.toBytes("Street")));
                System.out.println("ADDRESS:Street is: " + specificValue);
                specificValue = Bytes.toString(result.getValue(Bytes.toBytes("NAME"), Bytes.toBytes("First")));
                System.out.println("NAME:First is: " + specificValue);
                specificValue = Bytes.toString(result.getValue(Bytes.toBytes("NAME"), Bytes.toBytes("Last")));
                System.out.println("NAME:Last is: " + specificValue);
            }
	} finally { scanner.close(); }
    }
}

