#!/usr/bin/env python3
"""Unit tests for the Atom Fusion formulas."""

import unittest
import sys
import os

# Add the tools directory to the path so we can import our modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import the functions we want to test
from atom_fusion_builder import (
    breeding_order_simple,
    breeding_order_tier_based,
    breeding_order_health,
    breeding_order_simple2
)

class TestFormulas(unittest.TestCase):
    """Test cases for the breeding order formulas."""

    def test_breeding_order_simple(self):
        """Test the simple breeding order formula."""
        result = breeding_order_simple(10, 5, 30, 5, 100, 6)
        # Expected: int((10 * 10 * 5)/(30 + 1) + (10 * 5) + (100/100) + 6)
        # = int(500/31 + 50 + 1 + 6) = int(16.13 + 57) = int(73.13) = 73
        self.assertEqual(result, 73)

    def test_breeding_order_tier_based_tier1(self):
        """Test tier-based breeding order for Tier 1 units."""
        result = breeding_order_tier_based(10, 5, 30, 5, 500, 6)
        # Should fall into Tier 1 category (life <= 1600)
        # But our test value is 500, so it should be in Tier 1
        self.assertGreaterEqual(result, 1)
        self.assertLessEqual(result, 74)

    def test_breeding_order_tier_based_tier4(self):
        """Test tier-based breeding order for Tier 4 units."""
        result = breeding_order_tier_based(100, 10, 20, 50, 9000, 10)
        # Should fall into Tier 4 category (life > 8000)
        self.assertGreaterEqual(result, 220)
        self.assertLessEqual(result, 2000)

    def test_breeding_order_health(self):
        """Test health-based breeding order formula."""
        result = breeding_order_health(10, 5, 30, 5, 1000, 6)
        # Expected: min(int(1000/20), 240) = min(50, 240) = 50
        self.assertEqual(result, 50)

    def test_breeding_order_health_max(self):
        """Test health-based breeding order formula at maximum."""
        result = breeding_order_health(10, 5, 30, 5, 10000, 6)
        # Expected: min(int(10000/20), 240) = min(500, 240) = 240
        self.assertEqual(result, 240)

    def test_breeding_order_simple2(self):
        """Test alternative simple breeding order formula."""
        result = breeding_order_simple2(10, 5, 30, 5, 100, 6)
        # Expected: int((10 * 10 * 5)/(30 + 1) + (100/10) + 6)
        # = int(500/31 + 10 + 6) = int(16.13 + 16) = int(32.13) = 32
        self.assertEqual(result, 32)

if __name__ == '__main__':
    unittest.main()