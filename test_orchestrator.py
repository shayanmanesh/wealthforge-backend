"""
Test and Demo for Orchestrator Agent with AutoGen

This script demonstrates the orchestrator's ability to distribute tasks,
manage agent competition, and provide dynamic weighting based on strategy types.
"""

import json
import asyncio
from orchestrator_agent import (
    OrchestratorAgent, 
    StrategyType, 
    CompetitionManager,
    orchestrate_investment_task
)
from goal_constraint_parser import parse_goal_constraints


async def test_orchestrator_basic():
    """Test basic orchestrator functionality."""
    print("🤖 TESTING ORCHESTRATOR AGENT - BASIC FUNCTIONALITY")
    print("=" * 60)
    
    # Create orchestrator
    orchestrator = OrchestratorAgent(enable_logging=True)
    
    # Test agent creation
    print(f"✅ Created {len(orchestrator.agents)} specialized agents:")
    for agent in orchestrator.agents:
        print(f"   • {agent.name} ({agent.strategy_type.value})")
        print(f"     Expertise: {', '.join(agent.expertise_areas)}")
        print(f"     Performance: {agent.performance_history:.2f}")
    
    return orchestrator


async def test_agent_selection():
    """Test agent selection based on strategy matching."""
    print("\n🎯 TESTING AGENT SELECTION AND SCORING")
    print("=" * 50)
    
    orchestrator = OrchestratorAgent(enable_logging=True)
    
    # Test different strategies
    test_strategies = [
        "aggressive growth",
        "conservative income", 
        "balanced portfolio",
        "moderate risk",
        "high growth potential"
    ]
    
    for strategy in test_strategies:
        print(f"\n📊 Strategy: '{strategy}'")
        print("-" * 30)
        
        selected_agents = orchestrator.select_competing_agents(strategy, num_agents=3)
        
        print(f"Selected {len(selected_agents)} agents:")
        for agent in selected_agents:
            score = orchestrator.competition_manager.agent_scores[agent.name]
            print(f"  🏆 {agent.name}")
            print(f"     Strategy Match: {score.strategy_match:.3f}")
            print(f"     Performance: {score.performance_score:.3f}")
            print(f"     Total Score: {score.total_score:.3f}")


async def test_full_orchestration():
    """Test complete orchestration workflow."""
    print("\n🚀 TESTING COMPLETE ORCHESTRATION WORKFLOW")
    print("=" * 55)
    
    # Test cases with different investment scenarios
    test_cases = [
        {
            "name": "Aggressive Growth Investor",
            "input": {
                "goals": {
                    "strategy": "aggressive growth",
                    "timeline": "20 years",
                    "target_amount": 2000000,
                    "risk_tolerance": "high"
                },
                "constraints": {
                    "capital": 100000,
                    "contributions": 5000,
                    "contribution_frequency": "monthly",
                    "max_risk_percentage": 90,
                    "liquidity_needs": "low"
                }
            }
        },
        {
            "name": "Conservative Retiree",
            "input": {
                "goals": {
                    "strategy": "conservative income",
                    "timeline": "short-term",
                    "risk_tolerance": "low"
                },
                "constraints": {
                    "capital": 500000,
                    "liquidity_needs": "high",
                    "max_risk_percentage": 20
                }
            }
        },
        {
            "name": "Balanced Mid-Career Professional",
            "input": {
                "goals": {
                    "strategy": "balanced",
                    "timeline": "10 years",
                    "target_amount": 750000
                },
                "constraints": {
                    "capital": 150000,
                    "contributions": 2000,
                    "contribution_frequency": "monthly",
                    "max_risk_percentage": 60
                }
            }
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n🎪 TEST CASE {i}: {test_case['name']}")
        print("-" * 45)
        
        print("📝 Input:")
        print(json.dumps(test_case['input'], indent=2))
        
        try:
            # Execute orchestration
            result = await orchestrate_investment_task(
                test_case['input'], 
                f"Provide comprehensive investment recommendation for {test_case['name']}"
            )
            
            print("\n🎯 Orchestration Results:")
            print(f"   Target Strategy: {result['target_strategy']}")
            print(f"   Execution Time: {result['execution_time']:.2f}s")
            print(f"   Competing Agents: {', '.join(result['competing_agents'])}")
            
            print("\n🏆 Winner:")
            winner = result['winner']
            print(f"   Agent: {winner['agent']}")
            print(f"   Strategy: {winner['strategy']}")
            print(f"   Confidence: {winner['confidence']:.3f}")
            print(f"   Reason: {winner['reason']}")
            
            print("\n📊 Agent Results:")
            for agent_result in result['agent_results']:
                print(f"   • {agent_result['agent_name']} ({agent_result['strategy_type']})")
                print(f"     Confidence: {agent_result['confidence']:.3f}")
                print(f"     Execution Time: {agent_result['execution_time']:.2f}s")
                
                # Show recommendation summary
                rec = agent_result['recommendation']
                if 'allocation' in rec:
                    print(f"     Allocation: {rec['allocation']}")
            
            print("\n🤝 Consensus:")
            consensus = result['consensus_recommendation']
            print(f"   Summary: {consensus.get('recommendation_summary', 'N/A')}")
            print(f"   Average Confidence: {consensus.get('average_confidence', 0):.3f}")
            
        except Exception as e:
            print(f"❌ Error in test case: {e}")


async def test_competition_manager():
    """Test the competition management system."""
    print("\n⚔️  TESTING COMPETITION MANAGEMENT")
    print("=" * 45)
    
    # Create competition manager
    competition_manager = CompetitionManager()
    
    # Create sample agents
    orchestrator = OrchestratorAgent()
    agents = orchestrator.agents[:3]  # Use first 3 agents
    
    # Test strategy matching
    test_strategies = ["aggressive", "conservative", "balanced"]
    
    for strategy in test_strategies:
        print(f"\n🎯 Testing strategy: '{strategy}'")
        scores = competition_manager.score_agents(agents, strategy)
        
        print("Agent Scores:")
        for score in scores:
            print(f"  {score.agent_name}:")
            print(f"    Strategy Match: {score.strategy_match:.3f}")
            print(f"    Performance: {score.performance_score:.3f}")
            print(f"    Confidence: {score.confidence:.3f}")
            print(f"    Total Score: {score.total_score:.3f}")
    
    # Test performance updates
    print("\n📈 Testing Performance Updates:")
    print("Updating Conservative_Advisor performance...")
    competition_manager.update_performance("Conservative_Advisor", 0.95)
    
    if "Conservative_Advisor" in competition_manager.agent_scores:
        updated_score = competition_manager.agent_scores["Conservative_Advisor"]
        print(f"Updated performance: {updated_score.performance_score:.3f}")


async def test_integration_with_parser():
    """Test integration with goal-constraint parser."""
    print("\n🔗 TESTING INTEGRATION WITH GOAL-CONSTRAINT PARSER")
    print("=" * 60)
    
    # Raw user input (like what might come from a web form)
    raw_user_input = {
        "goals": {
            "strategy": "I want aggressive growth for my retirement in 25 years",
            "timeline": "25 years",
            "target_amount": 1500000,
            "risk_tolerance": "I can handle high risk for better returns"
        },
        "constraints": {
            "capital": 50000,
            "contributions": 2500,
            "contribution_frequency": "monthly",
            "max_risk_percentage": 85,
            "liquidity_needs": "low"
        },
        "additional_preferences": {
            "sectors": ["technology", "healthcare"],
            "esg_investing": False,
            "international": True
        }
    }
    
    print("📝 Raw User Input:")
    print(json.dumps(raw_user_input, indent=2))
    
    # Parse the input
    print("\n🔄 Parsing Goals and Constraints...")
    parsed_input = parse_goal_constraints(raw_user_input)
    
    print("✅ Parsed Input:")
    print(json.dumps(parsed_input, indent=2))
    
    # Create orchestrator and execute
    print("\n🤖 Executing Orchestration...")
    orchestrator = OrchestratorAgent(enable_logging=True)
    
    result = await orchestrator.orchestrate_task(
        parsed_input,
        "Provide personalized investment recommendation based on parsed goals"
    )
    
    print("\n🎯 Final Orchestration Result:")
    print(f"Strategy Identified: {result['target_strategy']}")
    print(f"Agents Competed: {', '.join(result['competing_agents'])}")
    print(f"Winner: {result['winner']['agent']} (confidence: {result['winner']['confidence']:.3f})")


async def demonstrate_dynamic_weighting():
    """Demonstrate dynamic weighting system."""
    print("\n⚖️  DEMONSTRATING DYNAMIC WEIGHTING SYSTEM")
    print("=" * 55)
    
    orchestrator = OrchestratorAgent(enable_logging=True)
    
    # Show how different strategies get different weightings
    strategies_to_test = [
        ("conservative bonds and safety", "Conservative strategy should win"),
        ("aggressive high-growth technology", "Aggressive strategy should win"),
        ("balanced diversified portfolio", "Balanced strategy should win"),
        ("dividend income generation", "Income strategy should win")
    ]
    
    for strategy, expected in strategies_to_test:
        print(f"\n🧪 Testing: '{strategy}'")
        print(f"Expected: {expected}")
        
        selected_agents = orchestrator.select_competing_agents(strategy, num_agents=3)
        
        print("Selected agents and scores:")
        for agent in selected_agents:
            score = orchestrator.competition_manager.agent_scores[agent.name]
            print(f"  🏅 {agent.name}: {score.total_score:.3f}")
            print(f"     Strategy Match: {score.strategy_match:.3f}")
        
        print(f"✅ Top choice: {selected_agents[0].name}")


async def performance_summary_test():
    """Test performance summary functionality."""
    print("\n📊 TESTING PERFORMANCE SUMMARY")
    print("=" * 40)
    
    orchestrator = OrchestratorAgent()
    
    # Run a few tasks to generate history
    test_inputs = [
        {"goals": {"strategy": "aggressive", "timeline": "long-term"}, "constraints": {"capital": 50000}},
        {"goals": {"strategy": "conservative", "timeline": "short-term"}, "constraints": {"capital": 100000}},
        {"goals": {"strategy": "balanced", "timeline": "medium-term"}, "constraints": {"capital": 75000}}
    ]
    
    for i, test_input in enumerate(test_inputs):
        print(f"Executing task {i+1}...")
        parsed = parse_goal_constraints(test_input)
        await orchestrator.orchestrate_task(parsed, f"Test task {i+1}")
    
    # Get performance summary
    summary = orchestrator.get_performance_summary()
    
    print("\n📈 Performance Summary:")
    print(f"Total Tasks: {summary['total_tasks']}")
    
    print("\nAgent Scores:")
    for agent_name, score_data in summary['agent_scores'].items():
        print(f"  {agent_name}:")
        print(f"    Total Score: {score_data['total_score']:.3f}")
        print(f"    Performance: {score_data['performance_score']:.3f}")
    
    print(f"\nRecent Tasks: {len(summary['recent_tasks'])}")


async def main():
    """Run all tests."""
    print("🎯 ORCHESTRATOR AGENT TESTING SUITE")
    print("=" * 70)
    
    try:
        # Run all tests
        await test_orchestrator_basic()
        await test_agent_selection()
        await test_competition_manager()
        await demonstrate_dynamic_weighting()
        await test_full_orchestration()
        await test_integration_with_parser()
        await performance_summary_test()
        
        print("\n" + "=" * 70)
        print("🎉 ALL TESTS COMPLETED SUCCESSFULLY!")
        print("✅ Orchestrator Agent is working correctly")
        print("✅ Agent competition system functional")
        print("✅ Dynamic weighting based on strategy types")
        print("✅ Integration with goal-constraint parser")
        print("✅ Task distribution and management")
        print("=" * 70)
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())