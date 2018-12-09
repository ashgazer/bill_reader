import datetime
import unittest

from bill_member import calculate_bill, extract_days


class TestBillMember(unittest.TestCase):

    def test_calculate_bill_for_august(self):
        amount, kwh = calculate_bill(member_id='member-123',
                                     account_id='ALL',
                                     bill_date='2017-08-31')
        self.assertEqual(amount, 27.57)
        self.assertEqual(kwh, 167)


    def test_extract_days(self):
        date_to_test = datetime.datetime(2017, 8, 31, 0, 0)
        days = extract_days(date_to_test)
        self.assertAlmostEquals(days,31)

if __name__ == '__main__':
    unittest.main()
