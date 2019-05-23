#!/usr/bin/env python3

"""
Wenlong Xiong (2019)

This script generates BERT training examples from patient history records.

It takes 2 arguments, the name of the file containing a CSV of patient history records, and the output file name.

The input file should be a CSV that has the following columns:
    [SUBJECT_ID] [HADM_ID] [CHARTTIME] [TEXT] [LABELS]

The input file is 
    /u/scratch/d/datduong/MIMIC3database/format10Jan2019/disch_full_correct_icd.csv

The output file is a "document", with unique patients grouped in "paragraphs". Each visit is recorded as a single "sentence", one per line. Consecutive visits are listed on the following lines. Between different patient paragraphs, there is an empty line to separate them.
"""

import sys
import pandas as pd
import numpy as np


if __name__ == "__main__":
    
    # argument check
    if len(sys.argv) < 3:
        print("Please call this script with 2 arguments: [input_file_name] [output_file_name]")
        exit()

    input_file = str(sys.argv[1])
    output_file = str(sys.argv[2])

    # Read input into a pandas dataframe
    df = pd.read_csv(input_file)

    # Drop rows when the visit had no codes
    df = df.dropna(subset=["LABELS"])

    # Limit the subjects to those that have more than 2 patient visits
    subject_ids, subject_counts = np.unique(list(df["SUBJECT_ID"]), return_counts=True)
    subject_counts = np.array(subject_counts)
    truncated_ids = np.array(subject_ids)[subject_counts > 2]
    df = df[df["SUBJECT_ID"].isin(truncated_ids)]

    with open(output_file, "w") as f:
        sequences = {}
        current_subject = df.iloc[0]["SUBJECT_ID"]
        for _, row in df.iterrows():
            # Consider a single patient a "document"
            if current_subject != row["SUBJECT_ID"]:
                current_subject = row["SUBJECT_ID"]
                f.write("\n")

            line = " ".join(row["LABELS"].split(";"))
            f.write(line + "\n")

    # Success

