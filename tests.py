import unittest

from cmk import Check, fmt_perf


class TestCheck(unittest.TestCase):
    def setUp(self):
        self.check_name = "test"
        self.check = Check(self.check_name)

    def test_ok(self):
        self.assertEquals("0 test - hello world", self.check.ok("hello world"))
    
    def test_warn(self):
        self.assertEquals("1 test - hello world", self.check.warn("hello world"))

    def test_crit(self):
        self.assertEquals("2 test - hello world", self.check.crit("hello world"))
    
    def test_unknown(self):
        self.assertEquals("3 test - hello world", self.check.unknown("hello world"))

    def test_ok_perf(self):
        resp = self.check.ok("hello world", [["test", 10]])
        self.assertEquals("0 test test=10 hello world", resp)

    def test_warn_perf(self):
        resp = self.check.warn("hello world", [["test", 25, 20, 30]])
        self.assertEquals("1 test test=25;20;30 hello world", resp)
    
    def test_crit_perf(self):
        resp = self.check.crit("hello world", [["test", 35, 20, 30, 0, 50]])
        self.assertEquals("2 test test=35;20;30;0;50 hello world", resp)

    def test_unknown_perf(self):
        resp = self.check.unknown("hello world", [["test", 35, 20, 30]])
        self.assertEquals("3 test test=35;20;30 hello world", resp)
    
    def test_compute_perf(self):
        resp = self.check.compute("hello world", [["test", 35, 20, 30]])
        self.assertEquals("P test test=35;20;30 hello world", resp)

    def test_ok_multi_perf(self):
        resp = self.check.ok("hello world", [["test", 10, 20, 30], ["other", 1, 2, 3, 0, 5]])
        self.assertEquals("0 test test=10;20;30|other=1;2;3;0;5 hello world", resp)


class TestFmtPerf(unittest.TestCase):
    def test_ok(self):
        self.assertEqual("test=1", fmt_perf(["test", 1]))
    
    def test_min_length(self):
        with self.assertRaises(ValueError):
            fmt_perf([])

        with self.assertRaises(ValueError):
            fmt_perf(["test"])


    def test_max_length(self):
        with self.assertRaises(ValueError):
            fmt_perf(["test", 1, 2, 3, 4, 5, 6])
