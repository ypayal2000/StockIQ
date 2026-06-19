from pyspark.sql import SparkSession
from pyspark.sql.window import Window
from pyspark.sql.functions import avg


def create_spark_session():
    return (
        SparkSession.builder
        .appName("StockIQ")
        .master("local[*]")
        .getOrCreate()
    )


if __name__ == "__main__":

    spark = create_spark_session()

    data = [
        ("TCS", "2024-01-01", 3500),
        ("TCS", "2024-01-02", 3550),
        ("TCS", "2024-01-03", 3600),
        ("TCS", "2024-01-04", 3650),
        ("TCS", "2024-01-05", 3700),
    ]

    columns = ["symbol", "trade_date", "close"]

    df = spark.createDataFrame(data, columns)

    window_spec = (
        Window
        .partitionBy("symbol")
        .orderBy("trade_date")
        .rowsBetween(-2, 0)
    )

    result_df = df.withColumn(
        "moving_avg_3",
        avg("close").over(window_spec)
    )

    result_df.show()

    spark.stop()