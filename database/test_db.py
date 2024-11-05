import unittest
from db import DataBase


class DataBaseTest(unittest.TestCase):
    
    def test_btree_search_1level_eq_indexed(self):
        db = DataBase()
        db.do([['CREATE', 'table'], [['name', False], ['age', True]]])
        db.do([['INSERT', 'table'], ['Max Verstappen', '27']])
        db.do([['INSERT', 'table'], ['Charles Leclerc', '27']])
        db.do([['INSERT', 'table'], ['Lewis Hamilton', '39']])
        responce = db.do([['SELECT', 'table'], ['age', '27', '=']])
        print(responce)
        self.assertEqual(responce, [['Max Verstappen', '27'], ['Charles Leclerc', '27']])
    
    def test_btree_search_1level_eq_2_not_indexed(self):
        db = DataBase()
        db.do([['CREATE', 'table'], [['name', False], ['age', True]]])
        db.do([['INSERT', 'table'], ['Max Verstappen', '27']])
        db.do([['INSERT', 'table'], ['Charles Leclerc', '27']])
        db.do([['INSERT', 'table'], ['Charles Leclerc', '28']])
        db.do([['INSERT', 'table'], ['Lewis Hamilton', '39']])
        responce = db.do([['SELECT', 'table'], ['name', 'Charles Leclerc', '=']])
        print(responce)
        self.assertEqual(responce, [['Charles Leclerc', '27'], ['Charles Leclerc', '28']])
    


if __name__ == "__main__":
    unittest.main()
