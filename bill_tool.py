import pandas as pd

class Item:
    def __init__(self, name, value):
        self.name = name
        self.value = value

class Patron:
    def __init__(self, patron):
        self.role = patron
        self.cart = []
        self.driver_income = 0
        
    def add(self, item, cnt):
        self.cart.append((item, cnt))
    
    def get_total(self):
        total = 0
        for item in self.cart:
            total += item[0].value * item[1]
        return total

    def print_cart(self):
        print("Cart for ", self.role)
        for item in self.cart:
            print(item[0].name, item[0].value, item[1], end="\t")
        print("\nTotal: ", self.get_total())
            
                    
        
def check_bill(bill_path, patrons):
    who_paid = bill_path.split("/")[-1].split("_")[0]
    event = bill_path.split("/")[-1].split("_")[1]
    driver = bill_path.split("/")[-1].split("_")[2]
    date = bill_path.split("/")[-1].split("_")[3].split(".")[0]
    bill = pd.read_csv(bill_path)
    total_price = 0
    driver_fee=0

    for line in bill.iterrows():
        item = Item(line[1]['name'], line[1]['price'])
        member = line[1]['member']
        
        quantity = line[1]['quantity']
        
        total_price += line[1]['price']*line[1]['quantity']
        
        members=member.split("&")
        for i in range(len(members)):
            members[i]=members[i].strip()
        if len(members)==1 and members[0] == 'All':
            for mem in patrons:
                # if mem == 'Qiu': continue
                patrons[mem].add(item, quantity/(len(patrons)))
        elif len(members)==1 and members[0] == "None":
            pass
        else:
            for mem in members:
                patrons[mem].add(item, quantity/len(members))
        if item.name == "DriverFee":
            driver_fee=item.value
            patrons[driver].driver_income+=driver_fee
    
    return {
        'total_price': total_price,
        'patrons': patrons,
        'paid': who_paid,
        'event': event,
        'date': date,
        'driver': driver,
        'driver_fee': driver_fee
    }

def reductMap(payMap):
    for i in payMap.nodes():
        for j in payMap.nodes():
                if payMap.has_edge(i, j) and payMap.has_edge(j, i):
                    if payMap[i][j]['weight'] > payMap[j][i]['weight']:
                        payMap[i][j]['weight'] -= payMap[j][i]['weight']
                        payMap.remove_edge(j, i)
                    elif payMap[i][j]['weight'] < payMap[j][i]['weight']:
                        payMap[j][i]['weight'] -= payMap[i][j]['weight']
                        payMap.remove_edge(i, j)
                    else:
                        payMap.remove_edge(i, j)
                        payMap.remove_edge(j, i)

def printMap(payMap):
    for i in payMap.nodes():
        for j in payMap.nodes():
            if payMap.has_edge(i, j):
                money = payMap[i][j]['weight']
                if money > 0:
                    print(i, "should give", j, round(money,2))