import os
import sys
from config.env_config import setup_env
from etl.extract.extract import extract_data
from etl.transform.transform import transform_data
from etl.load.load import load_data
import time


def main():
    start_time = time.time()
    run_env_setup()

    print("Extracting data...")
    extract_data()
    print("Data extraction complete.")

    print("Transforming data...")
    transform_data()
    print("Data transformation complete.")

    print("Loading data...")
    load_data()
    print("Data loading complete.")

    end_time = time.time()
    elapsed_time = round(end_time - start_time, 2)

    print(f"ETL run completed in {elapsed_time} seconds")

    print(
        f"ETL pipeline run successfully in "
        f'{os.getenv("ENV", "error")} environment!'
    )


def run_env_setup():
    print("Setting up environment...")
    setup_env(sys.argv)
    print("Environment setup complete.")


if __name__ == "__main__":
    main()
