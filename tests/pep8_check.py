import os
import unittest
import pep8

import givinggraph


class TestFormatting(unittest.TestCase):
    def test_pep8(self):
        print 'Running PEP-8 checks on path', givinggraph.root
        pep8style = pep8.StyleGuide(paths=[givinggraph.root], ignore=['E128', 'E501'])
        total_errors = pep8style.check_files().total_errors
        self.assertEqual(total_errors, 0, 'Codebase does not pass PEP-8 (%d errors)' % total_errors)
