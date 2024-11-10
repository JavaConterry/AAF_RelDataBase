import unittest
from db import DataBase


class DataBaseTest(unittest.TestCase):
    
    def test_btree_search_1level_eq_indexed_1(self):
        db = DataBase()
        db.do([['CREATE', 'table'], [['name', False], ['age', True]]])
        db.do([['INSERT', 'table'], ['Max Verstappen', '27']])
        db.do([['INSERT', 'table'], ['Charles Leclerc', '27']])
        db.do([['INSERT', 'table'], ['Lewis Hamilton', '39']])
        responce = db.do([['SELECT', 'table'], ['age', '27', '=']])
        self.assertEqual(responce, [['Max Verstappen', '27'], ['Charles Leclerc', '27']])
    
    def test_btree_search_1level_eq_indexed_2(self):
        db = DataBase()
        db.do([['CREATE', 'table'], [['race', True], ['winner', True]]])
        db.do([['INSERT', 'table'], ['Brazil','Verstappen']])
        db.do([['INSERT', 'table'], ['Mexico', 'Sainz']])
        db.do([['INSERT', 'table'], ['United States', 'Leclerc']])
        db.do([['INSERT', 'table'], ['Belgium', 'Hamilton']])
        db.do([['INSERT', 'table'], ['Great Britain', 'Hamilton']])
        db.do([['INSERT', 'table'], ['Spain', 'Verstappen']])
        db.do([['INSERT', 'table'], ['Canada', 'Verstappen']])
        responce = db.do([['SELECT', 'table'], ['winner', 'Verstappen', '=']])
        self.assertEqual(responce, [['Brazil','Verstappen'], ['Spain', 'Verstappen'],  ['Canada', 'Verstappen']])
    
    def test_btree_search_1level_eq_not_indexed(self):
        db = DataBase()
        db.do([['CREATE', 'table'], [['name', False], ['age', True], ['team', False]]])
        db.do([['INSERT', 'table'], ['Max Verstappen', '27', 'ORBR']])
        db.do([['INSERT', 'table'], ['Charles Leclerc', '27', 'Ferrari']])
        db.do([['INSERT', 'table'], ['Carlos Sainz', '30', 'Ferrari']])
        db.do([['INSERT', 'table'], ['Lewis Hamilton', '39', 'Mercedes']])
        responce = db.do([['SELECT', 'table'], ['team', 'Ferrari', '=']])
        self.assertEqual(responce, [['Charles Leclerc', '27', 'Ferrari'],  ['Carlos Sainz', '30', 'Ferrari']])
    
    def test_btree_search_1level_uneq_indexed_1(self):
        db = DataBase()
        db.do([['CREATE', 'table'], [['name', False], ['age', True]]])
        db.do([['INSERT', 'table'], ['Max Verstappen', '27']])
        db.do([['INSERT', 'table'], ['Charles Leclerc', '27']])
        db.do([['INSERT', 'table'],  ['Pierre Gasly', '28']])
        db.do([['INSERT', 'table'], ['Lewis Hamilton', '39']])
        responce = db.do([['SELECT', 'table'], ['age', '27', '>']])
        self.assertEqual(responce, [ ['Pierre Gasly', '28'], ['Lewis Hamilton', '39']])
    
    def test_btree_search_1level_uneq_indexed_2(self):
        db = DataBase()
        db.do([['CREATE', 'table'], [['name', False], ['age', True]]])
        db.do([['INSERT', 'table'], ['Max Verstappen', '27']])
        db.do([['INSERT', 'table'], ['Charles Leclerc', '27']])
        db.do([['INSERT', 'table'],  ['Pierre Gasly', '28']])
        db.do([['INSERT', 'table'], ['Lewis Hamilton', '39']])
        responce = db.do([['SELECT', 'table'], ['age', '39', '<']])
        self.assertEqual(responce, [['Max Verstappen', '27'], ['Charles Leclerc', '27'],  ['Pierre Gasly', '28']])

    def test_btree_search_1level_uneq_not_indexed(self):
        db = DataBase()
        db.do([['CREATE', 'table'], [['name', False], ['age', False], ['team', False]]])
        db.do([['INSERT', 'table'], ['Max Verstappen', '27', 'ORBR']])
        db.do([['INSERT', 'table'], ['Charles Leclerc', '27', 'Ferrari']])
        db.do([['INSERT', 'table'], ['Carlos Sainz', '30', 'Ferrari']])
        db.do([['INSERT', 'table'], ['Lewis Hamilton', '39', 'Mercedes']])
        responce = db.do([['SELECT', 'table'], ['team', 'Ferrari', '=']])
        self.assertEqual(responce, [['Charles Leclerc', '27', 'Ferrari'],  ['Carlos Sainz', '30', 'Ferrari']])
    

if __name__ == '__main__':
    unittest.main()