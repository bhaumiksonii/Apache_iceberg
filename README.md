# Apache IceBerg
Apache Iceberg is a data format and table management system that was designed to address some of the limitations of the Apache Parquet and Apache ORC data formats. It was developed by the Apache Software Foundation as part of the Apache Iceberg project, which aims to improve data management on data lakes and other large-scale data storage systems.

# official docs for python library
```
https://iceberg.apache.org/docs/0.13.1/python-api-intro/
```
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
