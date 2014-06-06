import csv

outfile = open('output-debug-schema-with-ratios-and-comments.csv', 'w')
writer = csv.writer(outfile)
infile = open('output-debug-with-ratios-and-comments.csv', 'rbU')
reader2 = csv.reader(infile)

with open('output-debug-schema-with-ratios.csv', 'rbU') as f:
  reader = csv.reader(f)
  first_row = next(reader)
  writer.writerow(first_row)
  #next(reader2)
  for row in reader:
    row2 = next(reader2)
    if row[2]!='' and float(row[2]) < 25:
      row.append('TRUE')
    else:
      row.append('')
    if row2[7]:
      row.append(row2[7])
    if row2[8]:
      row.append(row2[8])
    if row2[9]:
      row.append(row2[9])
    if row2[10]:
      row.append(row2[10])
    writer.writerow(row)