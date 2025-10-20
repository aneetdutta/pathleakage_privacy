import os, sys
from typing import Iterable

import numpy as np

sys.path.append(os.getcwd())

from modules.logger import MyLogger
from shapely.geometry import Polygon, Point
import csv

SCENARIO_NAME = os.getenv("SCENARIO_NAME")
POLYGON_COORDS = eval(os.getenv("POLYGON_COORDS"))

ml = MyLogger(f"filter_user_polygon_{SCENARIO_NAME}")
INPUT_CSV_PATH = f"data/raw_user_data_{SCENARIO_NAME}.csv"
OUTPUT_CSV_PATH = f"data/raw_user_data_filter_polygon_{SCENARIO_NAME}.csv"
chunk_size = 10000
polygon = Polygon(POLYGON_COORDS)

""" If not person id , save the person id and discard if visited next time"""
visited_person = set()

# Open the CSV file and read row by row
# Batch write rows for efficiency
batch_size = 10000
batch = []

import pandas


def process_piece(pieces: pandas.DataFrame) -> list[pandas.Series]:
    seen_users = set()
    chosen = []

    for piece in pieces.itertuples(index=False):
        user_id = piece[1]
        x, y = piece[2:]

        if user_id in seen_users:
            continue

        point = Point(x, y)

        # skip if point not inside the given polygon
        if not polygon.contains(point):
            seen_users.add(user_id)
            continue

        chosen.append((piece[0], piece[1], piece[2], piece[3]))

    return chosen


def save_results(filename: str, headers: list[str], records: Iterable[tuple[int, str, float, float]]):
    with open(filename, mode='w', newline='') as csv_output:
        writer = csv.writer(csv_output, delimiter=',')
        writer.writerow(headers)

        for record in records:
            writer.writerow(record)


def main():
    # load sources
    print("loading sources...")
    sources = pandas.read_csv(INPUT_CSV_PATH,
                              dtype={'timestep': np.int16, 'user_id': str, 'loc_x': np.float32,
                                     'loc_y': np.float32})

    # chunk the sources for parallel processing
    parallelism = 10

    chunk_len = int(len(sources) / parallelism)
    chunks = [sources[i:i + chunk_len] for i in range(0, len(sources), chunk_len)]

    total_chunked_len = sum(map(len, chunks))
    assert total_chunked_len == len(sources)
    # if total_chunked_len < len(sources):
    #     chunks[-1].extend(sources[total_chunked_len:])

    # create the pool and start parallel processing
    from multiprocessing import Pool
    with Pool(parallelism) as pool:
        print("processing sources...")
        results = pool.map(process_piece, chunks)

    save_results(OUTPUT_CSV_PATH,
                 ['timestep', 'user_id', 'loc_x', 'loc_y'],
                 (rr for r in results for rr in r))


def old_main():
    import pandas as pd

    print("loading raw data...")

    source = pd.read_csv(INPUT_CSV_PATH)[:100040]
    output = []

    print("filtering users based on provided polygon...")

    count = 0
    for row in source.itertuples(index=False):
        if count % batch_size == 0:
            print(f"Processed {count} rows...")
        count += 1

        try:
            # Extract user ID and coordinates
            user_id = row[1]
            if user_id in visited_person:
                continue

            loc_x = row[2]
            loc_y = row[3]
            point = Point(loc_x, loc_y)

            # Skip if the point is not inside the polygon
            if not polygon.contains(point):
                visited_person.add(user_id)
                continue

            # Add to batch
            output.append(row)

        except ValueError:
            print(f"Skipping row due to invalid data: {row}")

    output_df = pd.DataFrame(output)
    output_df.to_csv(OUTPUT_CSV_PATH, index=False)

# with open(INPUT_CSV_PATH, "r", encoding="utf-8") as input_csv, \
#         open(OUTPUT_CSV_PATH, "w", encoding="utf-8", newline="") as output_csv:
#     reader = csv.reader(input_csv)
#     writer = csv.writer(output_csv)
#
#     # Copy the header row to the new CSV
#     header = next(reader)
#     writer.writerow(header)
#
#     # Process each row
#     for i, row in enumerate(reader, start=1):
#         # print("Aneet")
#         if i % 10000 == 0:
#             print(f"Processed {i} rows...")
#
#         try:
#             # Extract user ID and coordinates
#             user_id = str(row[1])
#             if user_id in visited_person:
#                 continue
#
#             loc_x = float(row[2])
#             loc_y = float(row[3])
#             point = Point(loc_x, loc_y)
#
#             # Skip if the point is not inside the polygon
#             if not polygon.contains(point):
#                 visited_person.add(user_id)
#                 continue
#
#             # Add to batch
#             batch.append(row)
#
#             # Write batch to the output CSV
#             if len(batch) >= batch_size:
#                 writer.writerows(batch)
#                 batch = []
#
#         except ValueError:
#             print(f"Skipping row due to invalid data: {row}")
#
#     # Write any remaining rows in the batch
#     if batch:
#         writer.writerows(batch)
#
# print("Processing complete!")
