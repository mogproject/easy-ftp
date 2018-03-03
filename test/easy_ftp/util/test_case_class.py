from easy_ftp.util.case_class import CaseClass
import unittest


class Coord(CaseClass):
    def __init__(self, x, y):
        CaseClass.__init__(self, x=x, y=y)


class Coord2(CaseClass):
    def __init__(self, x, y):
        CaseClass.__init__(self, x=x, y=y)


class Composed(CaseClass):
    def __init__(self, c):
        CaseClass.__init__(self, c=c)


class TestCaseClass(unittest.TestCase):
    def test_init(self):
        a = Coord(123, 45)
        self.assertEqual(a.x, 123)
        self.assertEqual(a.y, 45)

        class CoordX(CaseClass):
            def __init__(self):
                CaseClass.__init__(self, x=123, y=45)

        b = CoordX()
        self.assertEqual(b.x, 123)
        self.assertEqual(b.y, 45)

    def test_cmp(self):
        a = Coord(123, 45)
        b = Coord(123, 45)
        c = Coord(123, 46)
        d = Coord(124, 45)
        e = Coord(122, 46)

        combi = [(i, j) for i in [a, b, c, d, e] for j in [a, b, c, d, e]]

        self.assertEqual([x == y for x, y in combi], [
            True, True, False, False, False,
            True, True, False, False, False,
            False, False, True, False, False,
            False, False, False, True, False,
            False, False, False, False, True,
        ])

        self.assertEqual([x != y for x, y in combi], [
            False, False, True, True, True,
            False, False, True, True, True,
            True, True, False, True, True,
            True, True, True, False, True,
            True, True, True, True, False,
        ])

        self.assertEqual([x < y for x, y in combi], [
            False, False, True, True, False,
            False, False, True, True, False,
            False, False, False, True, False,
            False, False, False, False, False,
            True, True, True, True, False,
        ])

        self.assertEqual([x <= y for x, y in combi], [
            True, True, True, True, False,
            True, True, True, True, False,
            False, False, True, True, False,
            False, False, False, True, False,
            True, True, True, True, True,
        ])

        self.assertEqual([x > y for x, y in combi], [
            False, False, False, False, True,
            False, False, False, False, True,
            True, True, False, False, True,
            True, True, True, False, True,
            False, False, False, False, False,
        ])

        self.assertEqual([x >= y for x, y in combi], [
            True, True, False, False, True,
            True, True, False, False, True,
            True, True, True, False, True,
            True, True, True, True, True,
            False, False, False, False, True,
        ])

    def test_different_types(self):
        class AAA:
            pass

        self.assertEqual(Coord(123, 45) == 10, False)
        self.assertEqual(Coord(123, 45) == 'x', False)
        self.assertEqual(Coord(123, 45) == AAA(), False)

        self.assertRaisesRegex(TypeError, '^unorderable types: Coord\(\) < int\(\)$', lambda: Coord(123, 45) < 10)
        self.assertRaisesRegex(TypeError, '^unorderable types: Coord\(\) < ', lambda: Coord(123, 45) < 'x')
        self.assertRaisesRegex(TypeError, '^unorderable types: Coord\(\) < AAA\(\)$', lambda: Coord(123, 45) < AAA())

    def test_eq_composed(self):
        self.assertTrue(Composed(Coord(123, 45)) == Composed(Coord(123, 45)))
        self.assertFalse(Composed(Coord(123, 45)) == Composed(Coord2(123, 45)))
        self.assertTrue(Composed(Coord(123, 45)) != Composed(Coord2(123, 45)))
        self.assertFalse(Composed(Coord(123, 45)) != Composed(Coord(123, 45)))

    def test_repr(self):
        self.assertEqual(repr(Coord(123, 45)), 'Coord(x=123, y=45)')

    def test_copy(self):
        a = Coord(123, 45)
        b = a.copy(y=67)
        self.assertEqual(b, Coord(123, 67))

    def test_copy_error(self):
        self.assertRaisesRegex(AssertionError, 'Invalid key: z', Coord(123, 45).copy, x=999, z=999)

    def test_values(self):
        self.assertEqual(Coord(123, 45).values(), {'x': 123, 'y': 45})
