from load_readings import get_readings
from dateutil.parser import parse
import pytz
from tariff import BULB_TARIFF
import operator


def extract_days(bill_date):
    """
    Extract days will minus one month from the given date and return the
    number of days.

    bill_date (datetime) :: datetime object of the bill_date.

    return (int) :: returns numbers of days as integer of 'bill_date - 1 month'.
    """

    if bill_date.month == 1:
        previous_date = 12
    else:
        previous_date = bill_date.month - 1

    diff = bill_date - bill_date.replace(month=previous_date)
    return int(diff.days)


def bill_finder(data, bill_date):
    """
    bill finder will calculate for 'gas' and 'electric' utils
    the kwh estimate using the last two previous bills from the bill_date.
    and return kwh and the amount of charge for the last month based on kwh.


     data (dict):: A dict of list of bills from specific utility saved as dictionaries.
     bill_date (datetime)  :: bill date period that has been entered.

     return :: amount, kwh
    """

    if 'electricity' in data:
        bill_type = 'electricity'
    elif 'gas' in data:
        bill_type = 'gas'
    else:
        raise ValueError('bill type is not of gas or electricity')

    bill_readings = {}
    for reading in data[bill_type]:
        if parse(reading['readingDate']) <= bill_date:
            bill_readings[reading['readingDate']] = reading['cumulative']

    sorted_keys = sorted(bill_readings.keys(), reverse=True)

    kwh = bill_readings[sorted_keys[0]] - bill_readings[sorted_keys[1]]
    SC = BULB_TARIFF[bill_type]['standing_charge'] * float(extract_days(bill_date))

    units = kwh * BULB_TARIFF[bill_type]['unit_rate']

    return (SC+units)/100, kwh


def calculate_bill(member_id, account_id, bill_date):
    """
    calculate will take member_id information and return a tuple of amound charged and the estimated
    usage in kwh

    member_id (str): membership number of bulb user.
    account_id (str): specific account_id of bulb user. can be Blank, All or specific.
    bill_date (str): the date the customer wishes to calculate their bill to.

    return (tuple) :: amount in £ and the estimated amount of utility used in kwh.
    """

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
                    charges = tuple(map(operator.add, charges, bill_finder(util_type, bill_date)))
    else:
        for accounts in readings:
            if account_id in accounts:
                for util_type in accounts[account_id]:
                    charges = tuple(map(operator.add, charges, bill_finder(util_type, bill_date)))

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
