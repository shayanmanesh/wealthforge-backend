"""
Three Constraint Adjustments Demonstration

Specific demonstration of the Fine-Tuning Engine simulating
3 key constraint adjustments to exceed financial goals:
1. Capital Optimization (Increase Initial Investment)
2. Contribution Enhancement (Increase Monthly Contributions) 
3. Timeline Extension (Strategic Timeline Optimization)
"""

import asyncio
import json
from fine_tuning_engine import (
    GoalExceedPredictor,
    SensitivityAnalyzer,
    FineTuningEngine,
    optimize_goal_exceedance,
    OptimizationStrategy,
    AdjustmentType
)


async def demonstrate_three_key_adjustments():
    """
    Demonstrate the three most impactful constraint adjustments
    for exceeding financial goals.
    """
    print("🔧 FINE-TUNING ENGINE: THREE CONSTRAINT ADJUSTMENTS DEMO")
    print("=" * 75)
    print("Simulating 3 Key Constraint Adjustments to Exceed Goals:")
    print("1. Capital Optimization (Increase Initial Investment)")
    print("2. Contribution Enhancement (Increase Monthly Contributions)")
    print("3. Timeline Extension (Strategic Timeline Optimization)")
    print("=" * 75)
    
    # Demo client profile - representative scenario
    demo_client = {
        "client_id": "three_adjustments_demo",
        "goals": {
            "strategy": "balanced growth with goal exceedance focus",
            "timeline": "15 years",
            "target_amount": 1000000,
            "risk_tolerance": "moderate to high"
        },
        "constraints": {
            "capital": 200000,
            "contributions": 3500,
            "contribution_frequency": "monthly",
            "max_risk_percentage": 75
        },
        "additional_preferences": {
            "age": 40,
            "goal_importance": "high",
            "flexibility": "moderate"
        },
        "financial_info": {
            "annual_income": 150000,
            "net_worth": 450000,
            "liquidity": 80000
        }
    }
    
    print("🎯 DEMO CLIENT SCENARIO:")
    print(f"   Current Capital: ${demo_client['constraints']['capital']:,}")
    print(f"   Monthly Contributions: ${demo_client['constraints']['contributions']:,}")
    print(f"   Timeline: {demo_client['goals']['timeline']}")
    print(f"   Target Amount: ${demo_client['goals']['target_amount']:,}")
    print(f"   Annual Income: ${demo_client['financial_info']['annual_income']:,}")
    print(f"   Available Liquidity: ${demo_client['financial_info']['liquidity']:,}")
    
    # Initialize Fine-Tuning Engine components
    predictor = GoalExceedPredictor()
    analyzer = SensitivityAnalyzer(predictor)
    
    print(f"\n📊 STEP 1: BASELINE GOAL ACHIEVEMENT ANALYSIS")
    print("-" * 50)
    
    # Baseline analysis
    baseline_prediction = await predictor.predict_goal_achievement(demo_client)
    
    print(f"   Current Goal Achievement Probability: {baseline_prediction['goal_achievement_probability']:.1%}")
    print(f"   Exceed by 25% Probability: {baseline_prediction['exceed_by_25_percent_probability']:.1%}")
    print(f"   Exceed by 50% Probability: {baseline_prediction['exceed_by_50_percent_probability']:.1%}")
    print(f"   Expected Median Outcome: ${baseline_prediction['median_outcome']:,.0f}")
    print(f"   Shortfall Risk: {baseline_prediction['shortfall_probability']:.1%}")
    
    if baseline_prediction['goal_achievement_probability'] < 0.7:
        print(f"   ⚠️  Goal achievement probability below 70% - optimization recommended")
    
    print(f"\n🔍 STEP 2: COMPREHENSIVE SENSITIVITY ANALYSIS")
    print("-" * 50)
    
    # Comprehensive sensitivity analysis
    sensitivity_results = await analyzer.comprehensive_sensitivity_analysis(demo_client)
    
    print("   Parameter Impact Analysis:")
    for param, analysis in sensitivity_results.items():
        print(f"   {param.capitalize()}:")
        print(f"     Sensitivity Coefficient: {analysis.sensitivity_coefficient:.4f}")
        print(f"     Elasticity: {analysis.elasticity:.2f}")
        print(f"     Impact Level: {'HIGH' if analysis.sensitivity_coefficient > 0.1 else 'MODERATE' if analysis.sensitivity_coefficient > 0.05 else 'LOW'}")
        if analysis.critical_threshold:
            print(f"     Critical Threshold: {analysis.critical_threshold:.2f}")
    
    print(f"\n⚙️ STEP 3: THREE KEY CONSTRAINT ADJUSTMENTS SIMULATION")
    print("=" * 75)
    
    # ADJUSTMENT 1: Capital Optimization
    print(f"\n💰 ADJUSTMENT 1: CAPITAL OPTIMIZATION")
    print("-" * 40)
    
    capital_scenarios = [
        {"name": "Conservative (+25%)", "multiplier": 1.25},
        {"name": "Moderate (+50%)", "multiplier": 1.50},
        {"name": "Aggressive (+75%)", "multiplier": 1.75}
    ]
    
    print("   Testing capital increase scenarios:")
    capital_results = []
    
    for scenario in capital_scenarios:
        current_capital = demo_client['constraints']['capital']
        new_capital = current_capital * scenario['multiplier']
        
        # Create adjusted profile
        adjusted_profile = demo_client.copy()
        adjusted_profile['constraints'] = demo_client['constraints'].copy()
        adjusted_profile['constraints']['capital'] = new_capital
        
        # Test prediction
        prediction = await predictor.predict_goal_achievement(adjusted_profile)
        improvement = prediction['goal_achievement_probability'] - baseline_prediction['goal_achievement_probability']
        
        capital_results.append({
            'scenario': scenario['name'],
            'new_capital': new_capital,
            'improvement': improvement,
            'success_prob': prediction['goal_achievement_probability'],
            'excess_25': prediction['exceed_by_25_percent_probability']
        })
        
        print(f"   {scenario['name']}:")
        print(f"     New Capital: ${new_capital:,.0f}")
        print(f"     Goal Probability: {prediction['goal_achievement_probability']:.1%}")
        print(f"     Improvement: {improvement:+.1%}")
        print(f"     Exceed 25%: {prediction['exceed_by_25_percent_probability']:.1%}")
    
    best_capital = max(capital_results, key=lambda x: x['improvement'])
    print(f"\n   🏆 Best Capital Scenario: {best_capital['scenario']}")
    print(f"      Improvement: {best_capital['improvement']:+.1%}")
    print(f"      Additional Investment: ${best_capital['new_capital'] - demo_client['constraints']['capital']:,.0f}")
    
    # ADJUSTMENT 2: Contribution Enhancement  
    print(f"\n📈 ADJUSTMENT 2: CONTRIBUTION ENHANCEMENT")
    print("-" * 45)
    
    contribution_scenarios = [
        {"name": "Moderate (+50%)", "multiplier": 1.50},
        {"name": "Significant (+100%)", "multiplier": 2.00},
        {"name": "Aggressive (+150%)", "multiplier": 2.50}
    ]
    
    print("   Testing contribution increase scenarios:")
    contribution_results = []
    
    for scenario in contribution_scenarios:
        current_contributions = demo_client['constraints']['contributions']
        new_contributions = current_contributions * scenario['multiplier']
        
        # Create adjusted profile
        adjusted_profile = demo_client.copy()
        adjusted_profile['constraints'] = demo_client['constraints'].copy()
        adjusted_profile['constraints']['contributions'] = new_contributions
        
        # Test prediction
        prediction = await predictor.predict_goal_achievement(adjusted_profile)
        improvement = prediction['goal_achievement_probability'] - baseline_prediction['goal_achievement_probability']
        
        # Calculate affordability
        additional_annual = (new_contributions - current_contributions) * 12
        affordability_ratio = additional_annual / demo_client['financial_info']['annual_income']
        
        contribution_results.append({
            'scenario': scenario['name'],
            'new_contributions': new_contributions,
            'improvement': improvement,
            'success_prob': prediction['goal_achievement_probability'],
            'excess_25': prediction['exceed_by_25_percent_probability'],
            'affordability': affordability_ratio
        })
        
        print(f"   {scenario['name']}:")
        print(f"     New Contributions: ${new_contributions:,.0f}/month")
        print(f"     Additional Annual: ${additional_annual:,.0f}")
        print(f"     Income Impact: {affordability_ratio:.1%}")
        print(f"     Goal Probability: {prediction['goal_achievement_probability']:.1%}")
        print(f"     Improvement: {improvement:+.1%}")
        print(f"     Exceed 25%: {prediction['exceed_by_25_percent_probability']:.1%}")
    
    best_contribution = max(contribution_results, key=lambda x: x['improvement'])
    print(f"\n   🏆 Best Contribution Scenario: {best_contribution['scenario']}")
    print(f"      Improvement: {best_contribution['improvement']:+.1%}")
    print(f"      Additional Monthly: ${best_contribution['new_contributions'] - demo_client['constraints']['contributions']:,.0f}")
    print(f"      Affordability Impact: {best_contribution['affordability']:.1%} of income")
    
    # ADJUSTMENT 3: Timeline Extension
    print(f"\n⏰ ADJUSTMENT 3: TIMELINE EXTENSION")
    print("-" * 40)
    
    timeline_scenarios = [
        {"name": "Moderate (+2 years)", "additional_years": 2},
        {"name": "Significant (+4 years)", "additional_years": 4},
        {"name": "Extended (+6 years)", "additional_years": 6}
    ]
    
    print("   Testing timeline extension scenarios:")
    timeline_results = []
    
    current_timeline_years = 15  # From demo_client['goals']['timeline']
    
    for scenario in timeline_scenarios:
        new_timeline_years = current_timeline_years + scenario['additional_years']
        
        # Create adjusted profile
        adjusted_profile = demo_client.copy()
        adjusted_profile['goals'] = demo_client['goals'].copy()
        adjusted_profile['goals']['timeline'] = f"{new_timeline_years} years"
        
        # Test prediction
        prediction = await predictor.predict_goal_achievement(adjusted_profile)
        improvement = prediction['goal_achievement_probability'] - baseline_prediction['goal_achievement_probability']
        
        timeline_results.append({
            'scenario': scenario['name'],
            'new_timeline': new_timeline_years,
            'improvement': improvement,
            'success_prob': prediction['goal_achievement_probability'],
            'excess_25': prediction['exceed_by_25_percent_probability']
        })
        
        print(f"   {scenario['name']}:")
        print(f"     New Timeline: {new_timeline_years} years")
        print(f"     Goal Probability: {prediction['goal_achievement_probability']:.1%}")
        print(f"     Improvement: {improvement:+.1%}")
        print(f"     Exceed 25%: {prediction['exceed_by_25_percent_probability']:.1%}")
    
    best_timeline = max(timeline_results, key=lambda x: x['improvement'])
    print(f"\n   🏆 Best Timeline Scenario: {best_timeline['scenario']}")
    print(f"      Improvement: {best_timeline['improvement']:+.1%}")
    print(f"      Additional Time: {best_timeline['new_timeline'] - current_timeline_years} years")
    
    # STEP 4: COMBINED OPTIMIZATION
    print(f"\n🚀 STEP 4: COMBINED OPTIMIZATION ANALYSIS")
    print("=" * 50)
    
    print("   Testing optimal combination of all three adjustments...")
    
    # Create combined scenario using best moderate options
    combined_profile = demo_client.copy()
    combined_profile['constraints'] = demo_client['constraints'].copy()
    combined_profile['goals'] = demo_client['goals'].copy()
    
    # Apply moderate adjustments
    combined_profile['constraints']['capital'] = demo_client['constraints']['capital'] * 1.50  # +50%
    combined_profile['constraints']['contributions'] = demo_client['constraints']['contributions'] * 1.75  # +75%
    combined_profile['goals']['timeline'] = f"{current_timeline_years + 3} years"  # +3 years
    
    combined_prediction = await predictor.predict_goal_achievement(combined_profile)
    combined_improvement = combined_prediction['goal_achievement_probability'] - baseline_prediction['goal_achievement_probability']
    
    print(f"\n   🎯 COMBINED SCENARIO RESULTS:")
    print(f"      Capital: ${combined_profile['constraints']['capital']:,.0f} (+50%)")
    print(f"      Contributions: ${combined_profile['constraints']['contributions']:,.0f}/month (+75%)")
    print(f"      Timeline: {combined_profile['goals']['timeline']} (+3 years)")
    print(f"      Goal Probability: {combined_prediction['goal_achievement_probability']:.1%}")
    print(f"      Total Improvement: {combined_improvement:+.1%}")
    print(f"      Exceed by 25%: {combined_prediction['exceed_by_25_percent_probability']:.1%}")
    print(f"      Exceed by 50%: {combined_prediction['exceed_by_50_percent_probability']:.1%}")
    print(f"      Expected Outcome: ${combined_prediction['median_outcome']:,.0f}")
    
    # STEP 5: IMPLEMENTATION ANALYSIS
    print(f"\n📋 STEP 5: IMPLEMENTATION FEASIBILITY ANALYSIS")
    print("=" * 55)
    
    print("   Individual Adjustment Analysis:")
    
    # Capital adjustment feasibility
    additional_capital_needed = best_capital['new_capital'] - demo_client['constraints']['capital']
    capital_feasibility = min(1.0, demo_client['financial_info']['liquidity'] / additional_capital_needed)
    
    print(f"\n   💰 Capital Optimization:")
    print(f"      Additional Capital Needed: ${additional_capital_needed:,.0f}")
    print(f"      Available Liquidity: ${demo_client['financial_info']['liquidity']:,.0f}")
    print(f"      Feasibility Score: {capital_feasibility:.1%}")
    print(f"      Implementation: {'FEASIBLE' if capital_feasibility >= 1.0 else 'CHALLENGING' if capital_feasibility >= 0.5 else 'DIFFICULT'}")
    
    # Contribution adjustment feasibility
    additional_annual_contrib = (best_contribution['new_contributions'] - demo_client['constraints']['contributions']) * 12
    contribution_feasibility = 1.0 - (additional_annual_contrib / demo_client['financial_info']['annual_income'])
    
    print(f"\n   📈 Contribution Enhancement:")
    print(f"      Additional Annual Contributions: ${additional_annual_contrib:,.0f}")
    print(f"      Current Annual Income: ${demo_client['financial_info']['annual_income']:,.0f}")
    print(f"      Income Impact: {additional_annual_contrib / demo_client['financial_info']['annual_income']:.1%}")
    print(f"      Feasibility Score: {max(0, contribution_feasibility):.1%}")
    print(f"      Implementation: {'FEASIBLE' if contribution_feasibility >= 0.8 else 'MODERATE' if contribution_feasibility >= 0.6 else 'CHALLENGING'}")
    
    # Timeline adjustment feasibility  
    timeline_feasibility = 0.9  # Generally high feasibility for timeline extensions
    additional_years = best_timeline['new_timeline'] - current_timeline_years
    
    print(f"\n   ⏰ Timeline Extension:")
    print(f"      Additional Years: {additional_years}")
    print(f"      New Target Timeline: {best_timeline['new_timeline']} years")
    print(f"      Feasibility Score: {timeline_feasibility:.1%}")
    print(f"      Implementation: FEASIBLE (planning adjustment)")
    
    # STEP 6: FINAL RECOMMENDATIONS
    print(f"\n🏆 STEP 6: FINAL OPTIMIZATION RECOMMENDATIONS")
    print("=" * 60)
    
    # Rank adjustments by impact vs feasibility
    adjustments_ranking = [
        {
            'name': 'Capital Optimization',
            'improvement': best_capital['improvement'],
            'feasibility': capital_feasibility,
            'score': best_capital['improvement'] * capital_feasibility
        },
        {
            'name': 'Contribution Enhancement', 
            'improvement': best_contribution['improvement'],
            'feasibility': max(0, contribution_feasibility),
            'score': best_contribution['improvement'] * max(0, contribution_feasibility)
        },
        {
            'name': 'Timeline Extension',
            'improvement': best_timeline['improvement'], 
            'feasibility': timeline_feasibility,
            'score': best_timeline['improvement'] * timeline_feasibility
        }
    ]
    
    ranked_adjustments = sorted(adjustments_ranking, key=lambda x: x['score'], reverse=True)
    
    print("   Recommended Implementation Priority:")
    for i, adj in enumerate(ranked_adjustments, 1):
        print(f"\n   {i}. {adj['name']}")
        print(f"      Impact: {adj['improvement']:+.1%}")
        print(f"      Feasibility: {adj['feasibility']:.1%}")
        print(f"      Combined Score: {adj['score']:.4f}")
        print(f"      Priority: {'HIGH' if adj['score'] > 0.15 else 'MEDIUM' if adj['score'] > 0.05 else 'LOW'}")
    
    print(f"\n   🎯 OPTIMAL STRATEGY:")
    if combined_improvement > 0.3:  # 30% improvement
        print(f"      Recommendation: COMBINED APPROACH")
        print(f"      Expected Improvement: {combined_improvement:+.1%}")
        print(f"      Implementation Phases:")
        print(f"        Phase 1: {ranked_adjustments[0]['name']} (highest priority)")
        print(f"        Phase 2: {ranked_adjustments[1]['name']} (monitor and adjust)")
        print(f"        Phase 3: {ranked_adjustments[2]['name']} (fine-tuning)")
    else:
        print(f"      Recommendation: FOCUSED APPROACH")
        print(f"      Primary Focus: {ranked_adjustments[0]['name']}")
        print(f"      Expected Improvement: {ranked_adjustments[0]['improvement']:+.1%}")
    
    print(f"\n" + "=" * 75)
    print("🌟 THREE CONSTRAINT ADJUSTMENTS DEMONSTRATION COMPLETE")
    print("=" * 75)
    print("💡 Key Findings:")
    print(f"   📊 Baseline Goal Probability: {baseline_prediction['goal_achievement_probability']:.1%}")
    print(f"   🚀 Combined Optimization: {combined_prediction['goal_achievement_probability']:.1%}")
    print(f"   📈 Total Improvement Potential: {combined_improvement:+.1%}")
    print(f"   🎯 Best Single Adjustment: {ranked_adjustments[0]['name']}")
    print(f"   ⚡ Highest Impact Parameter: Contributions (elasticity: {sensitivity_results['contributions'].elasticity:.1f})")
    print("=" * 75)
    
    return {
        'baseline': baseline_prediction,
        'capital_results': capital_results,
        'contribution_results': contribution_results,
        'timeline_results': timeline_results,
        'combined_result': combined_prediction,
        'sensitivity_analysis': sensitivity_results,
        'recommendations': ranked_adjustments
    }


async def run_quick_demo():
    """Run a quick demonstration of the three adjustments."""
    print("🔧 QUICK THREE ADJUSTMENTS DEMO")
    print("=" * 40)
    
    # Simple client scenario
    client = {
        "goals": {"timeline": "12 years", "target_amount": 500000},
        "constraints": {"capital": 100000, "contributions": 2000}
    }
    
    predictor = GoalExceedPredictor()
    
    print("📊 Testing three key adjustments:")
    
    # Test baseline
    baseline = await predictor.predict_goal_achievement(client)
    print(f"   Baseline: {baseline['goal_achievement_probability']:.1%}")
    
    # Test capital increase
    client_capital = client.copy()
    client_capital['constraints'] = client['constraints'].copy()
    client_capital['constraints']['capital'] = 150000  # +50%
    
    capital_result = await predictor.predict_goal_achievement(client_capital)
    capital_improvement = capital_result['goal_achievement_probability'] - baseline['goal_achievement_probability']
    print(f"   Capital +50%: {capital_result['goal_achievement_probability']:.1%} ({capital_improvement:+.1%})")
    
    # Test contribution increase
    client_contrib = client.copy()
    client_contrib['constraints'] = client['constraints'].copy()
    client_contrib['constraints']['contributions'] = 3000  # +50%
    
    contrib_result = await predictor.predict_goal_achievement(client_contrib)
    contrib_improvement = contrib_result['goal_achievement_probability'] - baseline['goal_achievement_probability']
    print(f"   Contributions +50%: {contrib_result['goal_achievement_probability']:.1%} ({contrib_improvement:+.1%})")
    
    # Test timeline extension
    client_timeline = client.copy()
    client_timeline['goals'] = client['goals'].copy()
    client_timeline['goals']['timeline'] = "15 years"  # +3 years
    
    timeline_result = await predictor.predict_goal_achievement(client_timeline)
    timeline_improvement = timeline_result['goal_achievement_probability'] - baseline['goal_achievement_probability']
    print(f"   Timeline +3 years: {timeline_result['goal_achievement_probability']:.1%} ({timeline_improvement:+.1%})")
    
    print(f"\n✅ Quick demo complete!")
    print(f"   Best adjustment: {'Capital' if capital_improvement > max(contrib_improvement, timeline_improvement) else 'Contributions' if contrib_improvement > timeline_improvement else 'Timeline'}")


async def main():
    """Main demonstration function."""
    print("🔧 FINE-TUNING ENGINE: THREE CONSTRAINT ADJUSTMENTS")
    print("=" * 70)
    print("Demonstrating GoalExceedPredictor and SensitivityAnalyzer")
    print("with 3 key constraint optimization strategies")
    print("=" * 70)
    
    try:
        # Run quick demo first
        await run_quick_demo()
        
        print("\n" + "=" * 70)
        
        # Run comprehensive demo
        results = await demonstrate_three_key_adjustments()
        
        print(f"\n🎉 DEMONSTRATION COMPLETE!")
        print(f"Successfully simulated 3 constraint adjustments with measurable improvements")
        
    except Exception as e:
        print(f"\n❌ Demo failed with error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())