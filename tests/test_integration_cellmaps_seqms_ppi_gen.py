#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Integration Tests for `cellmaps_seqms_ppi_gen` package."""

import os

import unittest
from cellmaps_seqms_ppi_gen import cellmaps_seqms_ppi_gencmd

SKIP_REASON = 'CELLMAPS_SEQMS_PPI_GEN_INTEGRATION_TEST ' \
              'environment variable not set, cannot run integration ' \
              'tests'

@unittest.skipUnless(os.getenv('CELLMAPS_SEQMS_PPI_GEN_INTEGRATION_TEST') is not None, SKIP_REASON)
class TestIntegrationCellmaps_seqms_ppi_gen(unittest.TestCase):
    """Tests for `cellmaps_seqms_ppi_gen` package."""

    def setUp(self):
        """Set up test fixtures, if any."""

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_something(self):
        """Tests parse arguments"""
        self.assertEqual(1, 1)
