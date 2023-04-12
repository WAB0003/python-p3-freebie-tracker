#!/usr/bin/env python3

# from sqlalchemy import create_engine

# from models import Company, Dev, Freebies

from freebie import Freebie
from company import Company
from dev import Dev

#! Drop all tables when first started to see if it works:
Company.drop_table()
Dev.drop_table()
Freebie.drop_table()

#! Create all (3) tables to exist in the database:
Company.create_table()
Dev.create_table()
Freebie.create_table()


#! Create some dev instances
ollie = Dev("ollie")
ollie.save()
wally = Dev("Wally")
wally.save()
bill = Dev("Bill")
bill.save()

#! Create some company instances

docusign = Company("DocuSign", 1999)
docusign.save()
gitHub = Company("GitHub", 2002)
gitHub.save()
walmart = Company("Walmart", 1804)
walmart.save()

#! Create some Freebie instances
koozie = Freebie("Koozie", 10, gitHub.id, bill.id)
koozie.save()
hat = Freebie("Hat", 20, gitHub.id, wally.id)
hat.save()
pen = Freebie("Pen", 1, docusign.id, bill.id)
pen.save()









if __name__ == '__main__':
    # engine = create_engine('sqlite:///freebies.db')
    import ipdb; ipdb.set_trace()
