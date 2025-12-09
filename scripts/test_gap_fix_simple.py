#!/usr/bin/env python3
"""
Simple standalone test for gap parameter fix

This test doesn't require Streamlit to be installed.
It tests the logic of the map_spacing_to_gap function.
"""


def map_spacing_to_gap(spacing: str) -> str:
    """
    Map design token spacing values to Streamlit's gap parameter.
    (Copied from chart_container.py for standalone testing)
    """
    # If already a valid Streamlit gap value, return as is
    if spacing in ["small", "medium", "large", "none"]:
        return spacing

    # Map rem values to closest Streamlit gap
    # Check for specific patterns in order (most specific first)

    # Small: Values less than 0.75rem
    if "0.5" in spacing or "0.25" in spacing or "0.125" in spacing:
        return "small"
    # Medium: 0.75rem - 1rem
    elif "0.75" in spacing or spacing == "1rem":
        return "medium"
    # Large: 1.5rem and above
    elif "1.5" in spacing or "2" in spacing or "3" in spacing or "4" in spacing or "6" in spacing:
        return "large"
    # Catch remaining "1" patterns (like "1rem") as medium
    elif "1" in spacing:
        return "medium"

    # Default to medium for unknown values
    return "medium"


def run_tests():
    """Run all test cases."""

    print("🧪 Testing map_spacing_to_gap() function\n")

    # Test cases: (input, expected, description)
    tests = [
        # Common design token values
        ("1.5rem", "large", "Spacing.LG (1.5rem) → large"),
        ("2rem", "large", "Spacing.XL (2rem) → large"),
        ("3rem", "large", "Spacing.XXL (3rem) → large"),
        ("4rem", "large", "Spacing.XXXL (4rem) → large"),
        ("1rem", "medium", "Spacing.BASE (1rem) → medium"),
        ("0.75rem", "medium", "Spacing.MD (0.75rem) → medium"),
        ("0.5rem", "small", "Spacing.SM (0.5rem) → small"),
        ("0.25rem", "small", "Spacing.XS (0.25rem) → small"),
        ("0.125rem", "small", "Spacing.XXS (0.125rem) → small"),

        # Already valid values (pass-through)
        ("large", "large", "Already valid: 'large'"),
        ("medium", "medium", "Already valid: 'medium'"),
        ("small", "small", "Already valid: 'small'"),
        ("none", "none", "Already valid: 'none'"),

        # Edge cases
        ("random", "medium", "Unknown value → default to 'medium'"),
    ]

    passed = 0
    failed = 0

    for input_val, expected, description in tests:
        result = map_spacing_to_gap(input_val)

        if result == expected:
            print(f"✅ {description}")
            print(f"   Input: '{input_val}' → Output: '{result}'")
            passed += 1
        else:
            print(f"❌ FAIL: {description}")
            print(f"   Input: '{input_val}'")
            print(f"   Expected: '{expected}', Got: '{result}'")
            failed += 1
        print()

    # Summary
    print("=" * 60)
    print(f"Results: {passed}/{len(tests)} tests passed")
    print("=" * 60)

    return failed == 0


if __name__ == "__main__":
    print("=" * 60)
    print("  Gap Parameter Fix - Simple Test")
    print("=" * 60)
    print()

    success = run_tests()

    if success:
        print("\n🎉 All tests passed!")
        print("The gap parameter fix is working correctly.")
        exit(0)
    else:
        print("\n❌ Some tests failed.")
        exit(1)
