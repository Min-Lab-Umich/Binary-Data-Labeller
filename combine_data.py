import os
import sys
import glob
import pandas as pd
import csv
from pathlib import Path
import shutil


all_csv = [f"data/{i}/labels.csv" for i in range(1, 13)]
with open('labelled_data/labels.csv', 'w') as output:
    output_writer = csv.writer(output)
    for a_csv in all_csv:
        with open(a_csv, 'r') as from_csv:
            reader = csv.reader(from_csv)
            for row in reader:
                output_writer.writerow(row)


for i in range(1, 13):
    for src_file in Path(f"data/{i}").glob('*.png'):
        shutil.copy(src_file, "labelled_data/")
