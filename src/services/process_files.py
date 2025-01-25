import os
import pandas as pd
from src.utils.compare_files import compare_files
from src.utils.csv_utils import create_file_and_path


def process_files(directory):
    csv_files = [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith('.csv')]
    dataframes = {file: pd.read_csv(file) for file in csv_files}

    all_common_inputs = pd.DataFrame(columns=["input"])

    for file in csv_files:
        reference_data = dataframes[file]
        common_inputs = compare_files(reference_data, dataframes, file)
        all_common_inputs = pd.concat([all_common_inputs, common_inputs]).drop_duplicates().reset_index(drop=True)

    output_file = create_file_and_path(directory, "pages_no_longer_exist.csv")
    all_common_inputs.to_csv(output_file, index=False)

    return output_file


def delete_no_exist_files(directory, output_file):
    reference_df = pd.read_csv(output_file)
    reference_input = reference_df["input"]
    csv_files = [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith('.csv')]
    
    for file in csv_files:
        if os.path.abspath(file) == os.path.abspath(output_file):
            continue
        
        current_df = pd.read_csv(file)
        filtered_df = current_df[~current_df['input'].isin(reference_input)]
        filtered_df.to_csv(file, index=False)
