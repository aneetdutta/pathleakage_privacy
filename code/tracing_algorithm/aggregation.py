import os, sys
sys.path.append(os.getcwd())

import polars as pl
import numpy as np

SCENARIO_NAME = os.getenv("SCENARIO_NAME")


def aggregate_id(input_csv: str, output_file: str):
    # Read the CSV file into a Polars DataFrame
    df = pl.read_csv(input_csv)
    
    aggregated_df = (
        df.lazy()
        .group_by("id")
        .agg([
            pl.col("user_id").first().alias("user_id"),
            pl.col("protocol").first().alias("protocol"),
            pl.col("timestep").min().alias("start_timestep"),
            pl.col("timestep").max().alias("last_timestep"),
            (pl.col("timestep").max() - pl.col("timestep").min() + 1).alias("total_time"),
        ])
        .sort("start_timestep")
        .collect()
    )
    print(aggregated_df)
    
    aggregated_df.write_parquet(output_file)
    
    return aggregated_df
    
input_file = f"data/{SCENARIO_NAME}/sniffed_data_{SCENARIO_NAME}.csv"
# Output file path
output_file = f"data/{SCENARIO_NAME}/aggregated_id_{SCENARIO_NAME}.parquet"
# Run the aggregation
aggregated_id_df = aggregate_id(input_file, output_file)
    
print("Aggregate ID completed")

def aggregate_users(df: pl.DataFrame, output_file):
    # Perform the aggregation
    user_aggregation = (
        df.lazy()
        .group_by("user_id")
        .agg([
        # Unique IDs for each protocol
            pl.when(pl.col("protocol") == "LTE").then(pl.col("id")).unique().alias("lte_ids"),
            pl.when(pl.col("protocol") == "WiFi").then(pl.col("id")).unique().alias("wifi_ids"),
            pl.when(pl.col("protocol") == "Bluetooth").then(pl.col("id")).unique().alias("bluetooth_ids"),
            pl.col("id").unique().alias("ids"),

            # Start and end time for each protocol
            pl.when(pl.col("protocol") == "LTE").then(pl.col("start_timestep")).min().alias("lte_start_timestep"),
            pl.when(pl.col("protocol") == "LTE").then(pl.col("last_timestep")).max().alias("lte_end_timestep"),

            pl.when(pl.col("protocol") == "Bluetooth").then(pl.col("start_timestep")).min().alias("ble_start_timestep"),
            pl.when(pl.col("protocol") == "Bluetooth").then(pl.col("last_timestep")).max().alias("ble_end_timestep"),

            pl.when(pl.col("protocol") == "WiFi").then(pl.col("start_timestep")).min().alias("wifi_start_timestep"),
            pl.when(pl.col("protocol") == "WiFi").then(pl.col("last_timestep")).max().alias("wifi_end_timestep"),
        ])
        .with_columns([
            # Replace nulls with defaults
            pl.col("lte_ids").map_elements(lambda lst: [x for x in lst if x is not None], return_dtype=pl.List(pl.Utf8)).alias("lte_ids"),
            pl.col("wifi_ids").map_elements(lambda lst: [x for x in lst if x is not None], return_dtype=pl.List(pl.Utf8)).alias("wifi_ids"),
            pl.col("bluetooth_ids").map_elements(lambda lst: [x for x in lst if x is not None], return_dtype=pl.List(pl.Utf8)).alias("bluetooth_ids"),
            pl.col("ids").map_elements(lambda lst: [x for x in lst if x is not None], return_dtype=pl.List(pl.Utf8)).alias("ids"),
        ])
        .collect()
    )
    
    print(user_aggregation)
    user_aggregation = user_aggregation.with_columns([
        # Duration for each protocol
        (pl.col("lte_end_timestep") - pl.col("lte_start_timestep") + 1).alias("lte_duration"),
        (pl.col("ble_end_timestep") - pl.col("ble_start_timestep") + 1).alias("ble_duration"),
        (pl.col("wifi_end_timestep") - pl.col("wifi_start_timestep") + 1).alias("wifi_duration"),
    ])
    
    user_aggregation = user_aggregation.to_pandas()

# Calculate the max for the three columns while skipping NaNs
    user_aggregation['last_timestep'] = user_aggregation[["lte_end_timestep", "wifi_end_timestep", "ble_end_timestep"]].max(axis=1, skipna=True)
    user_aggregation['start_timestep'] = user_aggregation[["lte_start_timestep", "wifi_start_timestep", "ble_start_timestep"]].min(axis=1, skipna=True)
    user_aggregation['ideal_duration'] = user_aggregation['last_timestep'] - user_aggregation['start_timestep'] + 1
    print(user_aggregation)
    
    user_aggregation.to_parquet(output_file)
    
output_file = f"data/{SCENARIO_NAME}/aggregated_users_{SCENARIO_NAME}.parquet"

aggregate_users(aggregated_id_df, output_file)





