import csv
import os
from pathlib import Path
from django.db import models
from django.core.management.base import BaseCommand, CommandError

from shopping_web.models import product

class Command(BaseCommand):
    help = 'Load data from csv'

    def handle(self, *args, **options):

        # drop the data from the table so that if we rerun the file, we don't repeat values
        product.objects.all().delete()
        print("table dropped successfully")
        # create table again

        # open the file to read it into the database
        base_dir = Path(__file__).resolve().parent.parent.parent.parent
        with open(str(base_dir) + '/shopping_web/data/fashion.csv', newline='') as f:
            reader = csv.reader(f, delimiter=",")
            next(reader) # skip the header line
            for row in reader:
                print(row)

                Product = product.objects.create(
                productId = int(row[0]),
                gender = row[1],
                category = row[2],
                subCategory = row[3],
                productType = row[4],
                colour = row[5],
                usage = row[6],
                producttitle=row[7],
                image=row[8],
                imageURL=row[9]
                )
                Product.save()
        print("data parsed successfully")