"""
Goal-Constraint Parser Usage Example
Demonstrates the correct way to use the parser functionality
"""

from goal_constraint_parser import GoalConstraintParser
import json

def main():
    """Main usage example."""
    
    print("🎯 Goal-Constraint Parser Usage Example")
    print("=" * 50)
    
    # Create parser instance
    parser = GoalConstraintParser()
    
    # Example 1: Complete investment scenario
    print("\n📈 Example 1: Complete Investment Scenario")
    print("-" * 40)
    
    investment_input = {
        "goals": {
            "strategy": "aggressive growth",
            "timeline": "15 years",
            "target_amount": 1000000,
            "risk_tolerance": "high"
        },
        "constraints": {
            "capital": 75000,
            "contributions": 3000,
            "contribution_frequency": "monthly",
            "max_risk_percentage": 85,
            "liquidity_needs": "low"
        },
        "additional_preferences": {
            "sectors": ["technology", "healthcare"],
            "esg_investing": True,
            "international_exposure": "moderate"
        }
    }
    
    print("Input:")
    print(json.dumps(investment_input, indent=2))
    
    # Use direct parsing to demonstrate actual functionality
    result = parser._direct_parse(investment_input)
    
    print("\nParsed Output:")
    print(json.dumps(result, indent=2))
    
    print(f"\n✨ Key Transformations:")
    print(f"   Strategy: '{investment_input['goals']['strategy']}' → '{result['goals']['strategy']}'")
    print(f"   Timeline: '{investment_input['goals']['timeline']}' → '{result['goals']['timeline']}'")
    print(f"   Capital: ${result['constraints']['capital']:,.0f}")
    
    # Example 2: Minimal input
    print("\n\n📊 Example 2: Minimal Input")
    print("-" * 30)
    
    minimal_input = {
        "goals": {
            "strategy": "conservative",
            "timeline": "short-term"
        },
        "constraints": {
            "capital": 50000
        }
    }
    
    print("Input:")
    print(json.dumps(minimal_input, indent=2))
    
    result2 = parser._direct_parse(minimal_input)
    
    print("\nParsed Output:")
    print(json.dumps(result2, indent=2))
    
    # Example 3: JSON string
    print("\n\n📝 Example 3: JSON String Input")
    print("-" * 35)
    
    json_string = '''
    {
        "goals": {
            "strategy": "balanced portfolio",
            "timeline": "7 years",
            "target_amount": 300000
        },
        "constraints": {
            "capital": 60000,
            "contributions": 1500,
            "contribution_frequency": "monthly"
        }
    }
    '''
    
    print("JSON String Input:")
    print(json_string)
    
    # Parse JSON string
    import json as json_lib
    data = json_lib.loads(json_string)
    result3 = parser._direct_parse(data)
    
    print("Parsed Output:")
    print(json.dumps(result3, indent=2))
    
    print("\n" + "=" * 50)
    print("✅ Parser Successfully Demonstrated!")
    print("📊 Features Shown:")
    print("  • Strategy normalization")
    print("  • Timeline classification") 
    print("  • Data type conversion")
    print("  • Validation and structure")
    print("  • Optional field handling")
    print("  • Additional preferences")
    print("  • Timestamp generation")
    

if __name__ == "__main__":
    main()