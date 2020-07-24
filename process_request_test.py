import unittest
from process_request import RequestApartments


class TestProcessRequest(unittest.TestCase):

    def test_process_request(self):

        addr = input("Please enter the query address: ")
        r = RequestApartments()
        parsed_data = r.run(addr)
        self.assertGreater(len(parsed_data), 0)
        parsed_data = r.run(addr)
        self.assertEqual(len(parsed_data), 0)


if __name__ == '__main__':
    unittest.main()
