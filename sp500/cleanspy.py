import pandas as pd

# List of file paths
file_paths = [
    "res_12_1.csv",
    "res_12_2.csv",
    "res_12_3.csv",
    "res_12_4.csv",
]

# Read and concatenate all files
combined_df = pd.concat([pd.read_csv(file) for file in file_paths], ignore_index=True)

# Save the combined DataFrame to a new CSV file
combined_df.to_csv("res_12_comb.csv", index=False)

print("Files successfully combined and saved as 'res_12_comb.csv'")
