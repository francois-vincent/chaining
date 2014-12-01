# -*- coding: utf-8 -*-

import unittest

from chaining import MappingChain
from filters import RegExp, Filter, RecordFilter, UnknownOperatorError


class RegExpTestCase(unittest.TestCase):

    def test_search(self):
        re = RegExp('\d')
        self.assertTrue(re('xx10xx'))

    def test_match(self):
        re = RegExp('\d', match=True)
        self.assertFalse(re('xx10xx'))
        self.assertTrue(re('10xx'))


class FilterTestCase(unittest.TestCase):

    def test_unknown_operator(self):
        self.assertRaises(UnknownOperatorError, Filter, operator=0)

    def test_equals(self):
        data = 123
        filter = Filter(equals=123)
        self.assertTrue(filter(data))
        data = '123'
        self.assertTrue(filter(data))
        filter = Filter(neq='abc')
        self.assertTrue(filter(data))

    def test_iequals(self):
        data = 'ABCDE'
        filter = Filter(ieq='abcde')
        self.assertTrue(filter(data))

    def test_regexp(self):
        data = 'xx10xx'
        filter = Filter(search='\d')
        self.assertTrue(filter(data))
        filter = Filter(match='\d')
        self.assertFalse(filter(data))


class RecordFilterTestCase(unittest.TestCase):

    def setUp(self):
        self.data = dict(
            name='abcdef',
            age='12',
        )

    def test_unknown_operator(self):
        self.assertRaises(UnknownOperatorError, RecordFilter, name__operator=0)

    def test_equals(self):
        data = self.data
        filter = RecordFilter(name='abcdef', age=12)
        self.assertTrue(filter(data))
        data['age'] = 12
        self.assertTrue(filter(data))
        data['name'] = 'zorro'
        self.assertFalse(filter(data))
        filter = RecordFilter(name__neq='abcdef', age=12)
        self.assertTrue(filter(data))

    def test_iequals(self):
        data = MappingChain(self.data).update(name='ABCDEF').reveal()
        filter = RecordFilter(name__ieq='abcdef', age=12)
        self.assertTrue(filter(data))
        filter = RecordFilter(name__nieq='abcdef', age=12)
        self.assertFalse(filter(data))

    def test_contains(self):
        data = self.data
        filter = RecordFilter(name__contains='bcd', age=12)
        self.assertTrue(filter(data))
        filter = RecordFilter(name__notcontains='bcd', age=12)
        self.assertFalse(filter(data))

    def test_icontains(self):
        data = MappingChain(self.data).update(name='ABCDEF').reveal()
        filter = RecordFilter(name__icontains='bcd', age=12)
        self.assertTrue(filter(data))
        filter = RecordFilter(name__noticontains='bcd', age=12)
        self.assertFalse(filter(data))

    def test_startswith(self):
        data = self.data
        filter = RecordFilter(name__start='abc', age=12)
        self.assertTrue(filter(data))
        filter = RecordFilter(name__nstart='abc', age=12)
        self.assertFalse(filter(data))

    def test_istartswith(self):
        data = MappingChain(self.data).update(name='ABCDEF').reveal()
        filter = RecordFilter(name__istart='abc', age=12)
        self.assertTrue(filter(data))
        filter = RecordFilter(name__nistart='abc', age=12)
        self.assertFalse(filter(data))

    def tetst_gt(self):
        data = self.data
        filter = RecordFilter(name='abcdef', age__gt=10)
        self.assertTrue(filter(data))
        filter = RecordFilter(name='abcdef', age__gt=18)
        self.assertFalse(filter(data))

    def test_inrange(self):
        data = self.data
        filter = RecordFilter(name='abcdef', age__inrange=(10, 13))
        self.assertTrue(filter(data))
        filter = RecordFilter(name='abcdef', age__inrange=(10, 12))
        self.assertFalse(filter(data))

    def test_missing_key(self):
        data = self.data
        filter = RecordFilter(name='abcdef', value__inrange=(10, 13))
        self.assertFalse(filter(data))
        filter = RecordFilter(name='abcdef', value__inrange=(10, 13), _key_missing_=True)
        self.assertTrue(filter(data))
        filter = RecordFilter(name='abcdef', value__inrange=(10, 13), _key_missing_=None)
        self.assertRaises(KeyError, filter, data)

    def test_or(self):
        data = self.data
        filter = RecordFilter({'name': 'abcdef'}, {'age': 13})
        self.assertTrue(filter(data))
        filter = RecordFilter({'name': 'toto'}, {'age': 12})
        self.assertTrue(filter(data))
        filter = RecordFilter({'name': 'toto'}, {'age': 13})
        self.assertFalse(filter(data))

    def test_regexp(self):
        data = MappingChain(self.data).update(age='xx10xx').reveal()
        filter = RecordFilter(name='abcdef', age__search='\d')
        self.assertTrue(filter(data))
        filter = RecordFilter(name='abcdef', age__match='\d')
        self.assertFalse(filter(data))


if __name__ == '__main__':
    unittest.main()
