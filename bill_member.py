from load_readings import get_readings
from dateutil.parser import parse
import pytz
from tariff import BULB_TARIFF



def calc_ashik(member_id, account_id,bill_date=None):
    utc = pytz.UTC
    readings = get_readings()
    readings = readings[member_id]
    bill_date = parse(bill_date)
    bill_date = utc.localize(bill_date)

    latest_reading =[]


    for accounts in readings:
        if account_id in accounts:
            for util_type in accounts[account_id]:
                if 'electricity' in util_type:
                    for reading in util_type['electricity']:
                        if parse(reading['readingDate']) <= bill_date:
                            latest_reading.append(reading)

                    latest_reading = latest_reading[len(latest_reading)-2:]

                    kwh = latest_reading[1]['cumulative'] - latest_reading[0]['cumulative']
                    SC = BULB_TARIFF['electricity']['standing_charge'] * float(bill_date.strftime('%d'))
                    units = kwh * BULB_TARIFF['electricity']['unit_rate']
                    print((SC+units)/100)









calc_ashik('member-123','account-abc', '2017-08-31')
#
def calculate_bill(member_id, account_id, bill_date):
    # TODO REFACTOR ME :)
    if (member_id == 'member-123' and
        account_id == 'ALL' and
            bill_date == '2017-08-31'):
        amount = 27.57
        kwh = 167
    else:
        amount = 0.
        kwh = 0


    return amount, kwh


def calculate_and_print_bill(member_id, account, bill_date):
    """Calculate the bill and then print it to screen.
    Account is an optional argument - I could bill for one account or many.
    There's no need to refactor this function."""
    member_id = member_id or 'member-123'
    bill_date = bill_date or '2017-08-31'
    account = account or 'ALL'
    amount, kwh = calculate_bill(member_id, account, bill_date)
    print('Hello {member}!'.format(member=member_id))
    print('Your bill for {account} on {date} is £{amount}'.format(
        account=account,
        date=bill_date,
        amount=amount))
    print('based on {kwh}kWh of usage in the last month'.format(kwh=kwh))
