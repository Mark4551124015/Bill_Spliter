
import pandas as pd
import os
from bill_tool import *
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-f", "--file", help="The file to be read", required=True)

args = parser.parse_args()

Target_bill = args.file

bill = pd.read_csv(Target_bill)
total_price = 0

Mark = Patron("Mark")


for line in bill.iterrows():
    if line[1]['name'] == "DriverFee":
        print("Driver Fee: ", line[1]['price'])
        continue
    it = Item(line[1]['name'], line[1]['price'])
    quant = line[1]['quantity']
    Mark.add(it, line[1]['quantity'])

print(round(Mark.get_total(), 2))
    