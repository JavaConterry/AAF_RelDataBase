import unittest
from database.db import DataBase


class DataBaseTest(unittest.TestCase):

    def test_btree_search_1level_eq_indexed_1(self):
        db = DataBase()
        db.do([['CREATE', 'table'], [['name', False], ['age', True]]])
        db.do([['INSERT', 'table'], ['Max Verstappen', '27']])
        db.do([['INSERT', 'table'], ['Charles Leclerc', '27']])
        db.do([['INSERT', 'table'], ['Lewis Hamilton', '39']])
        responce = db.do([['SELECT', 'table'], ['=', 'age', '27']])
        self.assertEqual(responce.data, [['Max Verstappen', '27'], ['Charles Leclerc', '27']])

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
        responce = db.do([['SELECT', 'table'], ['=', 'winner', 'Verstappen']])
        self.assertEqual(responce.data, [['Brazil','Verstappen'], ['Spain', 'Verstappen'],  ['Canada', 'Verstappen']])

    def test_btree_search_1level_eq_not_indexed(self):
        db = DataBase()
        db.do([['CREATE', 'table'], [['name', False], ['age', True], ['team', False]]])
        db.do([['INSERT', 'table'], ['Max Verstappen', '27', 'ORBR']])
        db.do([['INSERT', 'table'], ['Charles Leclerc', '27', 'Ferrari']])
        db.do([['INSERT', 'table'], ['Carlos Sainz', '30', 'Ferrari']])
        db.do([['INSERT', 'table'], ['Lewis Hamilton', '39', 'Mercedes']])
        responce = db.do([['SELECT', 'table'], ['=', 'team', 'Ferrari']])
        self.assertEqual(responce.data, [['Charles Leclerc', '27', 'Ferrari'],  ['Carlos Sainz', '30', 'Ferrari']])

    def test_btree_search_1level_uneq_indexed_1(self):
        db = DataBase()
        db.do([['CREATE', 'table'], [['name', False], ['age', True]]])
        db.do([['INSERT', 'table'], ['Max Verstappen', '27']])
        db.do([['INSERT', 'table'], ['Charles Leclerc', '27']])
        db.do([['INSERT', 'table'],  ['Pierre Gasly', '28']])
        db.do([['INSERT', 'table'], ['Lewis Hamilton', '39']])
        responce = db.do([['SELECT', 'table'], [ '>', 'age', '27']])
        self.assertEqual(responce.data, [ ['Pierre Gasly', '28'], ['Lewis Hamilton', '39']])

    def test_btree_search_1level_uneq_indexed_2(self):
        db = DataBase()
        db.do([['CREATE', 'table'], [['name', False], ['age', True]]])
        db.do([['INSERT', 'table'], ['Max Verstappen', '27']])
        db.do([['INSERT', 'table'], ['Charles Leclerc', '27']])
        db.do([['INSERT', 'table'],  ['Pierre Gasly', '28']])
        db.do([['INSERT', 'table'], ['Lewis Hamilton', '39']])
        responce = db.do([['SELECT', 'table'], ['<', 'age', '39']])
        self.assertEqual(responce.data, [['Max Verstappen', '27'], ['Charles Leclerc', '27'],  ['Pierre Gasly', '28']])

    def test_btree_search_1level_uneq_indexed_3(self):
        db = DataBase()
        db.do([['CREATE', 'table'], [['name', False], ['age', True]]])
        db.do([['INSERT', 'table'], ['Max Verstappen', '27']])
        db.do([['INSERT', 'table'], ['Charles Leclerc', '27']])
        db.do([['INSERT', 'table'],  ['Pierre Gasly', '28']])
        db.do([['INSERT', 'table'], ['Lewis Hamilton', '39']])
        responce = db.do([['SELECT', 'table'], ['<', 'name', 'Max Verstappen']])
        self.assertEqual(responce.data, [['Charles Leclerc', '27'],  ['Lewis Hamilton', '39']])

    def test_btree_search_1level_uneq_not_indexed(self):
        db = DataBase()
        db.do([['CREATE', 'table'], [['name', False], ['age', False], ['team', False]]])
        db.do([['INSERT', 'table'], ['Max Verstappen', '27', 'ORBR']])
        db.do([['INSERT', 'table'], ['Charles Leclerc', '27', 'Ferrari']])
        db.do([['INSERT', 'table'], ['Carlos Sainz', '30', 'Ferrari']])
        db.do([['INSERT', 'table'], ['Lewis Hamilton', '39', 'Mercedes']])
        responce = db.do([['SELECT', 'table'], ['=', 'team', 'Ferrari']])
        self.assertEqual(responce.data, [['Charles Leclerc', '27', 'Ferrari'],  ['Carlos Sainz', '30', 'Ferrari']])

    def test_select_2level_not_indexed_1(self):
        db = DataBase()
        db.do([['CREATE', 'table'], [['name', False], ['age', False], ['team', False]]])
        db.do([['INSERT', 'table'], ['Max Verstappen', '27', 'ORBR']])
        db.do([['INSERT', 'table'], ['Charles Leclerc', '27', 'Ferrari']])
        db.do([['INSERT', 'table'], ['Carlos Sainz', '30', 'Ferrari']])
        db.do([['INSERT', 'table'], ['Lewis Hamilton', '39', 'Mercedes']])
        responce = db.do([['SELECT', 'table'], ['OR', ['=', 'team', 'Ferrari'], ['=', 'team', 'Mercedes']]])
        self.assertEqual(responce.data, [['Charles Leclerc', '27', 'Ferrari'],  ['Carlos Sainz', '30', 'Ferrari'], ['Lewis Hamilton', '39', 'Mercedes']])

    def test_select_2level_not_indexed_2(self):
        db = DataBase()
        db.do([['CREATE', 'table'], [['name', False], ['age', False], ['team', False]]])
        db.do([['INSERT', 'table'], ['Max Verstappen', '27', 'ORBR']])
        db.do([['INSERT', 'table'], ['Charles Leclerc', '27', 'Ferrari']])
        db.do([['INSERT', 'table'], ['Carlos Sainz', '30', 'Ferrari']])
        db.do([['INSERT', 'table'], ['Lewis Hamilton', '39', 'Mercedes']])
        responce = db.do([['SELECT', 'table'], ['AND', ['>', 'age', '27'], ['<', 'age', '40']]])
        self.assertEqual(responce.data, [['Carlos Sainz', '30', 'Ferrari'], ['Lewis Hamilton', '39', 'Mercedes']])

    def test_select_2level_indexed_3(self):
        db = DataBase()
        db.do([['CREATE', 'table'], [['name', False], ['age', True], ['team', False]]])
        db.do([['INSERT', 'table'], ['Max Verstappen', '27', 'ORBR']])
        db.do([['INSERT', 'table'], ['Charles Leclerc', '27', 'Ferrari']])
        db.do([['INSERT', 'table'], ['Carlos Sainz', '30', 'Ferrari']])
        db.do([['INSERT', 'table'], ['Lewis Hamilton', '39', 'Mercedes']])
        responce = db.do([['SELECT', 'table'], ['AND', ['>', 'age', '27'], ['<', 'age', '40']]])
        self.assertEqual(responce.data, [['Carlos Sainz', '30', 'Ferrari'], ['Lewis Hamilton', '39', 'Mercedes']])

    def test_select_3level_indexed_1(self):
        db = DataBase()
        db.do([['CREATE', 'table'], [['name', False], ['age', True], ['team', False]]])
        db.do([['INSERT', 'table'], ['Max Verstappen', '27', 'ORBR']])
        db.do([['INSERT', 'table'], ['Charles Leclerc', '27', 'Ferrari']])
        db.do([['INSERT', 'table'], ['Carlos Sainz', '30', 'Ferrari']])
        db.do([['INSERT', 'table'], ['Lewis Hamilton', '39', 'Mercedes']])
        responce = db.do([['SELECT', 'table'], ['AND', ['AND', ['>', 'age', '27'], ['<', 'age', '40']], ['=', 'team', 'Ferrari']]])
        self.assertEqual(responce.data, [['Carlos Sainz', '30', 'Ferrari']])

    def test_select_3level_indexed_2(self):
        db = DataBase()
        db.do([['CREATE', 'table'], [['name', False], ['age', True], ['team', False]]])
        db.do([['INSERT', 'table'], ['Max Verstappen', '27', 'ORBR']])
        db.do([['INSERT', 'table'], ['Charles Leclerc', '27', 'Ferrari']])
        db.do([['INSERT', 'table'], ['Carlos Sainz', '30', 'Ferrari']])
        db.do([['INSERT', 'table'], ['Lewis Hamilton', '39', 'Mercedes']])
        db.do([['INSERT', 'table'], ['George Russell', '26', 'Mercedes']])
        db.do([['INSERT', 'table'], ['Oscar Piastri', '23', 'McLaren']])
        db.do([['INSERT', 'table'], ['Lando Norris', '25', 'McLaren']])
        responce = db.do([['SELECT', 'table'], ['OR', ['AND', ['>', 'age', '26'], ['<', 'age', '28']], ['=', 'team', 'McLaren']]])
        self.assertEqual(responce.data, [['Max Verstappen', '27', 'ORBR'],['Charles Leclerc', '27', 'Ferrari'],['Oscar Piastri', '23', 'McLaren'],['Lando Norris', '25', 'McLaren']])

    def test_search_in_single_column_indexed(self):
        db = DataBase()
        db.do([['CREATE', 'table'], [['studentID', True], ['personalID', True]]])
        db.do([['INSERT', 'table'], ['114', '24673']])
        db.do([['INSERT', 'table'], ['24673', '27']])
        db.do([['INSERT', 'table'], ['4213', '114']])
        responce = db.do([['SELECT', 'table'], ['=', 'studentID', '114']])
        self.assertEqual(responce.data, [['114', '24673']])

    def test_search_in_single_column_notindexed(self):
        db = DataBase()
        db.do([['CREATE', 'table'], [['studentID', False], ['personalID', False]]])
        db.do([['INSERT', 'table'], ['114', '24673']])
        db.do([['INSERT', 'table'], ['24673', '27']])
        db.do([['INSERT', 'table'], ['4213', '114']])
        responce = db.do([['SELECT', 'table'], ['=', 'studentID', '114']])
        self.assertEqual(responce.data, [['114', '24673']])

    def test_search_in_single_column_semiindexed(self):
        db = DataBase()
        db.do([['CREATE', 'table'], [['studentID', True], ['personalID', False]]])
        db.do([['INSERT', 'table'], ['114', '24673']])
        db.do([['INSERT', 'table'], ['24673', '27']])
        db.do([['INSERT', 'table'], ['4213', '114']])
        responce = db.do([['SELECT', 'table'], ['=', 'studentID', '114']])
        self.assertEqual(responce.data, [['114', '24673']])

    def test_search_in_single_column_semiindexed_2(self):
        db = DataBase()
        db.do([['CREATE', 'table'], [['studentID', True], ['personalID', False]]])
        db.do([['INSERT', 'table'], ['114', '24673']])
        db.do([['INSERT', 'table'], ['24673', '27']])
        db.do([['INSERT', 'table'], ['4213', '114']])
        responce = db.do([['SELECT', 'table'], ['=', 'personalID', '114']])
        self.assertEqual(responce.data, [['4213', '114']])

if __name__ == '__main__':
    unittest.main()
