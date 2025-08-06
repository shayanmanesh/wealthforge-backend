"""
Orchestrator Agent Demo

Practical examples showing how to use the Orchestrator Agent 
for real investment advisory scenarios.
"""

import json
import asyncio
from orchestrator_agent import orchestrate_investment_task, OrchestratorAgent
from goal_constraint_parser import parse_goal_constraints


async def demo_young_professional():
    """Demo scenario: Young professional starting investment journey."""
    print("💼 SCENARIO 1: Young Professional (Age 28)")
    print("=" * 50)
    
    scenario = {
        "name": "Sarah, Software Engineer",
        "description": "28-year-old with stable income, wants aggressive growth for retirement",
        "user_input": {
            "goals": {
                "strategy": "aggressive growth for maximum returns",
                "timeline": "35 years until retirement",
                "target_amount": 2000000,
                "risk_tolerance": "high - I can handle volatility"
            },
            "constraints": {
                "capital": 25000,  # Initial investment
                "contributions": 2000,  # Monthly contribution
                "contribution_frequency": "monthly",
                "max_risk_percentage": 90,
                "liquidity_needs": "very low - won't need money for decades"
            },
            "additional_preferences": {
                "sector_focus": ["technology", "healthcare", "clean energy"],
                "international_exposure": True,
                "esg_investing": True
            }
        }
    }
    
    print(f"👤 Client: {scenario['name']}")
    print(f"📋 Scenario: {scenario['description']}")
    print("\n📝 Client Input:")
    print(json.dumps(scenario['user_input'], indent=2))
    
    # Execute orchestration
    result = await orchestrate_investment_task(
        scenario['user_input'],
        f"Provide investment recommendation for {scenario['name']}"
    )
    
    print(f"\n🎯 Orchestrator Results:")
    print(f"   Strategy Identified: {result['target_strategy']}")
    print(f"   Competing Agents: {', '.join(result['competing_agents'])}")
    print(f"   Winner: {result['winner']['agent']} (confidence: {result['winner']['confidence']:.1%})")
    
    print(f"\n🏆 Winning Recommendation:")
    winner_result = next(r for r in result['agent_results'] if r['agent_name'] == result['winner']['agent'])
    rec = winner_result['recommendation']
    print(f"   Allocation: {rec.get('allocation', 'N/A')}")
    print(f"   Expected Return: {rec.get('expected_return', {}).get('range', 'N/A')}")
    print(f"   Time Horizon: {rec.get('time_horizon', 'N/A')}")
    
    return result


async def demo_pre_retiree():
    """Demo scenario: Pre-retiree focusing on capital preservation."""
    print("\n\n🏡 SCENARIO 2: Pre-Retiree (Age 58)")
    print("=" * 45)
    
    scenario = {
        "name": "Robert, Marketing Executive",
        "description": "58-year-old nearing retirement, needs income and capital preservation",
        "user_input": {
            "goals": {
                "strategy": "conservative income with some growth",
                "timeline": "7 years to retirement, then 20+ years in retirement",
                "target_amount": 800000,
                "risk_tolerance": "low to moderate"
            },
            "constraints": {
                "capital": 400000,  # Substantial savings
                "contributions": 3000,  # Catching up contributions
                "contribution_frequency": "monthly",
                "max_risk_percentage": 40,
                "liquidity_needs": "moderate - may need access for emergencies"
            },
            "additional_preferences": {
                "income_focus": True,
                "dividend_stocks": True,
                "bond_ladder": True,
                "inflation_protection": True
            }
        }
    }
    
    print(f"👤 Client: {scenario['name']}")
    print(f"📋 Scenario: {scenario['description']}")
    
    result = await orchestrate_investment_task(
        scenario['user_input'],
        f"Design retirement transition strategy for {scenario['name']}"
    )
    
    print(f"\n🎯 Orchestrator Results:")
    print(f"   Strategy Identified: {result['target_strategy']}")
    print(f"   Winner: {result['winner']['agent']}")
    
    # Show all agent perspectives
    print(f"\n🤝 Multi-Agent Perspectives:")
    for agent_result in result['agent_results']:
        print(f"   • {agent_result['agent_name']} ({agent_result['confidence']:.1%} confidence)")
        reasoning = agent_result['reasoning'][:100] + "..." if len(agent_result['reasoning']) > 100 else agent_result['reasoning']
        print(f"     {reasoning}")
    
    return result


async def demo_family_planning():
    """Demo scenario: Family with children planning for education and retirement."""
    print("\n\n👨‍👩‍👧‍👦 SCENARIO 3: Family Planning (Ages 35 & 33)")
    print("=" * 55)
    
    scenario = {
        "name": "The Johnson Family",
        "description": "Family with two young children, balancing education and retirement savings",
        "user_input": {
            "goals": {
                "strategy": "balanced growth with education planning",
                "timeline": "15 years for college, 30 years for retirement",
                "target_amount": 500000,
                "risk_tolerance": "moderate"
            },
            "constraints": {
                "capital": 75000,
                "contributions": 1500,
                "contribution_frequency": "monthly",
                "max_risk_percentage": 65,
                "liquidity_needs": "moderate - college expenses in 10-15 years"
            },
            "additional_preferences": {
                "education_savings": "529 plans",
                "tax_efficiency": True,
                "diversification": "domestic and international",
                "life_insurance": "term life for protection"
            }
        }
    }
    
    print(f"👤 Clients: {scenario['name']}")
    print(f"📋 Scenario: {scenario['description']}")
    
    result = await orchestrate_investment_task(
        scenario['user_input'],
        f"Create comprehensive family financial plan for {scenario['name']}"
    )
    
    print(f"\n🎯 Orchestrator Analysis:")
    print(f"   Primary Strategy: {result['target_strategy']}")
    print(f"   Agents Consulted: {len(result['agent_results'])}")
    
    # Show consensus
    consensus = result['consensus_recommendation']
    print(f"\n🤝 Consensus Recommendation:")
    print(f"   {consensus.get('recommendation_summary', 'Balanced approach recommended')}")
    print(f"   Confidence Level: {consensus.get('average_confidence', 0):.1%}")
    
    return result


async def demo_high_net_worth():
    """Demo scenario: High net worth individual with complex needs."""
    print("\n\n💎 SCENARIO 4: High Net Worth Individual")
    print("=" * 50)
    
    scenario = {
        "name": "Dr. Elizabeth Chen",
        "description": "Successful surgeon with high income and complex investment needs",
        "user_input": {
            "goals": {
                "strategy": "sophisticated growth with tax optimization",
                "timeline": "20 years to semi-retirement",
                "target_amount": 5000000,
                "risk_tolerance": "moderate to high"
            },
            "constraints": {
                "capital": 1200000,
                "contributions": 15000,
                "contribution_frequency": "monthly",
                "max_risk_percentage": 75,
                "liquidity_needs": "low for most assets"
            },
            "additional_preferences": {
                "tax_optimization": "maximum tax efficiency",
                "alternative_investments": "real estate, private equity",
                "estate_planning": "generational wealth transfer",
                "philanthropic_giving": "charitable strategies",
                "business_interests": "medical practice ownership"
            }
        }
    }
    
    print(f"👤 Client: {scenario['name']}")
    print(f"📋 Scenario: {scenario['description']}")
    
    result = await orchestrate_investment_task(
        scenario['user_input'],
        f"Design sophisticated wealth management strategy for {scenario['name']}"
    )
    
    print(f"\n🎯 Orchestrator Insights:")
    print(f"   Complexity Level: High")
    print(f"   Strategy Match: {result['target_strategy']}")
    
    # Show execution details
    print(f"\n⚡ Execution Analysis:")
    print(f"   Processing Time: {result['execution_time']:.2f} seconds")
    print(f"   Agents Analyzed: {len(result['competing_agents'])}")
    
    # Show agent competition results
    print(f"\n🏆 Agent Competition Results:")
    for i, agent_result in enumerate(result['agent_results'], 1):
        print(f"   {i}. {agent_result['agent_name']}")
        print(f"      Strategy Focus: {agent_result['strategy_type']}")
        print(f"      Confidence: {agent_result['confidence']:.1%}")
        print(f"      Processing Time: {agent_result['execution_time']:.2f}s")
    
    return result


async def compare_strategies():
    """Compare how different strategies are handled by the orchestrator."""
    print("\n\n📊 STRATEGY COMPARISON ANALYSIS")
    print("=" * 50)
    
    # Same financial situation, different strategies
    base_situation = {
        "constraints": {
            "capital": 100000,
            "contributions": 2000,
            "contribution_frequency": "monthly"
        }
    }
    
    strategies_to_test = [
        ("Ultra Conservative", "capital preservation with minimal risk"),
        ("Conservative Income", "steady income with low risk"),
        ("Moderate Growth", "balanced growth and income"),
        ("Aggressive Growth", "maximum growth potential"),
        ("Speculative", "high-risk high-reward investments")
    ]
    
    results = []
    
    for strategy_name, strategy_desc in strategies_to_test:
        test_input = {
            "goals": {
                "strategy": strategy_desc,
                "timeline": "10 years",
                "risk_tolerance": strategy_name.lower()
            },
            **base_situation
        }
        
        print(f"\n🧪 Testing: {strategy_name}")
        result = await orchestrate_investment_task(test_input, f"Recommend {strategy_name} strategy")
        
        winner = result['winner']
        print(f"   Winner: {winner['agent']} (confidence: {winner['confidence']:.1%})")
        print(f"   Strategy Detected: {result['target_strategy']}")
        
        results.append({
            "strategy": strategy_name,
            "winner": winner['agent'],
            "confidence": winner['confidence'],
            "target": result['target_strategy']
        })
    
    # Summary comparison
    print(f"\n📈 STRATEGY COMPARISON SUMMARY:")
    print("-" * 40)
    for result in results:
        print(f"   {result['strategy']:<20} → {result['winner']:<20} ({result['confidence']:.1%})")


async def demonstrate_performance_tracking():
    """Demonstrate performance tracking and learning."""
    print("\n\n📊 PERFORMANCE TRACKING DEMONSTRATION")
    print("=" * 55)
    
    orchestrator = OrchestratorAgent(enable_logging=True)
    
    # Simulate multiple investment scenarios over time
    scenarios = [
        {"strategy": "aggressive", "success": 0.9},
        {"strategy": "conservative", "success": 0.95},
        {"strategy": "moderate", "success": 0.85},
        {"strategy": "aggressive", "success": 0.8},
        {"strategy": "conservative", "success": 0.9}
    ]
    
    print("Simulating investment outcomes and performance updates...")
    
    for i, scenario in enumerate(scenarios):
        # Simulate task execution
        test_input = {
            "goals": {"strategy": scenario["strategy"], "timeline": "10 years"},
            "constraints": {"capital": 50000}
        }
        
        parsed = parse_goal_constraints(test_input)
        result = await orchestrator.orchestrate_task(parsed, f"Scenario {i+1}")
        
        # Update performance based on simulated success
        winner_agent = result['winner']['agent']
        orchestrator.competition_manager.update_performance(winner_agent, scenario["success"])
        
        print(f"   Scenario {i+1}: {scenario['strategy']} strategy, {scenario['success']:.1%} success")
    
    # Show final performance summary
    summary = orchestrator.get_performance_summary()
    
    print(f"\n📈 Final Performance Scores:")
    for agent_name, score_data in summary['agent_scores'].items():
        if score_data:  # Only show agents that have been scored
            print(f"   {agent_name}: {score_data['performance_score']:.3f}")


async def main():
    """Run all demo scenarios."""
    print("🎯 ORCHESTRATOR AGENT DEMONSTRATION")
    print("=" * 70)
    print("Showing practical investment advisory scenarios with agent competition")
    print("=" * 70)
    
    try:
        # Run demo scenarios
        await demo_young_professional()
        await demo_pre_retiree()
        await demo_family_planning()
        await demo_high_net_worth()
        await compare_strategies()
        await demonstrate_performance_tracking()
        
        print("\n" + "=" * 70)
        print("🎉 ORCHESTRATOR DEMONSTRATION COMPLETE!")
        print("=" * 70)
        print("Key Features Demonstrated:")
        print("✅ Multi-agent competition based on strategy matching")
        print("✅ Dynamic weighting system for agent selection")
        print("✅ Task distribution and result aggregation")
        print("✅ Integration with goal-constraint parser")
        print("✅ Performance tracking and learning")
        print("✅ Consensus building from multiple expert opinions")
        print("✅ Real-world investment advisory scenarios")
        print("=" * 70)
        
    except Exception as e:
        print(f"\n❌ Demo failed with error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())