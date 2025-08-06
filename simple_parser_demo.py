"""
Simple Goal-Constraint Parser Demo using direct parsing
"""

import json
from goal_constraint_parser import GoalConstraintParser


def demo_parser():
    """Demonstrate the parser functionality."""
    
    print("🎯 GOAL-CONSTRAINT PARSER - WORKING DEMO")
    print("=" * 60)
    
    # Create parser
    parser = GoalConstraintParser()
    
    # Test cases
    test_cases = [
        {
            "name": "Aggressive Growth Investment",
            "input": {
                "goals": {
                    "strategy": "aggressive growth",
                    "timeline": "15 years",
                    "target_amount": 1000000,
                    "risk_tolerance": "high"
                },
                "constraints": {
                    "capital": 50000,
                    "contributions": 3000,
                    "contribution_frequency": "monthly",
                    "max_risk_percentage": 90,
                    "liquidity_needs": "low"
                },
                "additional_preferences": {
                    "sector_focus": ["technology", "growth stocks"],
                    "international": True
                }
            }
        },
        {
            "name": "Conservative Retirement Fund",
            "input": {
                "goals": {
                    "strategy": "conservative income",
                    "timeline": "short-term",
                    "risk_tolerance": "low"
                },
                "constraints": {
                    "capital": 250000,
                    "liquidity_needs": "high",
                    "max_risk_percentage": 25
                }
            }
        },
        {
            "name": "Balanced Portfolio",
            "input": {
                "goals": {
                    "strategy": "balanced",
                    "timeline": "8 years",
                    "target_amount": 400000
                },
                "constraints": {
                    "capital": 75000,
                    "contributions": 2000,
                    "contribution_frequency": "monthly"
                }
            }
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n📊 EXAMPLE {i}: {test_case['name']}")
        print("-" * 50)
        
        print("🔹 Input JSON:")
        print(json.dumps(test_case['input'], indent=2))
        
        # Use direct parsing to show actual functionality
        try:
            result = parser._direct_parse(test_case['input'])
            print("\n🔹 Parsed Output:")
            print(json.dumps(result, indent=2))
            
            # Highlight key features
            print(f"\n🔹 Key Parsing Results:")
            print(f"   Strategy: {test_case['input']['goals']['strategy']} → {result['goals']['strategy']}")
            print(f"   Timeline: {test_case['input']['goals']['timeline']} → {result['goals']['timeline']}")
            print(f"   Capital: ${result['constraints']['capital']:,.0f}")
            if result['constraints']['contributions']:
                print(f"   Contributions: ${result['constraints']['contributions']:,.0f} {result['constraints']['contribution_frequency'] or ''}")
            
        except Exception as e:
            print(f"❌ Error: {e}")
    
    # JSON String Example
    print(f"\n📝 EXAMPLE 4: JSON String Input")
    print("-" * 35)
    
    json_string = '''
    {
        "goals": {
            "strategy": "growth stocks",
            "timeline": "12 years"
        },
        "constraints": {
            "capital": 25000,
            "contributions": 1000,
            "contribution_frequency": "monthly"
        }
    }
    '''
    
    print("🔹 Input JSON String:")
    print(json_string)
    
    try:
        # Parse JSON string first
        import json as json_lib
        data = json_lib.loads(json_string)
        result = parser._direct_parse(data)
        
        print("🔹 Parsed Output:")
        print(json.dumps(result, indent=2))
        
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("\n" + "=" * 60)
    print("✅ PARSER FEATURES DEMONSTRATED:")
    print("  🔹 Strategy normalization ('aggressive growth' → 'aggressive')")
    print("  🔹 Timeline classification ('15 years' → 'long-term')")
    print("  🔹 Automatic data type conversion")
    print("  🔹 Structured data validation")
    print("  🔹 Optional field handling")
    print("  🔹 Additional preferences preservation")
    print("  🔹 Timestamp generation")
    print("  🔹 Error handling and validation")
    print("=" * 60)


if __name__ == "__main__":
    demo_parser()