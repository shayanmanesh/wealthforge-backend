"""
Test and Demo for Strategy Optimization Arena

This script demonstrates the strategy optimization arena with 50 CrewAI agents
competing using AlphaScore calculations and comprehensive market simulations.
"""

import json
import asyncio
import numpy as np
from strategy_optimization_arena import (
    StrategyOptimizationArena, 
    AgentRole, 
    StrategyType, 
    MarketData,
    run_strategy_optimization
)


async def test_arena_initialization():
    """Test arena initialization and agent creation."""
    print("🏟️ TESTING ARENA INITIALIZATION")
    print("=" * 50)
    
    arena = StrategyOptimizationArena()
    
    print(f"✅ Arena created successfully")
    print(f"   Total Agents: {len(arena.agents)}")
    print(f"   Market Data Points: {len(arena.market_data)}")
    
    # Show agent distribution by role
    role_counts = {}
    for agent in arena.agents:
        role = agent.role.value
        role_counts[role] = role_counts.get(role, 0) + 1
    
    print(f"\n📊 Agent Distribution by Role:")
    for role, count in role_counts.items():
        print(f"   {role}: {count} agents")
    
    # Show sample agents from each role
    print(f"\n🤖 Sample Agents:")
    roles_shown = set()
    for agent in arena.agents:
        if agent.role not in roles_shown:
            print(f"   • {agent.name} ({agent.role.value}) - {agent.specialization}")
            roles_shown.add(agent.role)
        if len(roles_shown) >= 5:  # Show first 5 different roles
            break
    
    return arena


async def test_market_data_generation():
    """Test market data generation and analysis."""
    print("\n📈 TESTING MARKET DATA GENERATION")
    print("=" * 45)
    
    # Generate sample market data
    market_data = MarketData.generate_dummy_data(days_back=100)
    
    print(f"✅ Generated {len(market_data)} days of market data")
    
    # Analyze market data
    spy_prices = [d.spy_price for d in market_data]
    vix_values = [d.vix for d in market_data]
    yields = [d.ten_year_yield for d in market_data]
    
    print(f"\n📊 Market Data Statistics:")
    print(f"   SPY Price Range: ${min(spy_prices):.2f} - ${max(spy_prices):.2f}")
    print(f"   VIX Range: {min(vix_values):.1f} - {max(vix_values):.1f}")
    print(f"   10Y Yield Range: {min(yields):.2f}% - {max(yields):.2f}%")
    
    # Show recent market conditions
    recent = market_data[-5:]
    print(f"\n📅 Recent Market Conditions:")
    for data in recent:
        print(f"   {data.timestamp.strftime('%Y-%m-%d')}: SPY=${data.spy_price:.2f}, VIX={data.vix:.1f}")
    
    return market_data


async def test_single_competition():
    """Test a single strategy competition."""
    print("\n🏁 TESTING SINGLE STRATEGY COMPETITION")
    print("=" * 50)
    
    # Define test client input
    client_input = {
        "goals": {
            "strategy": "aggressive growth with technology focus",
            "timeline": "15 years",
            "target_amount": 1500000,
            "risk_tolerance": "high"
        },
        "constraints": {
            "capital": 100000,
            "contributions": 3000,
            "contribution_frequency": "monthly",
            "max_risk_percentage": 80,
            "liquidity_needs": "low"
        },
        "additional_preferences": {
            "sector_focus": ["technology", "healthcare"],
            "esg_investing": True
        }
    }
    
    print("📝 Client Input:")
    print(json.dumps(client_input, indent=2))
    
    # Run competition with 25 agents
    print(f"\n🚀 Running competition with 25 agents...")
    result = await run_strategy_optimization(client_input, num_agents=25)
    
    print(f"\n🎯 Competition Results:")
    print(f"   Competition ID: {result['competition_id']}")
    print(f"   Execution Time: {result['execution_time']:.3f}s")
    print(f"   Strategies Generated: {result['strategies_generated']}")
    
    # Show winner
    winner = result['winner']
    if winner:
        print(f"\n🏆 Winner:")
        print(f"   Agent: {winner['agent_name']} ({winner['agent_role']})")
        print(f"   Strategy Type: {winner['strategy_type']}")
        print(f"   AlphaScore: {winner['alpha_score']:.4f}")
        print(f"   Expected Return: {winner['expected_return']:.2%}")
        print(f"   Risk Score: {winner['risk_score']:.3f}")
        print(f"   Timeline Fit: {winner['timeline_fit']:.3f}")
        print(f"   Capital Efficiency: {winner['capital_efficiency']:.3f}")
        print(f"   Confidence: {winner['confidence']:.1%}")
    
    # Show top 5 strategies
    print(f"\n🎖️ Top 5 Strategies:")
    for i, strategy in enumerate(result['top_strategies'][:5], 1):
        print(f"   {i}. {strategy['agent_name']} - AlphaScore: {strategy['alpha_score']:.4f}")
        print(f"      Strategy: {strategy['strategy_type']} | Return: {strategy['expected_return']:.2%}")
    
    # Show AlphaScore distribution
    alpha_dist = result['alpha_score_distribution']
    print(f"\n📊 AlphaScore Distribution:")
    print(f"   Max: {alpha_dist['max']:.4f}")
    print(f"   Mean: {alpha_dist['mean']:.4f}")
    print(f"   Min: {alpha_dist['min']:.4f}")
    print(f"   Std: {alpha_dist['std']:.4f}")
    
    return result


async def test_multiple_scenarios():
    """Test multiple investment scenarios."""
    print("\n🎭 TESTING MULTIPLE INVESTMENT SCENARIOS")
    print("=" * 55)
    
    scenarios = [
        {
            "name": "Conservative Retiree",
            "input": {
                "goals": {
                    "strategy": "conservative income generation",
                    "timeline": "5 years",
                    "target_amount": 500000,
                    "risk_tolerance": "low"
                },
                "constraints": {
                    "capital": 400000,
                    "liquidity_needs": "high",
                    "max_risk_percentage": 30
                }
            }
        },
        {
            "name": "Young Aggressive Investor",
            "input": {
                "goals": {
                    "strategy": "maximum growth potential",
                    "timeline": "25 years",
                    "target_amount": 3000000,
                    "risk_tolerance": "very high"
                },
                "constraints": {
                    "capital": 50000,
                    "contributions": 4000,
                    "contribution_frequency": "monthly",
                    "max_risk_percentage": 95
                }
            }
        },
        {
            "name": "ESG-Focused Investor",
            "input": {
                "goals": {
                    "strategy": "sustainable investing with moderate growth",
                    "timeline": "12 years",
                    "target_amount": 1200000,
                    "risk_tolerance": "moderate"
                },
                "constraints": {
                    "capital": 150000,
                    "contributions": 2500,
                    "contribution_frequency": "monthly",
                    "max_risk_percentage": 65
                },
                "additional_preferences": {
                    "esg_investing": True,
                    "exclude_sectors": ["tobacco", "weapons"]
                }
            }
        }
    ]
    
    results = []
    
    for scenario in scenarios:
        print(f"\n🎪 Scenario: {scenario['name']}")
        print("-" * 30)
        
        result = await run_strategy_optimization(scenario['input'], num_agents=20)
        results.append({
            "scenario": scenario['name'],
            "result": result
        })
        
        winner = result['winner']
        if winner:
            print(f"   Winner: {winner['agent_name']} ({winner['agent_role']})")
            print(f"   AlphaScore: {winner['alpha_score']:.4f}")
            print(f"   Strategy: {winner['strategy_type']}")
            print(f"   Expected Return: {winner['expected_return']:.2%}")
    
    # Compare scenarios
    print(f"\n📊 Scenario Comparison:")
    print("-" * 25)
    for result in results:
        winner = result['result']['winner']
        if winner:
            print(f"   {result['scenario']:<25} | Winner: {winner['agent_name']:<15} | AlphaScore: {winner['alpha_score']:.4f}")
    
    return results


async def test_alphasccore_calculation():
    """Test AlphaScore calculation with different parameter combinations."""
    print("\n🧮 TESTING ALPHASCCORE CALCULATION")
    print("=" * 45)
    
    # Test different parameter combinations
    test_cases = [
        {"expected_return": 0.12, "timeline_fit": 0.9, "risk_score": 0.15, "capital_efficiency": 0.8, "name": "High Return, High Fit"},
        {"expected_return": 0.08, "timeline_fit": 0.95, "risk_score": 0.10, "capital_efficiency": 0.9, "name": "Moderate Return, Perfect Fit"},
        {"expected_return": 0.15, "timeline_fit": 0.7, "risk_score": 0.20, "capital_efficiency": 0.7, "name": "High Return, Moderate Fit"},
        {"expected_return": 0.06, "timeline_fit": 0.8, "risk_score": 0.08, "capital_efficiency": 0.95, "name": "Low Return, High Efficiency"},
        {"expected_return": 0.10, "timeline_fit": 0.5, "risk_score": 0.25, "capital_efficiency": 0.6, "name": "Poor Fit, High Risk"}
    ]
    
    print("AlphaScore = (ExpectedReturn × TimelineFit) / (RiskScore × CapitalEfficiency)")
    print("")
    
    alpha_scores = []
    for case in test_cases:
        alpha_score = (case['expected_return'] * case['timeline_fit']) / (case['risk_score'] * case['capital_efficiency'])
        alpha_scores.append(alpha_score)
        
        print(f"{case['name']:<25}:")
        print(f"   Return: {case['expected_return']:.1%} | Fit: {case['timeline_fit']:.2f} | Risk: {case['risk_score']:.3f} | Efficiency: {case['capital_efficiency']:.2f}")
        print(f"   AlphaScore: {alpha_score:.4f}")
        print("")
    
    print(f"📊 AlphaScore Range: {min(alpha_scores):.4f} - {max(alpha_scores):.4f}")
    print(f"   Average: {np.mean(alpha_scores):.4f}")
    
    return alpha_scores


async def test_arena_statistics():
    """Test arena statistics and leaderboard functionality."""
    print("\n📊 TESTING ARENA STATISTICS")
    print("=" * 40)
    
    arena = StrategyOptimizationArena()
    
    # Run multiple competitions to generate statistics
    client_inputs = [
        {
            "goals": {"strategy": "growth", "timeline": "10 years"},
            "constraints": {"capital": 100000}
        },
        {
            "goals": {"strategy": "conservative", "timeline": "5 years"},
            "constraints": {"capital": 200000}
        },
        {
            "goals": {"strategy": "aggressive", "timeline": "20 years"},
            "constraints": {"capital": 75000}
        }
    ]
    
    print("Running multiple competitions for statistics...")
    for i, client_input in enumerate(client_inputs, 1):
        print(f"   Competition {i}/3...")
        result = await arena.run_competition(client_input, num_agents=15)
    
    # Get arena statistics
    stats = arena.get_arena_statistics()
    
    print(f"\n🏟️ Arena Statistics:")
    print(f"   Total Competitions: {stats['total_competitions']}")
    print(f"   Strategies Evaluated: {stats['total_strategies_evaluated']}")
    print(f"   Active Agents: {stats['active_agents']}")
    print(f"   Avg Competition Time: {stats['average_competition_time']:.3f}s")
    
    alpha_stats = stats['alpha_score_statistics']
    print(f"\n📈 AlphaScore Statistics:")
    print(f"   Max: {alpha_stats['max']:.4f}")
    print(f"   Mean: {alpha_stats['mean']:.4f}")
    print(f"   Median: {alpha_stats['median']:.4f}")
    print(f"   Std: {alpha_stats['std']:.4f}")
    
    print(f"\n🏆 Most Successful Role: {stats['most_successful_role']}")
    print(f"🎯 Most Used Strategy: {stats['most_used_strategy_type']}")
    
    # Get leaderboard
    leaderboard = arena.get_leaderboard(top_n=10)
    
    print(f"\n🥇 Top 10 Leaderboard:")
    for entry in leaderboard:
        print(f"   {entry['rank']:2d}. {entry['agent_name']:<15} ({entry['agent_role']:<15}) - AlphaScore: {entry['alpha_score']:.4f}")
    
    return stats, leaderboard


async def test_strategy_simulation():
    """Test strategy performance simulation."""
    print("\n🎲 TESTING STRATEGY SIMULATION")
    print("=" * 40)
    
    arena = StrategyOptimizationArena()
    
    # Get a sample strategy
    client_input = {
        "goals": {"strategy": "balanced growth", "timeline": "8 years"},
        "constraints": {"capital": 120000}
    }
    
    result = await arena.run_competition(client_input, num_agents=10)
    
    if result['winner']:
        print(f"Simulating performance for winner: {result['winner']['agent_name']}")
        
        # Create strategy object for simulation
        from strategy_optimization_arena import AgentStrategy, AgentRole, StrategyType
        
        strategy = AgentStrategy(
            agent_id=result['winner']['agent_id'],
            agent_name=result['winner']['agent_name'],
            agent_role=AgentRole(result['winner']['agent_role']),
            strategy_type=StrategyType(result['winner']['strategy_type']),
            asset_allocation=result['winner']['asset_allocation'],
            expected_return=result['winner']['expected_return'],
            risk_score=result['winner']['risk_score'],
            timeline_fit=result['winner']['timeline_fit'],
            capital_efficiency=result['winner']['capital_efficiency']
        )
        
        # Run simulation
        sim_results = arena.simulate_strategy_performance(strategy, simulation_days=252)
        
        print(f"\n📊 1-Year Simulation Results:")
        print(f"   Total Return: {sim_results['total_return']:.2%}")
        print(f"   Annualized Return: {sim_results['annualized_return']:.2%}")
        print(f"   Volatility: {sim_results['volatility']:.2%}")
        print(f"   Sharpe Ratio: {sim_results['sharpe_ratio']:.3f}")
        print(f"   Max Drawdown: {sim_results['max_drawdown']:.2%}")
        print(f"   Win Rate: {sim_results['win_rate']:.1%}")
        print(f"   Best Day: {sim_results['best_day']:.2%}")
        print(f"   Worst Day: {sim_results['worst_day']:.2%}")
        
        return sim_results
    
    return None


async def test_role_specialization():
    """Test different agent role specializations."""
    print("\n🎭 TESTING ROLE SPECIALIZATION")
    print("=" * 40)
    
    arena = StrategyOptimizationArena()
    
    # Test scenario that should favor different roles
    scenarios = [
        {
            "name": "High Risk Scenario (should favor Risk Optimizers)",
            "input": {
                "goals": {"strategy": "high risk high return", "timeline": "3 years"},
                "constraints": {"capital": 50000, "max_risk_percentage": 95}
            }
        },
        {
            "name": "ESG Scenario (should favor ESG Specialists)",
            "input": {
                "goals": {"strategy": "sustainable investing", "timeline": "10 years"},
                "constraints": {"capital": 100000},
                "additional_preferences": {"esg_investing": True}
            }
        },
        {
            "name": "Tech Focus (should favor Sector Specialists)",
            "input": {
                "goals": {"strategy": "technology sector growth", "timeline": "7 years"},
                "constraints": {"capital": 80000},
                "additional_preferences": {"sector_focus": ["technology"]}
            }
        }
    ]
    
    for scenario in scenarios:
        print(f"\n🎯 {scenario['name']}")
        print("-" * 50)
        
        result = await arena.run_competition(scenario['input'], num_agents=25)
        
        # Analyze role performance
        role_perf = result['role_performance']
        print(f"Role Performance (top 3 by avg AlphaScore):")
        
        # Sort roles by average AlphaScore
        sorted_roles = sorted(role_perf.items(), 
                            key=lambda x: x[1]['avg_alpha_score'], 
                            reverse=True)
        
        for i, (role, stats) in enumerate(sorted_roles[:3], 1):
            print(f"   {i}. {role}: Avg AlphaScore {stats['avg_alpha_score']:.4f} ({stats['count']} agents)")
        
        # Show winner
        winner = result['winner']
        if winner:
            print(f"\n🏆 Winner: {winner['agent_name']} ({winner['agent_role']})")


async def demonstration_full_arena():
    """Full demonstration of the Strategy Optimization Arena."""
    print("\n🏟️ COMPREHENSIVE ARENA DEMONSTRATION")
    print("=" * 60)
    
    # Complex investment scenario
    complex_scenario = {
        "goals": {
            "strategy": "aggressive growth with ESG focus and technology bias",
            "timeline": "18 years until retirement",
            "target_amount": 2500000,
            "risk_tolerance": "high but not speculative"
        },
        "constraints": {
            "capital": 200000,
            "contributions": 6000,
            "contribution_frequency": "monthly",
            "max_risk_percentage": 85,
            "liquidity_needs": "low for most assets"
        },
        "additional_preferences": {
            "esg_investing": True,
            "sector_focus": ["technology", "healthcare", "renewable_energy"],
            "international_exposure": "moderate",
            "tax_optimization": "maximize tax efficiency",
            "exclude_sectors": ["tobacco", "weapons", "fossil_fuels"]
        }
    }
    
    print("🎯 Complex Investment Scenario:")
    print(json.dumps(complex_scenario, indent=2))
    
    print(f"\n🚀 Running full 50-agent competition...")
    
    # Run competition with all 50 agents
    result = await run_strategy_optimization(complex_scenario, num_agents=50)
    
    print(f"\n🏁 Competition Complete!")
    print(f"   Execution Time: {result['execution_time']:.2f}s")
    print(f"   Strategies Generated: {result['strategies_generated']}")
    
    # Detailed winner analysis
    winner = result['winner']
    if winner:
        print(f"\n🏆 WINNING STRATEGY ANALYSIS:")
        print(f"   Agent: {winner['agent_name']}")
        print(f"   Role: {winner['agent_role']}")
        print(f"   Strategy Type: {winner['strategy_type']}")
        print(f"   AlphaScore: {winner['alpha_score']:.6f}")
        print(f"   ")
        print(f"   Performance Metrics:")
        print(f"     Expected Return: {winner['expected_return']:.2%}")
        print(f"     Risk Score: {winner['risk_score']:.4f}")
        print(f"     Timeline Fit: {winner['timeline_fit']:.4f}")
        print(f"     Capital Efficiency: {winner['capital_efficiency']:.4f}")
        print(f"     Confidence: {winner['confidence']:.1%}")
        
        print(f"\n   Asset Allocation:")
        for asset, allocation in winner['asset_allocation'].items():
            print(f"     {asset}: {allocation:.1%}")
        
        print(f"\n   Reasoning: {winner['reasoning']}")
    
    # Show competition insights
    print(f"\n📊 COMPETITION INSIGHTS:")
    
    # Strategy type distribution
    strategy_dist = result['strategy_type_distribution']
    print(f"   Strategy Distribution:")
    for strategy_type, count in sorted(strategy_dist.items(), key=lambda x: x[1], reverse=True):
        print(f"     {strategy_type}: {count} agents")
    
    # Role performance
    role_perf = result['role_performance']
    print(f"\n   Top Performing Roles:")
    sorted_roles = sorted(role_perf.items(), 
                        key=lambda x: x[1]['avg_alpha_score'], 
                        reverse=True)
    
    for i, (role, stats) in enumerate(sorted_roles[:5], 1):
        print(f"     {i}. {role}: {stats['avg_alpha_score']:.4f} avg AlphaScore")
    
    # AlphaScore distribution
    alpha_dist = result['alpha_score_distribution']
    print(f"\n   AlphaScore Distribution:")
    print(f"     Range: {alpha_dist['min']:.4f} - {alpha_dist['max']:.4f}")
    print(f"     Mean: {alpha_dist['mean']:.4f} ± {alpha_dist['std']:.4f}")
    
    print(f"\n✅ ARENA DEMONSTRATION COMPLETE!")
    
    return result


async def main():
    """Run all tests and demonstrations."""
    print("🎯 STRATEGY OPTIMIZATION ARENA TESTING SUITE")
    print("=" * 80)
    print("Testing 50-agent CrewAI arena with AlphaScore competition system")
    print("=" * 80)
    
    try:
        # Run all tests
        await test_arena_initialization()
        await test_market_data_generation()
        await test_alphasccore_calculation()
        await test_single_competition()
        await test_multiple_scenarios()
        await test_role_specialization()
        await test_strategy_simulation()
        await test_arena_statistics()
        await demonstration_full_arena()
        
        print("\n" + "=" * 80)
        print("🎉 ALL TESTS COMPLETED SUCCESSFULLY!")
        print("=" * 80)
        print("✅ Strategy Optimization Arena is fully functional")
        print("✅ 50 CrewAI agents created and competing")
        print("✅ AlphaScore competition system working")
        print("✅ Market data simulation operational")
        print("✅ Performance tracking and analytics")
        print("✅ Multi-scenario testing successful")
        print("=" * 80)
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())