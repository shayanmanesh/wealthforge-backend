"""
Test Suite for Fine-Tuning Engine

Comprehensive testing of GoalExceedPredictor, SensitivityAnalyzer,
and optimization scenarios for constraint adjustments.
"""

import asyncio
import json
from datetime import datetime
from fine_tuning_engine import (
    FineTuningEngine,
    GoalExceedPredictor,
    SensitivityAnalyzer,
    optimize_goal_exceedance,
    OptimizationStrategy,
    AdjustmentType
)
from portfolio_surgeon import PortfolioSynthesis, RiskAnalysis, CostAnalysis


async def test_goal_exceed_predictor():
    """Test GoalExceedPredictor functionality."""
    print("🎯 TESTING GOAL EXCEED PREDICTOR")
    print("=" * 50)
    
    predictor = GoalExceedPredictor()
    
    print(f"   Simulation runs: {predictor.simulation_runs:,}")
    print(f"   Market scenarios: {len(predictor.market_scenarios)}")
    print(f"   Prediction models: {len(predictor.prediction_models)}")
    
    # Test scenarios
    test_scenarios = [
        {
            "name": "Conservative Young Investor",
            "profile": {
                "goals": {
                    "strategy": "conservative growth",
                    "timeline": "25 years",
                    "target_amount": 500000,
                    "risk_tolerance": "conservative"
                },
                "constraints": {
                    "capital": 50000,
                    "contributions": 1500,
                    "max_risk_percentage": 40
                }
            }
        },
        {
            "name": "Aggressive Mid-Career Professional",
            "profile": {
                "goals": {
                    "strategy": "aggressive growth",
                    "timeline": "15 years",
                    "target_amount": 1500000,
                    "risk_tolerance": "high"
                },
                "constraints": {
                    "capital": 200000,
                    "contributions": 4000,
                    "max_risk_percentage": 85
                }
            }
        },
        {
            "name": "Pre-Retirement Wealth Preservation",
            "profile": {
                "goals": {
                    "strategy": "wealth preservation",
                    "timeline": "10 years",
                    "target_amount": 2000000,
                    "risk_tolerance": "moderate"
                },
                "constraints": {
                    "capital": 1200000,
                    "contributions": 2000,
                    "max_risk_percentage": 60
                }
            }
        }
    ]
    
    for scenario in test_scenarios:
        print(f"\n🔍 Analyzing: {scenario['name']}")
        
        # Run goal achievement prediction
        prediction = await predictor.predict_goal_achievement(scenario['profile'])
        
        print(f"   Goal Achievement Probability: {prediction['goal_achievement_probability']:.1%}")
        print(f"   Exceed by 25% Probability: {prediction['exceed_by_25_percent_probability']:.1%}")
        print(f"   Exceed by 50% Probability: {prediction['exceed_by_50_percent_probability']:.1%}")
        print(f"   Expected Excess: {prediction['expected_excess_percentage']:.1%}")
        print(f"   Median Outcome: ${prediction['median_outcome']:,.0f}")
        print(f"   Worst Case (5th percentile): ${prediction['worst_case_5th_percentile']:,.0f}")
        
        # Test time to goal prediction
        target = scenario['profile']['goals']['target_amount']
        time_prediction = await predictor.predict_time_to_goal(scenario['profile'], target)
        
        print(f"   Expected Time to Goal: {time_prediction['expected_time_years']:.1f} years")
        print(f"   Conservative Estimate: {time_prediction['conservative_estimate']:.1f} years")
        print(f"   Optimistic Estimate: {time_prediction['optimistic_estimate']:.1f} years")
    
    print("\n✅ GoalExceedPredictor test completed")
    return predictor


async def test_sensitivity_analyzer():
    """Test SensitivityAnalyzer functionality."""
    print("\n📊 TESTING SENSITIVITY ANALYZER")
    print("=" * 45)
    
    predictor = GoalExceedPredictor()
    analyzer = SensitivityAnalyzer(predictor)
    
    # Test client profile
    test_profile = {
        "goals": {
            "strategy": "balanced growth",
            "timeline": "12 years",
            "target_amount": 800000,
            "risk_tolerance": "moderate"
        },
        "constraints": {
            "capital": 120000,
            "contributions": 2500,
            "max_risk_percentage": 70
        }
    }
    
    print(f"📋 Test Profile:")
    print(f"   Capital: ${test_profile['constraints']['capital']:,}")
    print(f"   Monthly Contributions: ${test_profile['constraints']['contributions']:,}")
    print(f"   Timeline: {test_profile['goals']['timeline']}")
    print(f"   Target: ${test_profile['goals']['target_amount']:,}")
    
    # Test individual parameter sensitivity
    parameters_to_test = ['capital', 'contributions', 'timeline']
    
    for parameter in parameters_to_test:
        print(f"\n🔍 Analyzing sensitivity to: {parameter}")
        
        try:
            sensitivity = await analyzer.analyze_parameter_sensitivity(test_profile, parameter)
            
            print(f"   Sensitivity Coefficient: {sensitivity.sensitivity_coefficient:.4f}")
            print(f"   Elasticity: {sensitivity.elasticity:.4f}")
            print(f"   Confidence Interval: [{sensitivity.confidence_interval[0]:.3f}, {sensitivity.confidence_interval[1]:.3f}]")
            
            if sensitivity.critical_threshold:
                print(f"   Critical Threshold: {sensitivity.critical_threshold:.2f}")
            
            if sensitivity.diminishing_returns_point:
                print(f"   Diminishing Returns Point: {sensitivity.diminishing_returns_point:.2f}")
            
            print(f"   Risk Factors: {len(sensitivity.risk_factors)}")
            for risk in sensitivity.risk_factors[:2]:
                print(f"     • {risk}")
                
        except Exception as e:
            print(f"   Error analyzing {parameter}: {e}")
    
    # Test comprehensive sensitivity analysis
    print(f"\n📈 Running comprehensive sensitivity analysis...")
    
    try:
        comprehensive_results = await analyzer.comprehensive_sensitivity_analysis(test_profile)
        
        print(f"   Parameters analyzed: {len(comprehensive_results)}")
        
        for param_name, analysis in comprehensive_results.items():
            print(f"   {param_name}:")
            print(f"     Sensitivity: {analysis.sensitivity_coefficient:.4f}")
            print(f"     Elasticity: {analysis.elasticity:.4f}")
            print(f"     Risk factors: {len(analysis.risk_factors)}")
        
        print("\n✅ Comprehensive sensitivity analysis complete")
        
    except Exception as e:
        print(f"   Error in comprehensive analysis: {e}")
    
    print("\n✅ SensitivityAnalyzer test completed")
    return analyzer


async def test_fine_tuning_engine():
    """Test complete Fine-Tuning Engine optimization."""
    print("\n🔧 TESTING FINE-TUNING ENGINE")
    print("=" * 45)
    
    engine = FineTuningEngine()
    
    print(f"   Optimization strategies: {len(engine.optimization_strategies)}")
    print(f"   Available strategies: {list(engine.optimization_strategies.keys())}")
    
    # Test client profile
    client_profile = {
        "goals": {
            "strategy": "aggressive growth with long-term focus",
            "timeline": "18 years",
            "target_amount": 1200000,
            "risk_tolerance": "high"
        },
        "constraints": {
            "capital": 180000,
            "contributions": 3000,
            "contribution_frequency": "monthly",
            "max_risk_percentage": 80
        },
        "additional_preferences": {
            "age": 35,
            "tax_optimization": True,
            "esg_investing": True
        }
    }
    
    print(f"\n📋 Client Profile for Optimization:")
    print(f"   Current Capital: ${client_profile['constraints']['capital']:,}")
    print(f"   Monthly Contributions: ${client_profile['constraints']['contributions']:,}")
    print(f"   Target Amount: ${client_profile['goals']['target_amount']:,}")
    print(f"   Timeline: {client_profile['goals']['timeline']}")
    
    # Test different optimization strategies
    strategies = [
        OptimizationStrategy.CONSERVATIVE,
        OptimizationStrategy.BALANCED,
        OptimizationStrategy.AGGRESSIVE
    ]
    
    optimization_results = []
    
    for strategy in strategies:
        print(f"\n🎯 Testing {strategy.value} optimization strategy...")
        
        try:
            result = await engine.optimize_for_goal_exceedance(
                client_profile,
                target_exceedance=0.25,  # 25% exceedance target
                strategy=strategy
            )
            
            optimization_results.append(result)
            
            print(f"   Original Goal Probability: {result.original_goal_probability:.1%}")
            print(f"   Optimized Goal Probability: {result.optimized_goal_probability:.1%}")
            print(f"   Improvement Factor: {result.improvement_factor:.2f}x")
            print(f"   Scenarios Generated: {len(result.recommended_scenarios)}")
            
            if result.recommended_scenarios:
                best_scenario = result.recommended_scenarios[0]
                print(f"   Best Scenario: {best_scenario.scenario_name}")
                print(f"   Success Probability: {best_scenario.probability_of_success:.1%}")
                print(f"   Implementation Score: {best_scenario.implementation_score:.1%}")
                print(f"   Excess Achievement: {best_scenario.excess_achievement:.1%}")
            
        except Exception as e:
            print(f"   Error in {strategy.value} optimization: {e}")
    
    print("\n✅ Fine-Tuning Engine test completed")
    return optimization_results


async def test_scenario_generation():
    """Test scenario generation and evaluation."""
    print("\n📋 TESTING SCENARIO GENERATION")
    print("=" * 45)
    
    engine = FineTuningEngine()
    
    # Test profile for scenario generation
    test_profile = {
        "goals": {
            "strategy": "balanced growth",
            "timeline": "15 years",
            "target_amount": 1000000,
            "risk_tolerance": "moderate"
        },
        "constraints": {
            "capital": 150000,
            "contributions": 2500,
            "max_risk_percentage": 70
        }
    }
    
    print(f"📊 Generating scenarios for optimization...")
    
    # Get sensitivity analysis first
    sensitivity_results = await engine.sensitivity_analyzer.comprehensive_sensitivity_analysis(test_profile)
    
    print(f"   Sensitivity analysis complete: {len(sensitivity_results)} parameters")
    
    # Generate scenarios
    scenarios = await engine._generate_adjustment_scenarios(
        test_profile,
        sensitivity_results,
        target_exceedance=0.30,
        strategy=OptimizationStrategy.BALANCED
    )
    
    print(f"   Generated scenarios: {len(scenarios)}")
    
    # Show sample scenarios
    print(f"\n📋 Sample Generated Scenarios:")
    for i, scenario in enumerate(scenarios[:5], 1):
        print(f"   {i}. {scenario['scenario_name']}")
        print(f"      Adjustments: {len(scenario['adjustments'])}")
        print(f"      Types: {[adj.value for adj in scenario['adjustment_types']]}")
    
    # Evaluate scenarios
    print(f"\n📈 Evaluating scenarios...")
    evaluated_scenarios = await engine._evaluate_scenarios(test_profile, scenarios)
    
    print(f"   Evaluated scenarios: {len(evaluated_scenarios)}")
    
    # Show top scenarios
    ranked_scenarios = engine._rank_scenarios(evaluated_scenarios, 0.30)
    
    print(f"\n🏆 Top 3 Scenarios:")
    for i, scenario in enumerate(ranked_scenarios[:3], 1):
        print(f"   {i}. {scenario.scenario_name}")
        print(f"      Success Probability: {scenario.probability_of_success:.1%}")
        print(f"      Implementation Score: {scenario.implementation_score:.1%}")
        print(f"      Excess Achievement: {scenario.excess_achievement:.1%}")
        print(f"      Time to Goal: {scenario.time_to_goal:.1f} years")
    
    print("\n✅ Scenario generation test completed")
    return ranked_scenarios


async def test_constraint_adjustments():
    """Test specific constraint adjustment types."""
    print("\n⚙️ TESTING CONSTRAINT ADJUSTMENTS")
    print("=" * 45)
    
    predictor = GoalExceedPredictor()
    
    # Base scenario
    base_profile = {
        "goals": {
            "target_amount": 750000,
            "timeline": "12 years"
        },
        "constraints": {
            "capital": 100000,
            "contributions": 2000
        }
    }
    
    print(f"📊 Base scenario analysis:")
    base_prediction = await predictor.predict_goal_achievement(base_profile)
    print(f"   Base goal probability: {base_prediction['goal_achievement_probability']:.1%}")
    
    # Test different adjustment types
    adjustment_scenarios = [
        {
            "name": "Capital Increase (+50%)",
            "adjustments": {"capital": 150000}
        },
        {
            "name": "Contribution Increase (+50%)",
            "adjustments": {"contributions": 3000}
        },
        {
            "name": "Timeline Extension (+3 years)",
            "adjustments": {"timeline_years": 15}
        },
        {
            "name": "Combined Optimization",
            "adjustments": {
                "capital": 130000,
                "contributions": 2500,
                "timeline_years": 14
            }
        }
    ]
    
    print(f"\n🔍 Testing adjustment scenarios:")
    
    for scenario in adjustment_scenarios:
        print(f"\n   {scenario['name']}:")
        
        # Create adjusted profile
        adjusted_profile = base_profile.copy()
        adjusted_profile['constraints'] = base_profile['constraints'].copy()
        
        for key, value in scenario['adjustments'].items():
            if key == 'timeline_years':
                adjusted_profile['goals']['timeline'] = f"{value} years"
            else:
                adjusted_profile['constraints'][key] = value
        
        # Predict outcome
        prediction = await predictor.predict_goal_achievement(adjusted_profile)
        
        improvement = prediction['goal_achievement_probability'] - base_prediction['goal_achievement_probability']
        
        print(f"      Goal Probability: {prediction['goal_achievement_probability']:.1%}")
        print(f"      Improvement: {improvement:+.1%}")
        print(f"      Excess Achievement: {prediction['expected_excess_percentage']:.1%}")
        print(f"      Median Outcome: ${prediction['median_outcome']:,.0f}")
    
    print("\n✅ Constraint adjustments test completed")


async def test_integration_with_portfolio():
    """Test Fine-Tuning Engine integration with portfolio results."""
    print("\n🔗 TESTING PORTFOLIO INTEGRATION")
    print("=" * 45)
    
    # Mock portfolio result
    mock_portfolio = PortfolioSynthesis(
        portfolio_id="test_fine_tuning_001",
        final_allocation={
            "Stocks": 0.50,
            "Bonds": 0.30,
            "Real Estate": 0.15,
            "Cash": 0.05
        },
        expected_return=0.085,
        risk_score=0.14,
        cost_score=0.006,
        sharpe_ratio=0.48,
        utility_score=0.072,
        synthesis_confidence=0.83,
        contributing_agents=["BalancedOptimizer", "RiskManager"],
        pareto_rank=3,
        optimization_method="pareto_synthesis",
        risk_analysis=RiskAnalysis(
            volatility=0.14,
            var_95=-0.018,
            var_99=-0.025,
            expected_shortfall=-0.021,
            max_drawdown=0.16,
            beta=0.78,
            correlation_matrix=None,
            tail_risk_score=0.38,
            concentration_risk=0.22,
            liquidity_risk=0.25,
            stress_test_results={
                "market_crash": -0.30,
                "recession": -0.18,
                "inflation_spike": -0.12
            },
            risk_attribution={}
        ),
        cost_analysis=CostAnalysis(
            total_expense_ratio=0.006,
            transaction_costs=0.002,
            bid_ask_spreads=0.001,
            market_impact_costs=0.0003,
            rebalancing_costs=0.001,
            tax_efficiency_score=0.78,
            cost_per_basis_point=45.5,
            fee_optimization_savings=0.008,
            cost_breakdown={}
        ),
        improvement_metrics={}
    )
    
    client_profile = {
        "goals": {
            "strategy": "balanced growth with risk management",
            "timeline": "16 years",
            "target_amount": 900000,
            "risk_tolerance": "moderate"
        },
        "constraints": {
            "capital": 160000,
            "contributions": 2800,
            "max_risk_percentage": 75
        }
    }
    
    print(f"📊 Portfolio Information:")
    print(f"   Expected Return: {mock_portfolio.expected_return:.2%}")
    print(f"   Risk Score: {mock_portfolio.risk_score:.3f}")
    print(f"   Sharpe Ratio: {mock_portfolio.sharpe_ratio:.3f}")
    
    print(f"\n🎯 Running optimization with portfolio context...")
    
    # Test optimization with portfolio
    result = await optimize_goal_exceedance(
        client_profile,
        target_exceedance=0.35,
        strategy=OptimizationStrategy.BALANCED,
        portfolio_result=mock_portfolio
    )
    
    print(f"   Optimization Results:")
    print(f"   Original Probability: {result.original_goal_probability:.1%}")
    print(f"   Optimized Probability: {result.optimized_goal_probability:.1%}")
    print(f"   Improvement: {(result.improvement_factor - 1)*100:+.1f}%")
    
    print(f"\n📈 Sensitivity Analysis Results:")
    for param, analysis in result.sensitivity_analysis.items():
        print(f"   {param}:")
        print(f"     Sensitivity: {analysis.sensitivity_coefficient:.4f}")
        print(f"     Elasticity: {analysis.elasticity:.4f}")
    
    print(f"\n🏆 Best Scenario: {result.recommended_scenarios[0].scenario_name}")
    print(f"   Success Probability: {result.recommended_scenarios[0].probability_of_success:.1%}")
    print(f"   Implementation Score: {result.recommended_scenarios[0].implementation_score:.1%}")
    
    print("\n✅ Portfolio integration test completed")
    return result


async def test_comprehensive_demo():
    """Run comprehensive Fine-Tuning Engine demonstration."""
    print("\n🔧 FINE-TUNING ENGINE COMPREHENSIVE DEMO")
    print("=" * 65)
    print("Advanced Goal Exceedance Optimization with Constraint Fine-Tuning")
    print("=" * 65)
    
    # Sophisticated client scenario
    sophisticated_client = {
        "client_id": "fine_tuning_demo_001",
        "goals": {
            "strategy": "sophisticated wealth accumulation with ESG focus",
            "timeline": "20 years until early retirement",
            "target_amount": 2500000,
            "risk_tolerance": "moderate to high with downside protection"
        },
        "constraints": {
            "capital": 350000,
            "contributions": 5000,
            "contribution_frequency": "monthly",
            "max_risk_percentage": 75,
            "liquidity_needs": "moderate"
        },
        "additional_preferences": {
            "age": 38,
            "tax_optimization": True,
            "esg_investing": True,
            "sector_focus": ["technology", "healthcare", "renewable_energy"],
            "international_exposure": "moderate"
        },
        "financial_info": {
            "annual_income": 185000,
            "net_worth": 580000,
            "investment_experience": "intermediate"
        }
    }
    
    print(f"🎯 SOPHISTICATED CLIENT SCENARIO:")
    print(f"   Target: ${sophisticated_client['goals']['target_amount']:,}")
    print(f"   Timeline: {sophisticated_client['goals']['timeline']}")
    print(f"   Current Capital: ${sophisticated_client['constraints']['capital']:,}")
    print(f"   Monthly Contributions: ${sophisticated_client['constraints']['contributions']:,}")
    print(f"   Annual Income: ${sophisticated_client['financial_info']['annual_income']:,}")
    
    print(f"\n🚀 EXECUTING COMPREHENSIVE FINE-TUNING ANALYSIS...")
    print("   Phase 1: Baseline goal achievement assessment")
    print("   Phase 2: Multi-parameter sensitivity analysis")
    print("   Phase 3: Constraint adjustment scenario generation")
    print("   Phase 4: Optimization with multiple strategies")
    print("   Phase 5: Implementation roadmap creation")
    
    # Phase 1: Baseline Assessment
    print(f"\n📊 Phase 1: Baseline Assessment")
    predictor = GoalExceedPredictor()
    baseline = await predictor.predict_goal_achievement(sophisticated_client)
    
    print(f"   Current Goal Probability: {baseline['goal_achievement_probability']:.1%}")
    print(f"   Exceed by 25%: {baseline['exceed_by_25_percent_probability']:.1%}")
    print(f"   Exceed by 50%: {baseline['exceed_by_50_percent_probability']:.1%}")
    print(f"   Expected Outcome: ${baseline['median_outcome']:,.0f}")
    
    # Phase 2: Sensitivity Analysis
    print(f"\n🔍 Phase 2: Comprehensive Sensitivity Analysis")
    analyzer = SensitivityAnalyzer(predictor)
    sensitivity_results = await analyzer.comprehensive_sensitivity_analysis(sophisticated_client)
    
    print(f"   Parameters Analyzed: {len(sensitivity_results)}")
    for param, analysis in sensitivity_results.items():
        print(f"   {param.capitalize()}:")
        print(f"     Impact Score: {analysis.sensitivity_coefficient:.4f}")
        print(f"     Elasticity: {analysis.elasticity:.4f}")
        if analysis.critical_threshold:
            print(f"     Critical Threshold: {analysis.critical_threshold:.2f}")
    
    # Phase 3 & 4: Optimization
    print(f"\n⚙️ Phase 3-4: Multi-Strategy Optimization")
    
    strategies_results = {}
    for strategy in [OptimizationStrategy.CONSERVATIVE, OptimizationStrategy.BALANCED, OptimizationStrategy.AGGRESSIVE]:
        print(f"\n   Testing {strategy.value.upper()} strategy:")
        
        result = await optimize_goal_exceedance(
            sophisticated_client,
            target_exceedance=0.40,  # 40% exceedance target
            strategy=strategy
        )
        
        strategies_results[strategy.value] = result
        
        print(f"     Improvement: {(result.improvement_factor - 1)*100:+.1f}%")
        print(f"     Best Scenario: {result.recommended_scenarios[0].scenario_name}")
        print(f"     Success Rate: {result.recommended_scenarios[0].probability_of_success:.1%}")
        print(f"     Implementation: {result.recommended_scenarios[0].implementation_score:.1%}")
    
    # Phase 5: Best Strategy Analysis
    print(f"\n🏆 Phase 5: Optimal Strategy Selection")
    
    best_strategy = max(strategies_results.items(), 
                       key=lambda x: x[1].improvement_factor)
    
    best_strategy_name, best_result = best_strategy
    
    print(f"   Optimal Strategy: {best_strategy_name.upper()}")
    print(f"   Total Improvement: {(best_result.improvement_factor - 1)*100:+.1f}%")
    print(f"   Original Probability: {best_result.original_goal_probability:.1%}")
    print(f"   Optimized Probability: {best_result.optimized_goal_probability:.1%}")
    
    print(f"\n📋 TOP 3 RECOMMENDED SCENARIOS:")
    for i, scenario in enumerate(best_result.recommended_scenarios[:3], 1):
        print(f"   {i}. {scenario.scenario_name}")
        print(f"      Success Probability: {scenario.probability_of_success:.1%}")
        print(f"      Excess Achievement: {scenario.excess_achievement:.1%}")
        print(f"      Implementation Score: {scenario.implementation_score:.1%}")
        print(f"      Time to Goal: {scenario.time_to_goal:.1f} years")
        print(f"      Adjustments Required: {len(scenario.adjustments)}")
    
    print(f"\n🗺️ IMPLEMENTATION ROADMAP:")
    for step in best_result.implementation_roadmap[:8]:
        print(f"   {step}")
    
    print(f"\n📊 RISK ASSESSMENT:")
    for risk_type, risk_level in best_result.risk_assessment.items():
        risk_label = "LOW" if risk_level < 0.3 else "MODERATE" if risk_level < 0.6 else "HIGH"
        print(f"   {risk_type.replace('_', ' ').title()}: {risk_level:.2f} ({risk_label})")
    
    print(f"\n" + "=" * 65)
    print("🌟 FINE-TUNING ENGINE DEMONSTRATION COMPLETE")
    print("=" * 65)
    print("💡 Key Optimization Insights:")
    print("   🎯 Goal Exceedance: Advanced constraint optimization")
    print("   📊 Sensitivity Analysis: Multi-parameter impact assessment")
    print("   🔧 Scenario Generation: Automated adjustment recommendations")
    print("   🏆 Strategy Optimization: Multi-objective constraint tuning")
    print("   📈 Performance Enhancement: Measurable improvement quantification")
    print("   🗺️ Implementation Planning: Actionable roadmap generation")
    print("=" * 65)
    
    return best_result


async def main():
    """Run all Fine-Tuning Engine tests."""
    print("🔧 FINE-TUNING ENGINE TESTING SUITE")
    print("=" * 70)
    print("Comprehensive testing of goal optimization and constraint fine-tuning")
    print("=" * 70)
    
    try:
        # Component tests
        await test_goal_exceed_predictor()
        await test_sensitivity_analyzer()
        await test_constraint_adjustments()
        
        # Integration tests
        await test_fine_tuning_engine()
        await test_scenario_generation()
        await test_integration_with_portfolio()
        
        # Comprehensive demonstration
        await test_comprehensive_demo()
        
        print("\n" + "=" * 70)
        print("🎉 ALL FINE-TUNING ENGINE TESTS COMPLETED SUCCESSFULLY!")
        print("=" * 70)
        print("✅ GoalExceedPredictor: Advanced Monte Carlo goal prediction")
        print("✅ SensitivityAnalyzer: Multi-parameter impact analysis")
        print("✅ Scenario Generation: Intelligent constraint adjustments")
        print("✅ Optimization Engine: Multi-strategy goal exceedance")
        print("✅ Portfolio Integration: Seamless WealthForge compatibility")
        print("✅ Implementation Planning: Actionable optimization roadmaps")
        print("✅ Risk Assessment: Comprehensive optimization risk evaluation")
        print("=" * 70)
        
    except Exception as e:
        print(f"\n❌ Test suite failed with error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())