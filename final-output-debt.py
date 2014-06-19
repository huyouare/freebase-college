import csv

# Master
master_ipeds = set()
master_ipeds_dict = dict()

with open('master-matching.csv', 'rU') as csvfile:
  reader = csv.reader(csvfile)
  next(reader, None)
  for row in reader:
    master_ipeds.add(int(row[0]))
    master_ipeds_dict[int(row[0])] = row

outfile = open('final-output-vs-master-matching.csv', 'w')
writer = csv.writer(outfile)

# vs output-final
accred_colleges = set()
accred_rows = dict()

with open('output-final.csv', 'rU') as csvfile:
  reader = csv.reader(csvfile)
  for row in reader:
    new_row = row
    if (row[2] != '') and (row[2] != 'ipeds_id') and (int(row[2]) in master_ipeds):
      new_row = new_row + master_ipeds_dict[int(row[2])]
    writer.writerow(new_row)