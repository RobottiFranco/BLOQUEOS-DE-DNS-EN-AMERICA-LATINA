import pandas as pd

def compare_files(reference_data, dataframes, reference_file):
    common_inputs = set(reference_data['input'])
    for file, df in dataframes.items():
        if file != reference_file:
            common_inputs &= set(df['input'])

    return pd.DataFrame(common_inputs, columns=["input"])