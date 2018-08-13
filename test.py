import nose
from tasks import sales_commit, commission_commit, get_total_commission
from unittest import TestCase
from unittest import mock

class TestSalesCommit(TestCase):
    def test_sales(self):
        with mock.patch('requests.post') as bmock:
            ins = bmock.return_value
            ins.json.return_value = {'foo': 'bar'}
            ins.status_code = 200
            res = sales_commit(10, 10, 10, 100)
            self.assertEqual(bmock.called, True)
            self.assertEqual(res, True)


class TestCommissionCommit(TestCase):
    def test_commission(self):
        with mock.patch('requests.post') as bmock:
            ins = bmock.return_value
            ins.json.return_value = {'foo': 'bar'}
            ins.status_code = 200
            res = commission_commit(10, 100)
            self.assertEqual(bmock.called, True)
            self.assertEqual(res, True)


class TestGetTotalCommision(TestCase):

    def test_total_commission(self):
        with mock.patch('requests.get') as bmock:
            ins = bmock.return_value
            ins.json.return_value = {'account_id': 10, 'total': 3000}
            ins.status_code = 200
            with mock.patch('requests.post') as cmock:
                ins = cmock.return_value
                ins.status_code = 200
                res = get_total_commission(10)
                self.assertEqual(bmock.called, True)
                self.assertEqual(res, False)
