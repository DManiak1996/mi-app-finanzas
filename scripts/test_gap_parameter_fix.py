#!/usr/bin/env python3
"""
Test script for st.columns() gap parameter fix

This script verifies that the map_spacing_to_gap() function correctly
converts design tokens to valid Streamlit gap values.

Usage:
    python scripts/test_gap_parameter_fix.py
"""

import sys
sys.path.insert(0, '/Users/daniel/mi_app_finanzas')

from utils.components.chart_container import map_spacing_to_gap
from utils.design_tokens import Spacing


def test_map_spacing_to_gap():
    """Test the map_spacing_to_gap function with various inputs."""

    print("🧪 Testing map_spacing_to_gap() function...\n")

    # Test cases: (input, expected_output, description)
    test_cases = [
        # Design token spacing values
        (Spacing.LG, "large", "Spacing.LG (1.5rem)"),
        (Spacing.XL, "large", "Spacing.XL (2rem)"),
        (Spacing.XXL, "large", "Spacing.XXL (3rem)"),
        (Spacing.BASE, "medium", "Spacing.BASE (1rem)"),
        (Spacing.MD, "medium", "Spacing.MD (0.75rem)"),
        (Spacing.SM, "small", "Spacing.SM (0.5rem)"),
        (Spacing.XS, "small", "Spacing.XS (0.25rem)"),
        (Spacing.XXS, "small", "Spacing.XXS (0.125rem)"),

        # Already valid Streamlit gap values
        ("large", "large", "Already 'large'"),
        ("medium", "medium", "Already 'medium'"),
        ("small", "small", "Already 'small'"),
        ("none", "none", "Already 'none'"),

        # Edge cases
        ("1.5rem", "large", "Custom rem value (1.5rem)"),
        ("2rem", "large", "Custom rem value (2rem)"),
        ("1rem", "medium", "Custom rem value (1rem)"),
        ("0.5rem", "small", "Custom rem value (0.5rem)"),
    ]

    passed = 0
    failed = 0

    for input_val, expected, description in test_cases:
        result = map_spacing_to_gap(input_val)

        if result == expected:
            print(f"✅ PASS: {description}")
            print(f"   Input: {input_val!r} → Output: {result!r}")
            passed += 1
        else:
            print(f"❌ FAIL: {description}")
            print(f"   Input: {input_val!r}")
            print(f"   Expected: {expected!r}, Got: {result!r}")
            failed += 1
        print()

    # Summary
    print("=" * 60)
    print(f"📊 Test Results: {passed} passed, {failed} failed")
    print("=" * 60)

    if failed == 0:
        print("\n🎉 All tests passed! The fix is working correctly.")
        return 0
    else:
        print(f"\n⚠️  {failed} test(s) failed. Please review the implementation.")
        return 1


def test_streamlit_columns_mock():
    """Simulate how Streamlit would call st.columns with the converted gap."""

    print("\n🔧 Testing Streamlit columns mock...\n")

    # Simulate Streamlit's gap validation
    valid_gaps = ["small", "medium", "large", "none"]

    def mock_st_columns(num_cols, gap="medium"):
        """Mock st.columns function with validation."""
        if gap not in valid_gaps:
            raise ValueError(
                f"The gap argument to st.columns must be {', '.join(repr(g) for g in valid_gaps)}. "
                f"The argument passed was {gap}."
            )
        return f"✅ Created {num_cols} columns with gap='{gap}'"

    # Test with design tokens (should work after conversion)
    test_cases = [
        (2, Spacing.LG, "Two columns with Spacing.LG"),
        (3, Spacing.MD, "Three columns with Spacing.MD"),
        (4, Spacing.SM, "Four columns with Spacing.SM"),
    ]

    for num_cols, gap_token, description in test_cases:
        try:
            # Convert the gap token
            converted_gap = map_spacing_to_gap(gap_token)

            # Try to create columns with converted gap
            result = mock_st_columns(num_cols, converted_gap)
            print(f"✅ {description}")
            print(f"   Token: {gap_token!r} → Converted: {converted_gap!r}")
            print(f"   Result: {result}")
            print()
        except ValueError as e:
            print(f"❌ {description}")
            print(f"   Error: {e}")
            print()
            return 1

    print("🎉 All mock Streamlit columns calls succeeded!")
    return 0


if __name__ == "__main__":
    print("=" * 60)
    print("     st.columns() Gap Parameter Fix - Test Suite")
    print("=" * 60)
    print()

    # Run tests
    result1 = test_map_spacing_to_gap()
    result2 = test_streamlit_columns_mock()

    # Exit with appropriate code
    exit_code = max(result1, result2)

    if exit_code == 0:
        print("\n" + "=" * 60)
        print("✅ ALL TESTS PASSED - Fix is working correctly!")
        print("=" * 60)
    else:
        print("\n" + "=" * 60)
        print("❌ SOME TESTS FAILED - Please review")
        print("=" * 60)

    sys.exit(exit_code)
