from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, window
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, FloatType, TimestampType

spark = SparkSession.builder.appName("KafkaSparkStreaming").getOrCreate()
spark.sparkContext.setLogLevel("WARN")

# Esquema estructurado alineado con el productor ambiental
schema = StructType([
    StructField("sensor_id", IntegerType()),
    StructField("ciudad", StringType()),
    StructField("pm25", FloatType()),
    StructField("co2", FloatType()),
    StructField("timestamp", TimestampType())
])

df = spark.readStream.format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "sensor_data") \
    .load()

parsed_df = df.select(from_json(col("value").cast("string"), schema).alias("data")).select("data.*")

# Procesamiento analítico continuo por ventanas temporales y ciudades
windowed_stats = parsed_df \
    .groupBy(window(col("timestamp"), "1 minute"), "ciudad") \
    .agg({"pm25": "avg", "co2": "avg"})

query = windowed_stats.writeStream.outputMode("complete").format("console").start()
query.awaitTermination()
