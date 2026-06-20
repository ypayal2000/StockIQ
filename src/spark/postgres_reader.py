from pyspark.sql import SparkSession


def create_spark_session():
    return (
        SparkSession.builder
        .appName("StockIQ")
        .master("local[*]")
        .config(
            "spark.driver.extraJavaOptions",
            "-Duser.timezone=UTC"
        )
        .config(
            "spark.executor.extraJavaOptions",
            "-Duser.timezone=UTC"
        )
        .config(
            "spark.jars",
            "jars\\postgresql-42.7.3.jar"
        )
        .getOrCreate()
    )

if __name__ == "__main__":

    spark = create_spark_session()

    df = (
        spark.read
        .format("jdbc")
        .option(
            "url",
            "jdbc:postgresql://localhost:5432/stock_market_db?options=-c%20TimeZone=Asia/Kolkata"
        )
        .option("dbtable", "stock_prices")
        .option("user", "postgres")
        .option("password", "postgres")
        .option("driver", "org.postgresql.Driver")
        .load()
    )

    print("\nSchema:")
    df.printSchema()

    print("\nRow Count:")
    print(df.count())

    print("\nSample Data:")
    df.show(5)

    spark.stop()