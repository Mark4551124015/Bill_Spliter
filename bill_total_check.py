
import pandas as pd
import os
from object_class import *
Root = "./bills-19"

Target_bill = "Qiu_Target_9-19.csv"

bill = pd.read_csv(os.path.join(Root,Target_bill))
total_price = 0

Mark = Patron("Mark")


for line in bill.iterrows():
    it = Item(line[1]['name'], line[1]['price'])
    quant = line[1]['quantity']
    Mark.add(it, line[1]['quantity'])

print(Mark.get_total())
    