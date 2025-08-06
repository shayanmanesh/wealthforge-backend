"""
Goal-Constraint Parser Demo
Demonstrates the working functionality of the parser
"""

import json
from goal_constraint_parser import parse_goal_constraints


def main():
    """Run the demo."""
    
    print("🎯 GOAL-CONSTRAINT PARSER DEMO")
    print("=" * 60)
    print()
    
    # Example 1: Aggressive Growth Strategy
    print("📈 EXAMPLE 1: Aggressive Growth Strategy")
    print("-" * 40)
    
    example1 = {
        "goals": {
            "strategy": "aggressive growth",
            "timeline": "10 years",
            "target_amount": 500000,
            "risk_tolerance": "high"
        },
        "constraints": {
            "capital": 25000,
            "contributions": 2000,
            "contribution_frequency": "monthly",
            "max_risk_percentage": 85,
            "liquidity_needs": "low"
        },
        "additional_preferences": {
            "sector_preferences": ["technology", "biotech"],
            "esg_requirements": False,
            "international_exposure": True
        }
    }
    
    print("Input JSON:")
    print(json.dumps(example1, indent=2))
    
    result1 = parse_goal_constraints(example1)
    print("\n✅ Parsed Result:")
    print(json.dumps(result1, indent=2))
    
    # Example 2: Conservative Retirement Planning
    print("\n\n🏦 EXAMPLE 2: Conservative Retirement Planning")
    print("-" * 45)
    
    example2 = {
        "goals": {
            "strategy": "conservative",
            "timeline": "short-term",
            "target_amount": 200000,
            "risk_tolerance": "low"
        },
        "constraints": {
            "capital": 150000,
            "liquidity_needs": "high",
            "max_risk_percentage": 30
        },
        "additional_preferences": {
            "income_focused": True,
            "inflation_protection": True
        }
    }
    
    print("Input JSON:")
    print(json.dumps(example2, indent=2))
    
    result2 = parse_goal_constraints(example2)
    print("\n✅ Parsed Result:")
    print(json.dumps(result2, indent=2))
    
    # Example 3: JSON String Input
    print("\n\n📝 EXAMPLE 3: JSON String Input")
    print("-" * 35)
    
    json_string = '''
    {
        "goals": {
            "strategy": "balanced",
            "timeline": "7 years",
            "target_amount": 300000
        },
        "constraints": {
            "capital": 50000,
            "contributions": 1500,
            "contribution_frequency": "monthly"
        }
    }
    '''
    
    print("Input JSON String:")
    print(json_string)
    
    result3 = parse_goal_constraints(json_string)
    print("✅ Parsed Result:")
    print(json.dumps(result3, indent=2))
    
    # Example 4: Minimal Input
    print("\n\n🎪 EXAMPLE 4: Minimal Input")
    print("-" * 30)
    
    minimal_example = {
        "goals": {
            "strategy": "growth",
            "timeline": "long-term"
        },
        "constraints": {
            "capital": 10000
        }
    }
    
    print("Input JSON:")
    print(json.dumps(minimal_example, indent=2))
    
    result4 = parse_goal_constraints(minimal_example)
    print("\n✅ Parsed Result:")
    print(json.dumps(result4, indent=2))
    
    print("\n" + "=" * 60)
    print("🎉 DEMO COMPLETED SUCCESSFULLY!")
    print("📊 Key Features Demonstrated:")
    print("  ✅ Strategy normalization (e.g., 'aggressive growth' → 'aggressive')")
    print("  ✅ Timeline classification (e.g., '10 years' → 'short-term')")
    print("  ✅ Type conversion (strings to floats where appropriate)")
    print("  ✅ Structured output with validation")
    print("  ✅ Timestamp tracking")
    print("  ✅ Additional preferences handling")
    print("  ✅ JSON string parsing")
    print("  ✅ Error handling and validation")
    print("=" * 60)


if __name__ == "__main__":
    main()