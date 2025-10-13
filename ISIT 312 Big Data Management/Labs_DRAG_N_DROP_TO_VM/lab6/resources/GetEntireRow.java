import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.hbase.HBaseConfiguration;
import org.apache.hadoop.hbase.client.Get;
import org.apache.hadoop.hbase.client.HTable;
import org.apache.hadoop.hbase.client.Result;
import org.apache.hadoop.hbase.util.Bytes;

import java.util.Map;
import java.util.NavigableMap;

public class GetEntireRow {
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

        System.out.println("Row key: " + row);
        NavigableMap<byte[], NavigableMap<byte[],NavigableMap<Long,byte[]>>> map = result.getMap();
        for (Map.Entry<byte[], NavigableMap<byte[], NavigableMap<Long, byte[]>>> navigableMapEntry : map.entrySet()) {
            String family = Bytes.toString(navigableMapEntry.getKey());
            System.out.println("\t" + family);
            NavigableMap<byte[], NavigableMap<Long, byte[]>> familyContents = navigableMapEntry.getValue();
            for (Map.Entry<byte[], NavigableMap<Long, byte[]>> mapEntry : familyContents.entrySet()) {
                String qualifier = Bytes.toString(mapEntry.getKey());
                System.out.println("\t\t" + qualifier);
                NavigableMap<Long, byte[]> qualifierContents = mapEntry.getValue();
                for (Map.Entry<Long, byte[]> entry : qualifierContents.entrySet()) {
                    Long timestamp = entry.getKey();
                    String value = Bytes.toString(entry.getValue());
                    System.out.printf("\t\t\t%s, %d\n", value, timestamp);
                }
            }
        }
        table.close();
    }
}

