# import csv 

# with open('pomiary.csv', newline='') as csvfile:
#     spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
#     for row in spamreader:
#         print(', '.join(row))

#     rows =[]
#     for row in spamreader:
#         rows.append(row)
#     print(rows)


import csv
rows = []
with open("pomiary.csv", 'r') as file:
    csvreader = csv.reader(file)
    header = next(csvreader)
    for row in csvreader:
        rows.append(row)
print(header)
print(rows[1])