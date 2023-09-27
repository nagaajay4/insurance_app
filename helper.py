import csv

def calculate_premium_logic(data):
    premium={}
    table=CSVtable('insurance_app\samplerates.csv')
    for i in range(len(table)):
        if data["member_csv"]==table[i]['member_csv'] and data['tier']==table[i]['tier']:
            age_range=table[i]['age_range'].split("-")
            if int(age_range[0]) <= int(data["age_range"]) and int(data["age_range"])<=int(age_range[1]):
                premium=table[i]
                break
    return premium

def CSVtable(file):
    table = []
    with open(file) as csvFileObj:
        reader = csv.DictReader(csvFileObj, delimiter=',', quotechar='"')
        for record in reader:
        # record is a dictionary of the csv record
            table.append(record)
    return table