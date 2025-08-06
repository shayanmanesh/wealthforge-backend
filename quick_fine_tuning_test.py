"""
Quick Fine-Tuning Engine Test

Simple test to verify the Fine-Tuning Engine functionality.
"""

import asyncio
from fine_tuning_engine import (
    GoalExceedPredictor,
    SensitivityAnalyzer,
    optimize_goal_exceedance,
    OptimizationStrategy
)


async def test_goal_predictor():
    print('🎯 Testing GoalExceedPredictor')
    print('='*40)
    
    predictor = GoalExceedPredictor()
    
    # Simple test scenario
    client_profile = {
        'goals': {
            'strategy': 'balanced growth',
            'timeline': '15 years',
            'target_amount': 800000,
            'risk_tolerance': 'moderate'
        },
        'constraints': {
            'capital': 150000,
            'contributions': 2500
        }
    }
    
    print('Client: $150,000 capital')
    print('Target: $800,000 in 15 years')
    print('Contributions: $2,500/month')
    
    print('\n🚀 Running prediction...')
    
    # Run prediction
    prediction = await predictor.predict_goal_achievement(client_profile)
    
    print(f'\n📊 Results:')
    print(f'   Goal Achievement: {prediction["goal_achievement_probability"]:.1%}')
    print(f'   Exceed by 25%: {prediction["exceed_by_25_percent_probability"]:.1%}')
    print(f'   Expected Excess: {prediction["expected_excess_percentage"]:.1%}')
    print(f'   Median Outcome: ${prediction["median_outcome"]:,.0f}')
    
    print('\n✅ GoalExceedPredictor test successful!')


async def test_sensitivity_analyzer():
    print('\n📊 Testing SensitivityAnalyzer')
    print('='*40)
    
    predictor = GoalExceedPredictor()
    analyzer = SensitivityAnalyzer(predictor)
    
    # Test profile
    test_profile = {
        'goals': {
            'timeline': '12 years',
            'target_amount': 600000,
            'risk_tolerance': 'moderate'
        },
        'constraints': {
            'capital': 100000,
            'contributions': 2000
        }
    }
    
    print('Testing sensitivity to capital changes...')
    
    try:
        sensitivity = await analyzer.analyze_parameter_sensitivity(test_profile, 'capital')
        
        print(f'   Sensitivity Coefficient: {sensitivity.sensitivity_coefficient:.4f}')
        print(f'   Elasticity: {sensitivity.elasticity:.4f}')
        print(f'   Risk Factors: {len(sensitivity.risk_factors)}')
        
        print('\n✅ SensitivityAnalyzer test successful!')
        
    except Exception as e:
        print(f'   Error: {e}')


async def test_optimization():
    print('\n🔧 Testing Fine-Tuning Optimization')
    print('='*45)
    
    # Client profile for optimization
    client_profile = {
        'goals': {
            'strategy': 'aggressive growth',
            'timeline': '18 years',
            'target_amount': 1200000,
            'risk_tolerance': 'high'
        },
        'constraints': {
            'capital': 180000,
            'contributions': 3000,
            'max_risk_percentage': 80
        },
        'additional_preferences': {
            'age': 35
        }
    }
    
    print('Client Profile:')
    print('   Capital: $180,000')
    print('   Target: $1,200,000')
    print('   Timeline: 18 years')
    print('   Contributions: $3,000/month')
    
    print('\n🚀 Running optimization...')
    
    try:
        result = await optimize_goal_exceedance(
            client_profile,
            target_exceedance=0.25,
            strategy=OptimizationStrategy.BALANCED
        )
        
        print(f'\n📊 Optimization Results:')
        print(f'   Original Probability: {result.original_goal_probability:.1%}')
        print(f'   Optimized Probability: {result.optimized_goal_probability:.1%}')
        print(f'   Improvement Factor: {result.improvement_factor:.2f}x')
        print(f'   Scenarios Generated: {len(result.recommended_scenarios)}')
        
        if result.recommended_scenarios:
            best = result.recommended_scenarios[0]
            print(f'\n🏆 Best Scenario: {best.scenario_name}')
            print(f'   Success Probability: {best.probability_of_success:.1%}')
            print(f'   Implementation Score: {best.implementation_score:.1%}')
            print(f'   Excess Achievement: {best.excess_achievement:.1%}')
        
        print('\n✅ Optimization test successful!')
        
    except Exception as e:
        print(f'   Error: {e}')
        import traceback
        traceback.print_exc()


async def main():
    print('🔧 FINE-TUNING ENGINE QUICK TEST')
    print('='*50)
    
    await test_goal_predictor()
    await test_sensitivity_analyzer()
    await test_optimization()
    
    print('\n' + '='*50)
    print('🎉 Fine-Tuning Engine tests completed!')
    print('='*50)


if __name__ == "__main__":
    asyncio.run(main())