from load_readings import get_readings
from dateutil.parser import parse
import pytz
from tariff import BULB_TARIFF
import operator




def bill_finder(data, bill_date, type):

    bill_readings = {}
    for reading in data[type]:
        if parse(reading['readingDate']) <= bill_date:
            bill_readings[reading['readingDate']] = reading['cumulative']

    sorted_keys = sorted(bill_readings.keys(), reverse=True)

    kwh = bill_readings[sorted_keys[0]] - bill_readings[sorted_keys[1]]
    SC = BULB_TARIFF[type]['standing_charge'] * float(bill_date.strftime('%d'))
    units = kwh * BULB_TARIFF[type]['unit_rate']

    return (SC+units)/100, kwh




def calculate_bill(member_id, account_id, bill_date):
    utc = pytz.UTC
    readings = get_readings()
    readings = readings[member_id]
    bill_date = parse(bill_date)
    bill_date = utc.localize(bill_date)
    charges = (0, 0)


    if account_id == 'ALL' or account_id is None:
        for accounts in readings:
            for account in accounts:
                for util_type in accounts[account]:
                    if 'electricity' in util_type:
                        elect_charge = bill_finder(util_type, bill_date, 'electricity')
                        charges = tuple(map(operator.add, charges, elect_charge))

                    if 'gas' in util_type:
                        gas_charge = bill_finder(util_type, bill_date, 'gas')
                        charges = tuple(map(operator.add, charges, gas_charge))


    else:
        for accounts in readings:
            if account_id in accounts:
                for util_type in accounts[account_id]:
                    if 'electricity' in util_type:
                        elect_charge = bill_finder(util_type, bill_date, 'electricity')
                        charges = tuple(map(operator.add, charges, elect_charge))

                    if 'gas' in util_type:
                        gas_charge = bill_finder(util_type, bill_date, 'gas')
                        charges = tuple(map(operator.add, charges, gas_charge))


    return float("{0:.2f}".format(charges[0])), charges[1]









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
