# Delete the Hbase table task2 to recreate it.
disable 'task2'
drop 'task2'

# Create the Hbase table task2.
create 'task2', 'SALES-TRX','CUSTOMER','PRODUCT','DATE'

# Put/insert information about a customer '007'.
put 'task2','customer:007','CUSTOMER:customerId','007'
put 'task2','customer:007','CUSTOMER:customerName','James Bond'
put 'task2','customer:007','CUSTOMER:location','England'
put 'task2','customer:007','CUSTOMER:ageGroup','15 - 64'

# Put/insert information about a customer '666'.
put 'task2','customer:666','CUSTOMER:customerId','666'
put 'task2','customer:666','CUSTOMER:customerName','Harry Potter'
put 'task2','customer:666','CUSTOMER:location','England'
put 'task2','customer:666','CUSTOMER:ageGroup','<15'

# Put/insert information about a customer '888'.
put 'task2','customer:888','CUSTOMER:customerId','888'
put 'task2','customer:888','CUSTOMER:customerName','Wukong'
put 'task2','customer:888','CUSTOMER:location','China'
put 'task2','customer:888','CUSTOMER:ageGroup','>64'

# Put/insert information about a product '101'.
put 'task2','product:101','PRODUCT:productId','101'
put 'task2','product:101','PRODUCT:productName','1 TB SSD'
put 'task2','product:101','PRODUCT:category','Storage'
put 'task2','product:101','PRODUCT:brand','Samsung'
put 'task2','product:101','PRODUCT:unitPrice',119

# Put/insert information about a product '102'.
put 'task2','product:102','PRODUCT:productId','102'
put 'task2','product:102','PRODUCT:productName','Samsung Galaxy S24 Ultra 5G 512GB'
put 'task2','product:102','PRODUCT:category','Mobile Phone'
put 'task2','product:102','PRODUCT:brand','Samsung'
put 'task2','product:102','PRODUCT:unitPrice',1600

# Put/insert information about a product '202'.
put 'task2','product:202','PRODUCT:productId','202'
put 'task2','product:202','PRODUCT:productName','Apple iPhone 16 Pro Max'
put 'task2','product:202','PRODUCT:category','Mobile Phone'
put 'task2','product:202','PRODUCT:brand','Apple'
put 'task2','product:202','PRODUCT:unitPrice',2100

# Put/insert information about a product '302'.
put 'task2','product:302','PRODUCT:productId','302'
put 'task2','product:302','PRODUCT:productName','Xiaomi Redmi Note 13 Pro 5G 256GB'
put 'task2','product:302','PRODUCT:category','Mobile Phone'
put 'task2','product:302','PRODUCT:brand','Xiaomi'
put 'task2','product:302','PRODUCT:unitPrice',400

# Put/insert information about a product '303'.
put 'task2','product:303','PRODUCT:productId','303'
put 'task2','product:303','PRODUCT:productName','Xiaomi Redmi Watch 4'
put 'task2','product:303','PRODUCT:category','Watch'
put 'task2','product:303','PRODUCT:brand','Xiaomi'
put 'task2','product:303','PRODUCT:unitPrice',100

# Put/insert information about DATE.
put 'task2','date:20240110','DATE:year','2024'
put 'task2','date:20240110','DATE:month','01'
put 'task2','date:20240110','DATE:day','10'
put 'task2','date:20240110','DATE:quarter','01'
put 'task2','date:20240110','DATE:dayOfWeek','Wednesday'
#
put 'task2','date:20240128','DATE:year','2024'
put 'task2','date:20240128','DATE:month','01'
put 'task2','date:20240128','DATE:day','28'
put 'task2','date:20240128','DATE:quarter','01'
put 'task2','date:20240128','DATE:dayOfWeek','Sunday'
#
put 'task2','date:20240130','DATE:year','2024'
put 'task2','date:20240130','DATE:month','01'
put 'task2','date:20240130','DATE:day','30'
put 'task2','date:20240130','DATE:quarter','01'
put 'task2','date:20240130','DATE:dayOfWeek','Tuesday'
#
put 'task2','date:20240206','DATE:year','2024'
put 'task2','date:20240206','DATE:month','02'
put 'task2','date:20240206','DATE:day','06'
put 'task2','date:20240206','DATE:quarter','01'
put 'task2','date:20240206','DATE:dayOfWeek','Tuesday'
#
put 'task2','date:20240217','DATE:year','2024'
put 'task2','date:20240217','DATE:month','02'
put 'task2','date:20240217','DATE:day','17'
put 'task2','date:20240217','DATE:quarter','01'
put 'task2','date:20240217','DATE:dayOfWeek','Saturday'
#
put 'task2','date:20240222','DATE:year','2024'
put 'task2','date:20240222','DATE:month','02'
put 'task2','date:20240222','DATE:day','22'
put 'task2','date:20240222','DATE:quarter','01'
put 'task2','date:20240222','DATE:dayOfWeek','Thursday'
#
put 'task2','date:20240304','DATE:year','2024'
put 'task2','date:20240304','DATE:month','03'
put 'task2','date:20240304','DATE:day','04'
put 'task2','date:20240304','DATE:quarter','01'
put 'task2','date:20240304','DATE:dayOfWeek','Wednesday'
#
put 'task2','date:20240306','DATE:year','2024'
put 'task2','date:20240306','DATE:month','03'
put 'task2','date:20240306','DATE:day','06'
put 'task2','date:20240306','DATE:quarter','01'
put 'task2','date:20240306','DATE:dayOfWeek','Wednesday'
#
put 'task2','date:20240330','DATE:year','2024'
put 'task2','date:20240330','DATE:month','03'
put 'task2','date:20240330','DATE:day','30'
put 'task2','date:20240330','DATE:quarter','01'
put 'task2','date:20240330','DATE:dayOfWeek','Saturday'
#
put 'task2','date:20240416','DATE:year','2024'
put 'task2','date:20240416','DATE:month','04'
put 'task2','date:20240416','DATE:day','16'
put 'task2','date:20240416','DATE:quarter','01'
put 'task2','date:20240416','DATE:dayOfWeek','Tuesday'
#
put 'task2','date:20240427','DATE:year','2024'
put 'task2','date:20240427','DATE:month','04'
put 'task2','date:20240427','DATE:day','27'
put 'task2','date:20240427','DATE:quarter','01'
put 'task2','date:20240427','DATE:dayOfWeek','Saturday'
#
put 'task2','date:20240428','DATE:year','2024'
put 'task2','date:20240428','DATE:month','04'
put 'task2','date:20240428','DATE:day','28'
put 'task2','date:20240428','DATE:quarter','01'
put 'task2','date:20240428','DATE:dayOfWeek','Sunday'
#

# Put/insert information about a sales transaction of product 202 by
# customer '007'.
put 'task2','salestrx:007|202|28012025','SALES-TRX:salesId','20240101'
put 'task2','salestrx:007|202|28012025','DATE:sYear','2024'
put 'task2','salestrx:007|202|28012025','DATE:sMonth','01'
put 'task2','salestrx:007|202|28012025','DATE:sDay','28'
put 'task2','salestrx:007|202|28012025','CUSTOMER:customerId','007'
put 'task2','salestrx:007|202|28012025','PRODUCT:productId','202'
put 'task2','salestrx:007|202|28012025','SALES-TRX:quantitySold',1
put 'task2','salestrx:007|202|28012025','SALES-TRX:totalSale',2100
put 'task2','salestrx:007|202|28012025','SALES-TRX:discount',0.1

# Put/insert information about a sales transaction of product 101 by
# customer '007'.
put 'task2','salestrx:007|101|30012025','SALES-TRX:salesId','20240102'
put 'task2','salestrx:007|101|30012025','DATE:sYear','2024'
put 'task2','salestrx:007|101|30012025','DATE:sMonth','01'
put 'task2','salestrx:007|101|30012025','DATE:sDay','30'
put 'task2','salestrx:007|101|30012025','CUSTOMER:customerId','007'
put 'task2','salestrx:007|101|30012025','PRODUCT:productId','101'
put 'task2','salestrx:007|101|30012025','SALES-TRX:quantitySold',2
put 'task2','salestrx:007|101|30012025','SALES-TRX:totalSale',238
put 'task2','salestrx:007|101|30012025','SALES-TRX:discount',0.2

# Put/insert information about a sales transaction of product 302 by
# customer '888'.
put 'task2','salestrx:888|302|06032025','SALES-TRX:salesId','20240301'
put 'task2','salestrx:888|302|06032025','DATE:sYear','2024'
put 'task2','salestrx:888|302|06032025','DATE:sMonth','03'
put 'task2','salestrx:888|302|06032025','DATE:sDay','06'
put 'task2','salestrx:888|302|06032025','CUSTOMER:customerId','888'
put 'task2','salestrx:888|302|06032025','PRODUCT:productId','302'
put 'task2','salestrx:888|302|06032025','SALES-TRX:quantitySold',2
put 'task2','salestrx:888|302|06032025','SALES-TRX:totalSale',800
put 'task2','salestrx:888|302|06032025','SALES-TRX:discount',0.3

# Put/insert information about a sales transaction of product 102 by
# customer '007'.
put 'task2','salestrx:666|102|22022025','SALES-TRX:salesId','20240201'
put 'task2','salestrx:666|102|22022025','DATE:sYear','2024'
put 'task2','salestrx:666|102|22022025','DATE:sMonth','02'
put 'task2','salestrx:666|102|22022025','DATE:sDay','22'
put 'task2','salestrx:666|102|22022025','CUSTOMER:customerId','666'
put 'task2','salestrx:666|102|22022025','PRODUCT:productId','102'
put 'task2','salestrx:666|102|22022025','SALES-TRX:quantitySold',1
put 'task2','salestrx:666|102|22022025','SALES-TRX:totalSale',1600
put 'task2','salestrx:666|102|22022025','SALES-TRX:discount',0.2

# Put/insert information about a sales transaction of product 302 by
# customer '888'.
put 'task2','salestrx:888|303|28042025','SALES-TRX:salesId','20240401'
put 'task2','salestrx:888|303|28042025','DATE:sYear','2024'
put 'task2','salestrx:888|303|28042025','DATE:sMonth','04'
put 'task2','salestrx:888|303|28042025','DATE:sDay','28'
put 'task2','salestrx:888|303|28042025','CUSTOMER:customerId','888'
put 'task2','salestrx:888|303|28042025','PRODUCT:productId','303'
put 'task2','salestrx:888|303|28042025','SALES-TRX:quantitySold',5
put 'task2','salestrx:888|303|28042025','SALES-TRX:totalSale',500
put 'task2','salestrx:888|303|28042025','SALES-TRX:discount',0.4

# Describing the structure of the Hbase table 'task2'
describe 'task2'

# Scan/display the content of the Hbase table 'task2'
scan 'task2'
