from pyspark.sql import SparkSession
from pyspark.sql.window import Window
from pyspark.sql.functions import avg, round, lag, col, stddev, when
from src.utils.logger import logger 


def create_spark_session():
    """
    Create Spark session.
    """
    logger.info("creating spark session")
    spark = (
        SparkSession.builder
        .appName("Stock Analytics")
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
            "spark.driver.extraClassPath",
            "jars/postgresql-42.7.3.jar"
        )
        .config(
            "spark.executor.extraClassPath",
            "jars/postgresql-42.7.3.jar"
        )
        .config(
        "spark.jars",
        "/opt/airflow/jars/postgresql-42.7.3.jar"
        )
        .getOrCreate()
    )

    spark.sparkContext.setLogLevel("ERROR")

    return spark


def read_stock_data(spark):
    """
    Read stock data from PostgreSQL.
    """
    logger.info("Read Stock Data: start")
    return (
        spark.read
        .format("jdbc")
        .option(
            "url",
            "jdbc:postgresql://host.docker.internal:5432/stock_market_db"
        )
        .option("dbtable", "stock_prices")
        .option("user", "postgres")
        .option("password", "postgres")
        .option("driver", "org.postgresql.Driver")
        .load()
    )


# def calculate_moving_average(df):
#     """
#     Calculate 3-day moving average.
#     """

#     window_spec = (
#         Window
#         .partitionBy("symbol")
#         .orderBy("trade_date")
#         .rowsBetween(-2, 0)
#     )

#     return df.withColumn(
#         "moving_avg_3",
#         round(
#             avg("close").over(window_spec),
#             2
#         )
#     )

def calculate_moving_averages(df):
    """
    Calculate multiple moving averages.
    """
    logger.info("calculating moving averages: start")
    window_3 = (
        Window
        .partitionBy("symbol")
        .orderBy("trade_date")
        .rowsBetween(-2, 0)
    )

    window_5 = (
        Window
        .partitionBy("symbol")
        .orderBy("trade_date")
        .rowsBetween(-4, 0)
    )

    window_10 = (
        Window
        .partitionBy("symbol")
        .orderBy("trade_date")
        .rowsBetween(-9, 0)
    )

    window_20 = (
        Window
        .partitionBy("symbol")
        .orderBy("trade_date")
        .rowsBetween(-19, 0)
    )

    logger.info("calculating moving averages: start")
    return (
        df
        .withColumn(
            "moving_avg_3",
            round(avg("close").over(window_3), 2)
        )
        .withColumn(
            "moving_avg_5",
            round(avg("close").over(window_5), 2)
        )
        .withColumn(
            "moving_avg_10",
            round(avg("close").over(window_10), 2)
        )
        .withColumn(
            "moving_avg_20",
            round(avg("close").over(window_20), 2)
        )
    )


def calculate_multi_day_returns(df):
    """
    Calculate 3-day and 5-day returns.
    """
    logger.info("Calculate multi day return: Start")
    window_spec = (
        Window
        .partitionBy("symbol")
        .orderBy("trade_date")
    )
    logger.info("Calculate multi day return: END")

    return (
        df
        .withColumn(
            "close_3d_ago",
            lag("close", 3).over(window_spec)
        )
        .withColumn(
            "close_5d_ago",
            lag("close", 5).over(window_spec)
        )
        .withColumn(
            "return_3d",
            round(
                (
                    (col("close") - col("close_3d_ago"))
                    / col("close_3d_ago")
                ) * 100,
                2
            )
        )
        .withColumn(
            "return_5d",
            round(
                (
                    (col("close") - col("close_5d_ago"))
                    / col("close_5d_ago")
                ) * 100,
                2
            )
        )
    )


def calculate_volume_features(df):
    """
    Calculate rolling volume averages.
    """
    logger.info("Calculate Volume feature: Start")

    volume_window_5 = (
        Window
        .partitionBy("symbol")
        .orderBy("trade_date")
        .rowsBetween(-4, 0)
    )

    volume_window_20 = (
        Window
        .partitionBy("symbol")
        .orderBy("trade_date")
        .rowsBetween(-19, 0)
    )
    logger.info("Calculate volume feature: End")
    return (
        df
        .withColumn(
            "avg_volume_5",
            round(
                avg("volume").over(volume_window_5),
                2
            )
        )
        .withColumn(
            "avg_volume_20",
            round(
                avg("volume").over(volume_window_20),
                2
            )
        )
    )


def calculate_price_vs_ma20(df):
    """
    Distance from 20 day moving average.
    """
    logger.info("Calculate calculate_price_vs_ma20: Start")
    return (
        df.withColumn(
            "price_vs_ma20",
            round(
                (
                    (col("close") - col("moving_avg_20"))
                    / col("moving_avg_20")
                ) * 100,
                2
            )
        )
    )


def calculate_daily_range(df):
    """
    Daily trading range.
    """
    logger.info("calculate_daily_range: start")
    return (
        df.withColumn(
            "daily_range_pct",
            round(
                (
                    (col("high") - col("low"))
                    / col("close")
                ) * 100,
                2
            )
        )
    )


def calculate_volatility(df):
    """
    Calculate volatility per stock.
    """
    logger.info("Calculate_volaity: start")
    volatility_df = (
        df.groupBy("symbol")
        .agg(
            round(
                stddev("close"),
                2
            ).alias("volatility")
        )
    )

    return df.join(
        volatility_df,
        on="symbol",
        how="left"
    )


def calculate_daily_return(df):
    """
    Calculate daily percentage return.
    """
    logger.info("calculate_daily_return : start")
    window_spec = (
        Window
        .partitionBy("symbol")
        .orderBy("trade_date")
    )

    return (
        df.withColumn(
            "previous_close",
            lag("close").over(window_spec)
        )
        .withColumn(
            "daily_return_pct",
            round(
                (
                    (col("close") - col("previous_close"))
                    / col("previous_close")
                ) * 100,
                2
            )
        )
    )


def calculate_momentum(df):

    logger.info("Calculate Momentum: Start")

    window_spec = (
        Window
        .partitionBy("symbol")
        .orderBy("trade_date")
    )

    result = (
        df
        .withColumn(
            "close_10d_ago",
            lag("close", 10).over(window_spec)
        )
        .withColumn(
            "momentum_10",
            round(
                (
                    (col("close") - col("close_10d_ago"))
                    / col("close_10d_ago")
                ) * 100,
                2
            )
        )
    )

    logger.info("Calculate Momentum: End")

    return result


def calculate_volume_spike(df):

    logger.info("Calculate Volume Spike: Start")

    result = (
        df.withColumn(
            "volume_spike",
            round(
                col("volume")
                /
                col("avg_volume_20"),
                2
            )
        )
    )

    logger.info("Calculate Volume Spike: End")

    return result


def calculate_rsi(df):
    """
    Calculate RSI-14.
    """

    logger.info("Calculate RSI: Start")

    window_spec = (
        Window
        .partitionBy("symbol")
        .orderBy("trade_date")
    )

    rsi_window = (
        Window
        .partitionBy("symbol")
        .orderBy("trade_date")
        .rowsBetween(-13, 0)
    )

    df = (
        df.withColumn(
            "price_change",
            col("close") - lag("close").over(window_spec)
        )
    )

    df = (
        df.withColumn(
            "gain",
            when(
                col("price_change") > 0,
                col("price_change")
            ).otherwise(0)
        )
        .withColumn(
            "loss",
            when(
                col("price_change") < 0,
                -col("price_change")
            ).otherwise(0)
        )
    )

    df = (
        df.withColumn(
            "avg_gain",
            avg("gain").over(rsi_window)
        )
        .withColumn(
            "avg_loss",
            avg("loss").over(rsi_window)
        )
    )

    df = (
        df.withColumn(
            "rs",
            col("avg_gain") / col("avg_loss")
        )
    )

    df = (
        df.withColumn(
            "rsi_14",
            round(
                100 - (
                    100 /
                    (1 + col("rs"))
                ),
                2
            )
        )
    )

    logger.info("Calculate RSI: End")

    return df


def display_results(df):
    logger.info("displaying result: start")
    logger.info(f"length of df is {df.count()}")

    (
        df.select(
            "symbol",
            "trade_date",
            "close",
            "moving_avg_3",
            "moving_avg_5",
            "moving_avg_10",
            "moving_avg_20",
            "daily_return_pct",
            "return_3d",
            "return_5d",
            "avg_volume_5",
            "avg_volume_20",
            "price_vs_ma20",
            "daily_range_pct",
            "volatility",
            "momentum_10",
            "volume_spike",
            "rsi_14",
        )
        .orderBy(
            "symbol",
            "trade_date"
        )
        .show(20, truncate=False)
    )


def save_metrics(df):
    """
    Save analytics results to PostgreSQL.
    """
    logger.info("saving metrics : start")
    # logger.info(f"total rows to be saved{len(df)}")
    (
        df.select(
            "symbol",
            "trade_date",
            "close",
            "moving_avg_3",
            "moving_avg_5",
            "moving_avg_10",
            "moving_avg_20",
            "daily_return_pct",
            "return_3d",
            "return_5d",
            "avg_volume_5",
            "avg_volume_20",
            "price_vs_ma20",
            "daily_range_pct",
            "volatility",
            "momentum_10",
            "volume_spike",
            "rsi_14",
        )
        .write
        .format("jdbc")
        .option(
            "url",
            "jdbc:postgresql://host.docker.internal:5432/stock_market_db"
        )
        .option("dbtable", "stock_metrics")
        .option("user", "postgres")
        .option("password", "postgres")
        .option("driver", "org.postgresql.Driver")
        .mode("overwrite")
        .save()
    )
    logger.info("Data saved sucessfully in the table")


def run_analytics():
    """
    Main analytics workflow.
    """
    spark = create_spark_session()

    try:
        stock_df = read_stock_data(spark)

        analytics_df = calculate_moving_averages(stock_df)
        analytics_df = calculate_daily_return(analytics_df)

        analytics_df = calculate_daily_return(analytics_df)
        analytics_df = calculate_multi_day_returns(analytics_df)

        analytics_df = calculate_volume_features(analytics_df)
        analytics_df = calculate_price_vs_ma20(analytics_df)
        analytics_df = calculate_daily_range(analytics_df)
        analytics_df = calculate_volatility(analytics_df)

        analytics_df = calculate_momentum(analytics_df)
        analytics_df = calculate_volume_spike(analytics_df)
        analytics_df = calculate_rsi(analytics_df)

        save_metrics(analytics_df)

        display_results(analytics_df)

    finally:
        spark.stop()


if __name__ == "__main__":
    run_analytics()