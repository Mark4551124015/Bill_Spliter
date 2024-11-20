from bill_tool import *
from glob import glob
import networkx as nx
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-r", "--root", help="The root directory of the bills", required=True)


Member = ["Qiu", "Feng", "Li", "Xiao", "Zhou", "Hu"]
patrons = {}
for key in Member:
    patrons[key] = Patron(key)


def split(bill_path):
    payMap = nx.DiGraph()
    memPaid = {}
    for key in Member:
        memPaid[key] = 0.
    
    bills = glob(bill_path+'/*.csv')
    for index, bill_path in enumerate(bills):
        print(f"+++++++++++ Bill {index+1} +++++++++++")
        bill = check_bill(bill_path, patrons)
        summation = round(bill['total_price'], 2)
        payer = bill['paid']
        driver = bill['driver']
        print("The bill is paid by:", payer, "at", bill['event'], "on", bill['date'])
        if driver in Member:
            print("The driver is:", driver)
        else:
            print("There is no Driver")
        print("Summation of the bill is: ", summation)
        memPaid[payer] += summation
        for man in Member:
            patron = patrons[man]
            dollar = patron.get_total()
            if dollar > 0:
                print(man+"'s bill is: ", round(dollar,2))
            if payer == man: continue
            payMap.add_edge(man, payer, weight=dollar)
    
    print("\n==================== Summary ================")
    for mem in memPaid:
        if memPaid[mem] > 0:
            print(mem, "paid: ", round(memPaid[mem],2))
        
    for mem in Member:
        if patrons[mem].driver_income > 0:
            print(mem, "earned driver fee: ", round(patrons[mem].driver_income,2))
    reductMap(payMap)
    printMap(payMap)
    print("=============================================")

    
if __name__ == "__main__":
    args = parser.parse_args()

    split(args.root)