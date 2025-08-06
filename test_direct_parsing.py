"""
Direct test of the parser without LLM to verify functionality
"""

import json
from goal_constraint_parser import GoalConstraintParser


def test_direct_parsing():
    """Test direct parsing functionality."""
    
    # Create parser and force it to use direct parsing
    parser = GoalConstraintParser()
    
    # Test input
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
    
    print("Testing direct parsing method...")
    print("Input:")
    print(json.dumps(sample_input, indent=2))
    
    # Call direct parsing method directly
    result = parser._direct_parse(sample_input)
    
    print("\nDirect parsing result:")
    print(json.dumps(result, indent=2))
    
    return result


def test_various_inputs():
    """Test various input scenarios."""
    
    parser = GoalConstraintParser()
    
    test_cases = [
        {
            "name": "Conservative Investment",
            "input": {
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
        },
        {
            "name": "Growth Strategy",
            "input": {
                "goals": {
                    "strategy": "growth",
                    "timeline": "long-term"
                },
                "constraints": {
                    "capital": 10000
                }
            }
        },
        {
            "name": "Balanced Portfolio",
            "input": {
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
                }
            }
        }
    ]
    
    for test_case in test_cases:
        print(f"\n{'='*60}")
        print(f"TEST: {test_case['name']}")
        print('='*60)
        
        print("Input:")
        print(json.dumps(test_case['input'], indent=2))
        
        try:
            result = parser._direct_parse(test_case['input'])
            print("\nParsed Result:")
            print(json.dumps(result, indent=2))
        except Exception as e:
            print(f"\nError: {e}")


if __name__ == "__main__":
    print("🧪 TESTING DIRECT PARSING FUNCTIONALITY")
    print()
    
    test_direct_parsing()
    test_various_inputs()
    
    print("\n✅ Direct parsing tests completed!")