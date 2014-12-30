# -*- coding: utf-8 -*-

import unittest
from operator import add

from chaining import Chain, RecastingChain, HistoryChain, SequenceChain, MappingChain
from filters import Filter, Select


class toto(object):
    def a(self):
        """ archetype of a mutable method returning self
        """
        return self
    def b(self):
        """ archetype of a mutable method returning None
        """
        return None
    def c(self):
        """ archetype of an accessor/computation method returning a result
        """
        return 1
    def d(self):
        """ archetype of a immutable method returning another object of same type
        """
        return self.__class__()


class ChainTestCase(unittest.TestCase):

    def test_mutable(self):
        l = [1, 2, 3]
        ll = list(l)
        c = Chain(ll)
        self.assertEqual(repr(c), 'Chain([1, 2, 3])')
        self.assertIs(c.append('x').__iadd__((4, 5)).extend('ab'), c)
        self.assertListEqual(c.wrapped, ll)
        self.assertListEqual(ll, l + ['x', 4, 5, 'a', 'b'])

    def test_immutable(self):
        l = [1, 2, 3]
        ll = list(l)
        c = Chain(ll)
        cc = c.__add__([4, 5])
        self.assertIs(cc, c)
        self.assertListEqual(cc.wrapped, l + [4, 5])
        self.assertListEqual(ll, l)

    def test_mutable_a(self):
        o = toto()
        c = Chain(o)
        cc = c.a()
        self.assertIs(cc, c)

    def test_mutable_b(self):
        o = toto()
        c = Chain(o)
        cc = c.b()
        self.assertIs(cc, c)

    def test_immutable_c(self):
        o = toto()
        c = Chain(o)
        cc = c.c()
        self.assertIs(cc, 1)

    def test_immutable_d(self):
        o = toto()
        c = Chain(o)
        cc = c.d()
        self.assertIs(cc, c)


class RecastingChainTestCase(unittest.TestCase):

    def test_immutable(self):
        l = [1, 2, 3]
        ll = list(l)
        c = RecastingChain(ll)
        cc = c.__add__([4, 5])
        self.assertIsNot(cc, c)
        self.assertIsInstance(cc, Chain)
        self.assertListEqual(cc.wrapped, l + [4, 5])
        self.assertListEqual(ll, l)

    def test_immutable_d(self):
        o = toto()
        c = RecastingChain(o)
        cc = c.d()
        self.assertIsInstance(cc, Chain)
        self.assertIsNot(cc, c)


class HistoryChainTestCase(unittest.TestCase):

    def test_immutable_d(self):
        o = toto()
        c = HistoryChain(o)
        cc = c.d()
        self.assertIs(cc, c)
        self.assertIsNot(cc.wrapped, o)
        self.assertIs(cc.backward().wrapped, o)


class SequenceChainTestCase(unittest.TestCase):

    def test_all(self):
        self.assertTrue(SequenceChain([1, 2, 3]).all())
        self.assertFalse(SequenceChain([1, 2, 3, 0]).all())

    def test_any(self):
        self.assertTrue(SequenceChain([1, 2, None]).any(f=lambda x: x is None))

    def test_first(self):
        self.assertEqual(SequenceChain([None, None, 'a']).first(f=lambda x: x is not None), 'a')

    def test_aggregate(self):
        l = [1, 2, 3]
        self.assertEqual(SequenceChain(l).aggregate(), ((1, 2), 3))
        self.assertEqual(SequenceChain(l).aggregate(op=add), 6)
        self.assertEqual(SequenceChain(l).aggregate(f=bool, op=add), 3)

    def test_where(self):
        l = ['ab', 'bc', 'ca', 'AB']
        self.assertListEqual(SequenceChain(l).where().reveal(), l)
        self.assertListEqual(SequenceChain(l).where(Filter(eq='ab')).reveal(), ['ab'])
        self.assertListEqual(SequenceChain(l).where(Filter(contains='a')).reveal(), ['ab', 'ca'])
        self.assertListEqual(SequenceChain(l).where(Filter(icontains='a')).reveal(), ['ab', 'ca', 'AB'])
        self.assertListEqual(SequenceChain(l).where(Filter(istartswith='a')).reveal(), ['ab', 'AB'])
        self.assertListEqual(SequenceChain(l).where(Filter(contains='a', contains_='b')).reveal(), ['ab', 'bc', 'ca'])

    def test_select(self):
        l = [1, 2, 3]
        self.assertListEqual(SequenceChain(l).select().reveal(), l)
        l = [
            dict(a=1, b=2, c=3),
            dict(a=5, b=6, d=7)
        ]
        self.assertEqual(SequenceChain(l).select(Select('a')).reveal(), [{'a': 1}, {'a': 5}])
        self.assertEqual(SequenceChain(l).select(Select('a', 'c')).reveal(), [{'a': 1, 'c': 3}, {'a': 5}])

if __name__ == '__main__':
    unittest.main()
