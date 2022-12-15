# Apache IceBerg
Apache Iceberg is a data format and table management system that was designed to address some of the limitations of the Apache Parquet and Apache ORC data formats. It was developed by the Apache Software Foundation as part of the Apache Iceberg project, which aims to improve data management on data lakes and other large-scale data storage systems.

# How do IceBerg tables work?
Iceberg uses a **snapshot based querying model**, where data files are mapped using _manifest and metadata files_. Even when data grows at scale, querying on these table gives high performance, as data is accessible at the file level. **These mappings are stored in an Iceberg catalog**.

Athena supports Apache Iceberg tables that use the Apache Parquet format for data and the **AWS Glue catalog for their metastore**__.

# Python Library
```
from iceberg.hive import HiveTables

# instantiate Hive Tables
conf = {"hive.metastore.uris": 'thrift://{hms_host}:{hms_port}'}
tables = HiveTables(conf)

# load table
tbl = tables.load("iceberg_db.iceberg_test_table")

# inspect metadata
print(tbl.schema())
print(tbl.spec())
print(tbl.location())

# get table level record count
from pprint import pprint
pprint(int(tbl.current_snapshot().summary.get("total-records")))
```
# PySpark
```
spark-sql --packages org.apache.iceberg:iceberg-spark-runtime-3.2_2.12:0.13.1\
    --conf spark.sql.extensions=org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions \
    --conf spark.sql.catalog.spark_catalog=org.apache.iceberg.spark.SparkSessionCatalog \
    --conf spark.sql.catalog.spark_catalog.type=hive \
    --conf spark.sql.catalog.local=org.apache.iceberg.spark.SparkCatalog \
    --conf spark.sql.catalog.local.type=hadoop \
    --conf spark.sql.catalog.local.warehouse=$PWD/warehouse
####Creating table
##To create your first Iceberg table in Spark, use the spark-sql shell or spark.sql(...) to run a CREATE TABLE command:

-- local is the path-based catalog defined above
CREATE TABLE local.db.table (id bigint, data string) USING iceberg

####Writing
##Once your table is created, insert data using INSERT INTO:

INSERT INTO local.db.table VALUES (1, 'a'), (2, 'b'), (3, 'c');
INSERT INTO local.db.table SELECT id, data FROM source WHERE length(data) = 1;

##Iceberg also adds row-level SQL updates to Spark, MERGE INTO and DELETE FROM:

MERGE INTO local.db.target t USING (SELECT * FROM updates) u ON t.id = u.id
WHEN MATCHED THEN UPDATE SET t.count = t.count + u.count
WHEN NOT MATCHED THEN INSERT *

##Iceberg supports writing DataFrames using the new v2 DataFrame write API:

spark.table("source").select("id", "data")
     .writeTo("local.db.table").append()

####Reading
##To read with SQL, use the an Iceberg table name in a SELECT query:

SELECT count(1) as count, data
FROM local.db.table
GROUP BY data

##SQL is also the recommended way to inspect tables. To view all of the snapshots in a table, use the snapshots metadata table:

SELECT * FROM local.db.table.snapshots
```
# AWS Athena
```
CREATE TABLE iceberg_table (
  id int,
  data string,
  category string) 
PARTITIONED BY (category, bucket(16,id)) 
LOCATION 's3://DOC-EXAMPLE-BUCKET/iceberg-folder' 
TBLPROPERTIES (
  'table_type'='ICEBERG',
  'format'='parquet',
  'write_target_data_file_size_bytes'='536870912',
  'optimize_rewrite_delete_file_threshold'='10'
)
```
