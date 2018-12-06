import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", 'stock_market.settings')



import django
django.setup()

from stock_info.models import StockInfo
from faker import Faker

fakegen = Faker()

def populate(N):

    for entry in range (N):
        fake_symbol = fakegen.company_suffix().upper()
        fake_date = fakegen.date(pattern="%Y-%m-%d", end_datetime=None)
        fake_high = fakegen.pyfloat(left_digits=3, right_digits=3, positive=True)
        fake_low = fakegen.pyfloat(left_digits=3, right_digits=3, positive=True)
        fake_open = fakegen.pyfloat(left_digits=3, right_digits=3, positive=True)
        fake_close = fakegen.pyfloat(left_digits=3, right_digits=3, positive=True)
        fake_volume = fakegen.pyint()
        fake_adj_close = fakegen.pyfloat(left_digits=3, right_digits=3, positive=True)

        stock_data = StockInfo.objects.get_or_create (symbol = fake_symbol, date = fake_date,
                                           high = fake_high, low = fake_low,
                                           open = fake_open, close = fake_close,
                                            volume = fake_volume, adj_close = fake_adj_close) [0]


if __name__ == '__main__':
    print("populating data")
    populate(5)
    print("Done")


