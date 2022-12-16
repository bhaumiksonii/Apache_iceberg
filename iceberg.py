from pyspark.sql import SparkSession

class IceBerg:
    def __init__(self):
        self.spark = SparkSession.builder \
            .master('local[*]') \
            .appName('myAppName') \
            .config('spark.jars.packages', 'org.apache.iceberg:iceberg-spark-runtime-3.2_2.12:0.13.1')\
            .config('spark.sql.extensions', 'org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions')\
            .config('spark.sql.catalog.spark_catalog', 'org.apache.iceberg.spark.SparkSessionCatalog')\
            .config('spark.sql.catalog.spark_catalog.type', 'hive')\
            .config('spark.sql.catalog.local','org.apache.iceberg.spark.SparkCatalog')\
            .config('spark.sql.catalog.local.type','hadoop')\
            .config('spark.sql.catalog.local.warehouse','iceberg_pyspark/warehouse')\
            .getOrCreate()

            

    def create_table(self):
        self.spark.sql("CREATE TABLE local.db.table (id bigint, data string) USING iceberg")

    def write_data(self):
        self.spark.sql("INSERT INTO local.db.table VALUES (1, 'a'), (2, 'b'), (3, 'c');")
    
    def read_data(self):
        result = self.spark.sql("SELECT * FROM local.db.table;")
        return result.show()
    
    def update_data(self):
        self.spark.sql("INSERT INTO local.db.table VALUES (1, 'a'), (2, 'b'), (3, 'c');")
    
    def inspect_snapshot(self):
        result = self.spark.sql("SELECT * FROM local.db.table.snapshots;")
        return result.show()
ice = IceBerg()


print("**********Creating Table**********")
ice.create_table()


print("**********Writing Table**********")
ice.write_data()


print("**********Reading Table**********")
print(ice.read_data())


print("**********Inspecting Table**********")
print(ice.inspect_snapshot())



