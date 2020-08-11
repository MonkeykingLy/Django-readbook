import csv
from readbook.backed.models import *

path='data.csv'
f=open(path)
reader=csv.reader(f)
for row in reader:
    Book.objects.update_or_create(id=row[0],title=row[1],authors=row[2],publisher=row[3],publish_date=row[4],page_count=row[5],categories=row[6],ISBN=row[7],imageLink=row[8],description=row[9])