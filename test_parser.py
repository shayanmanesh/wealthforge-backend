"""
Test and example usage for Goal-Constraint Parser
"""

import json
from goal_constraint_parser import parse_goal_constraints, GoalConstraintParser


def test_example_1():
    """Test basic goal and constraint parsing."""
    print("=" * 60)
    print("TEST 1: Basic Goals and Constraints")
    print("=" * 60)
    
    sample_input = {
        "goals": {
            "strategy": "aggressive growth",
            "timeline": "10 years",
            "target_amount": 100000,
            "risk_tolerance": "high"
        },
        "constraints": {
            "capital": 25000,
            "contributions": 500,
            "contribution_frequency": "monthly",
            "max_risk_percentage": 80,
            "liquidity_needs": "low"
        },
        "additional_preferences": {
            "sector_preferences": ["technology", "healthcare"],
            "esg_requirements": True
        }
    }
    
    print("Input JSON:")
    print(json.dumps(sample_input, indent=2))
    print("\nParsed Output:")
    
    try:
        result = parse_goal_constraints(sample_input)
        print(json.dumps(result, indent=2))
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False


def test_example_2():
    """Test conservative investment parsing."""
    print("\n" + "=" * 60)
    print("TEST 2: Conservative Investment")
    print("=" * 60)
    
    sample_input = {
        "goals": {
            "strategy": "conservative",
            "timeline": "short-term",
            "risk_tolerance": "low"
        },
        "constraints": {
            "capital": 50000,
            "liquidity_needs": "high"
        }
    }
    
    print("Input JSON:")
    print(json.dumps(sample_input, indent=2))
    print("\nParsed Output:")
    
    try:
        result = parse_goal_constraints(sample_input)
        print(json.dumps(result, indent=2))
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False


def test_example_3():
    """Test JSON string input."""
    print("\n" + "=" * 60)
    print("TEST 3: JSON String Input")
    print("=" * 60)
    
    json_string = '''
    {
        "goals": {
            "strategy": "balanced",
            "timeline": "5 years",
            "target_amount": 75000
        },
        "constraints": {
            "capital": 15000,
            "contributions": 1000,
            "contribution_frequency": "quarterly",
            "max_risk_percentage": 60
        },
        "additional_preferences": {
            "diversification": "international",
            "tax_efficiency": true
        }
    }
    '''
    
    print("Input JSON String:")
    print(json_string)
    print("\nParsed Output:")
    
    try:
        result = parse_goal_constraints(json_string)
        print(json.dumps(result, indent=2))
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False


def test_example_4():
    """Test minimal input."""
    print("\n" + "=" * 60)
    print("TEST 4: Minimal Input")
    print("=" * 60)
    
    sample_input = {
        "goals": {
            "strategy": "growth",
            "timeline": "long-term"
        },
        "constraints": {
            "capital": 10000
        }
    }
    
    print("Input JSON:")
    print(json.dumps(sample_input, indent=2))
    print("\nParsed Output:")
    
    try:
        result = parse_goal_constraints(sample_input)
        print(json.dumps(result, indent=2))
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False


def test_example_5():
    """Test retirement planning scenario."""
    print("\n" + "=" * 60)
    print("TEST 5: Retirement Planning")
    print("=" * 60)
    
    sample_input = {
        "goals": {
            "strategy": "moderate",
            "timeline": "30 years",
            "target_amount": 1000000,
            "risk_tolerance": "medium"
        },
        "constraints": {
            "capital": 5000,
            "contributions": 2000,
            "contribution_frequency": "monthly",
            "max_risk_percentage": 70,
            "liquidity_needs": "low"
        },
        "additional_preferences": {
            "retirement_age": 65,
            "inflation_protection": True,
            "tax_advantaged_accounts": ["401k", "IRA"]
        }
    }
    
    print("Input JSON:")
    print(json.dumps(sample_input, indent=2))
    print("\nParsed Output:")
    
    try:
        result = parse_goal_constraints(sample_input)
        print(json.dumps(result, indent=2))
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False


def test_error_handling():
    """Test error handling with invalid input."""
    print("\n" + "=" * 60)
    print("TEST 6: Error Handling")
    print("=" * 60)
    
    # Test invalid JSON string
    print("Testing invalid JSON string...")
    try:
        result = parse_goal_constraints("invalid json string")
        print("Should have failed!")
        return False
    except ValueError as e:
        print(f"Correctly caught error: {e}")
    
    # Test negative capital
    print("\nTesting negative capital...")
    try:
        invalid_input = {
            "goals": {"strategy": "growth", "timeline": "5 years"},
            "constraints": {"capital": -1000}
        }
        result = parse_goal_constraints(invalid_input)
        print("Should have failed!")
        return False
    except ValueError as e:
        print(f"Correctly caught error: {e}")
    
    return True


def demonstrate_parser_features():
    """Demonstrate key features of the parser."""
    print("\n" + "=" * 80)
    print("GOAL-CONSTRAINT PARSER FEATURES DEMONSTRATION")
    print("=" * 80)
    
    print("\n🎯 KEY FEATURES:")
    print("✅ Parses JSON input (string or dict)")
    print("✅ Validates data using Pydantic models")
    print("✅ Uses LangChain for intelligent parsing")
    print("✅ Provides structured output as Python dict")
    print("✅ Handles missing fields gracefully")
    print("✅ Normalizes strategy and timeline values")
    print("✅ Includes timestamp for tracking")
    print("✅ Supports additional preferences")
    print("✅ Fallback parsing when LLM unavailable")
    
    print("\n📊 SUPPORTED GOAL FIELDS:")
    print("• strategy: Investment strategy (conservative, moderate, aggressive, etc.)")
    print("• timeline: Investment timeline (short-term, medium-term, long-term, or specific)")
    print("• target_amount: Target amount to achieve (optional)")
    print("• risk_tolerance: Risk tolerance level (low, medium, high)")
    
    print("\n💰 SUPPORTED CONSTRAINT FIELDS:")
    print("• capital: Initial capital amount (required)")
    print("• contributions: Regular contribution amount (optional)")
    print("• contribution_frequency: Frequency of contributions (monthly, quarterly, annual)")
    print("• max_risk_percentage: Maximum risk percentage (0-100)")
    print("• liquidity_needs: Liquidity requirements (high, medium, low)")
    
    print("\n🔧 ADDITIONAL FEATURES:")
    print("• additional_preferences: Custom preferences and requirements")
    print("• parsed_timestamp: Automatic timestamp when parsing completed")
    print("• Error handling and validation")
    print("• Flexible input formats")


if __name__ == "__main__":
    print("🚀 GOAL-CONSTRAINT PARSER TESTING")
    
    # Demonstrate features
    demonstrate_parser_features()
    
    # Run all tests
    tests = [
        test_example_1,
        test_example_2, 
        test_example_3,
        test_example_4,
        test_example_5,
        test_error_handling
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"Test failed with exception: {e}")
    
    print("\n" + "=" * 80)
    print(f"📊 TEST RESULTS: {passed}/{total} tests passed")
    print("=" * 80)
    
    if passed == total:
        print("🎉 All tests passed! The Goal-Constraint Parser is working correctly.")
    else:
        print("⚠️  Some tests failed. Please check the implementation.")