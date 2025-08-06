"""
WealthForge FastAPI Integration Test

Test script to demonstrate all API endpoints and async functionality.
"""

import asyncio
import json
import httpx
import time
from datetime import datetime

# API Configuration
API_BASE_URL = "http://localhost:8000"
API_TOKEN = "demo-api-token"  # For development/demo

class WealthForgeAPITester:
    """Test client for WealthForge FastAPI endpoints."""
    
    def __init__(self, base_url: str = API_BASE_URL, token: str = API_TOKEN):
        self.base_url = base_url
        self.headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
    
    async def test_health(self):
        """Test health endpoint."""
        print("🔍 Testing API Health...")
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.base_url}/health")
            print(f"   Status: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                print(f"   API: {data['data']['api']}")
                print(f"   Redis: {data['data']['redis']}")
                print(f"   Kafka: {data['data']['kafka']}")
            return response.status_code == 200
    
    async def test_root(self):
        """Test root endpoint."""
        print("🌟 Testing Root Endpoint...")
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.base_url}/")
            print(f"   Status: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                print(f"   Title: {data['data']['version']}")
                print(f"   Components: {len(data['data']['components'])}")
            return response.status_code == 200
    
    async def test_goal_parsing(self):
        """Test goal parsing endpoint."""
        print("📋 Testing Goal Parsing...")
        
        client_profile = {
            "goals": {
                "strategy": "aggressive growth with ESG focus",
                "timeline": "12 years",
                "target_amount": 800000,
                "risk_tolerance": "high"
            },
            "constraints": {
                "capital": 150000,
                "contributions": 2500,
                "contribution_frequency": "monthly",
                "max_risk_percentage": 85
            },
            "additional_preferences": {
                "age": 32,
                "esg_investing": True
            },
            "financial_info": {
                "annual_income": 95000,
                "net_worth": 275000
            }
        }
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                f"{self.base_url}/api/v1/parse-goals",
                headers=self.headers,
                json=client_profile
            )
            print(f"   Status: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                print(f"   Execution Time: {data['execution_time']:.3f}s")
                print(f"   Success: {data['success']}")
                return data
            else:
                print(f"   Error: {response.text}")
                return None
    
    async def test_strategy_optimization(self, client_profile):
        """Test strategy optimization endpoint."""
        print("🏁 Testing Strategy Optimization...")
        
        request_data = {
            "client_profile": client_profile,
            "num_agents": 25,  # Reduced for faster testing
            "strategy_focus": "aggressive_growth"
        }
        
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                f"{self.base_url}/api/v1/strategy-optimization",
                headers=self.headers,
                json=request_data
            )
            print(f"   Status: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                print(f"   Execution Time: {data['execution_time']:.3f}s")
                arena_result = data['data']['arena_result']
                print(f"   Strategies Generated: {arena_result['strategies_generated']}")
                print(f"   Winner: {arena_result['winner']['agent_name']}")
                print(f"   Alpha Score: {arena_result['winner']['alpha_score']:.4f}")
                return data
            else:
                print(f"   Error: {response.text}")
                return None
    
    async def test_portfolio_synthesis(self, client_profile):
        """Test portfolio synthesis endpoint."""
        print("🔬 Testing Portfolio Synthesis...")
        
        request_data = {
            "client_profile": client_profile,
            "portfolio_value": 150000,
            "use_real_data": False  # Use dummy data for testing
        }
        
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                f"{self.base_url}/api/v1/portfolio-synthesis",
                headers=self.headers,
                json=request_data
            )
            print(f"   Status: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                print(f"   Execution Time: {data['execution_time']:.3f}s")
                synthesis = data['data']['synthesis_result']
                print(f"   Portfolio ID: {synthesis['portfolio_id']}")
                print(f"   Expected Return: {synthesis['expected_return']:.2%}")
                print(f"   Risk Score: {synthesis['risk_score']:.3f}")
                print(f"   Sharpe Ratio: {synthesis['sharpe_ratio']:.3f}")
                return data
            else:
                print(f"   Error: {response.text}")
                return None
    
    async def test_compliance_audit(self, client_profile):
        """Test compliance audit endpoint."""
        print("⚖️ Testing Compliance Audit...")
        
        request_data = {
            "client_profile": client_profile
        }
        
        async with httpx.AsyncClient(timeout=45.0) as client:
            response = await client.post(
                f"{self.base_url}/api/v1/compliance-audit",
                headers=self.headers,
                json=request_data
            )
            print(f"   Status: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                print(f"   Execution Time: {data['execution_time']:.3f}s")
                audit = data['data']['audit_report']
                print(f"   Audit ID: {audit['audit_id']}")
                print(f"   Overall Compliance: {audit['overall_compliance']}")
                print(f"   Audit Score: {audit['audit_score']:.1f}/100")
                print(f"   Violations: {len(audit['violations'])}")
                return data
            else:
                print(f"   Error: {response.text}")
                return None
    
    async def test_fine_tuning(self, client_profile):
        """Test fine-tuning optimization endpoint."""
        print("🔧 Testing Fine-Tuning Optimization...")
        
        request_data = {
            "client_profile": client_profile,
            "target_exceedance": 0.30,
            "strategy": "balanced"
        }
        
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                f"{self.base_url}/api/v1/fine-tuning",
                headers=self.headers,
                json=request_data
            )
            print(f"   Status: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                print(f"   Execution Time: {data['execution_time']:.3f}s")
                optimization = data['data']['optimization_result']
                print(f"   Optimization ID: {optimization['optimization_id']}")
                print(f"   Original Probability: {optimization['original_goal_probability']:.1%}")
                print(f"   Optimized Probability: {optimization['optimized_goal_probability']:.1%}")
                print(f"   Improvement Factor: {optimization['improvement_factor']:.2f}x")
                if optimization['recommended_scenarios']:
                    best_scenario = optimization['recommended_scenarios'][0]
                    print(f"   Best Scenario: {best_scenario['scenario_name']}")
                return data
            else:
                print(f"   Error: {response.text}")
                return None
    
    async def test_market_data(self):
        """Test market data endpoint."""
        print("📊 Testing Market Data...")
        
        request_data = {
            "symbols": ["AAPL", "SPY", "QQQ"],
            "timespan": "day",
            "limit": 10
        }
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                f"{self.base_url}/api/v1/market-data",
                headers=self.headers,
                json=request_data
            )
            print(f"   Status: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                print(f"   Execution Time: {data['execution_time']:.3f}s")
                market_data = data['data']['market_data']
                print(f"   Symbols Fetched: {len(market_data)}")
                for symbol, symbol_data in market_data.items():
                    print(f"   {symbol}: {symbol_data['count']} data points")
                return data
            else:
                print(f"   Error: {response.text}")
                return None
    
    async def test_economic_data(self):
        """Test economic data endpoint."""
        print("📈 Testing Economic Data...")
        
        request_data = {
            "series_id": "GDP",
            "start_date": "2023-01-01",
            "end_date": "2024-01-01"
        }
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                f"{self.base_url}/api/v1/economic-data",
                headers=self.headers,
                json=request_data
            )
            print(f"   Status: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                print(f"   Execution Time: {data['execution_time']:.3f}s")
                economic_data = data['data']['economic_data']
                print(f"   Series ID: {economic_data['series_id']}")
                print(f"   Data Points: {economic_data['count']}")
                return data
            else:
                print(f"   Error: {response.text}")
                return None
    
    async def test_complete_analysis(self, client_profile):
        """Test complete analysis endpoint."""
        print("🌟 Testing Complete Analysis...")
        
        async with httpx.AsyncClient(timeout=120.0) as client:
            response = await client.post(
                f"{self.base_url}/api/v1/complete-analysis",
                headers=self.headers,
                json=client_profile
            )
            print(f"   Status: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                print(f"   Execution Time: {data['execution_time']:.3f}s")
                analysis = data['data']['complete_analysis']
                print(f"   Components Executed: {data['data']['components_executed']}")
                
                # Print summary of each component
                if 'arena_result' in analysis:
                    print(f"   Arena Winner: {analysis['arena_result']['winner']['agent_name']}")
                if 'portfolio_synthesis' in analysis:
                    print(f"   Portfolio Return: {analysis['portfolio_synthesis']['expected_return']:.2%}")
                if 'compliance_audit' in analysis:
                    print(f"   Compliance Score: {analysis['compliance_audit']['audit_score']:.1f}")
                if 'optimization' in analysis:
                    print(f"   Optimization Factor: {analysis['optimization']['improvement_factor']:.2f}x")
                
                return data
            else:
                print(f"   Error: {response.text}")
                return None

async def run_comprehensive_api_test():
    """Run comprehensive API integration test."""
    print("🚀 WEALTHFORGE FASTAPI INTEGRATION TEST")
    print("=" * 70)
    print("Testing all API endpoints and async functionality")
    print("=" * 70)
    
    tester = WealthForgeAPITester()
    start_time = time.time()
    
    # Test basic endpoints
    print("\n🔍 BASIC ENDPOINT TESTS")
    print("-" * 40)
    
    health_ok = await tester.test_health()
    root_ok = await tester.test_root()
    
    if not (health_ok and root_ok):
        print("❌ Basic endpoint tests failed. Check if API is running.")
        return
    
    # Test core WealthForge components
    print("\n🏗️ WEALTHFORGE COMPONENT TESTS")
    print("-" * 45)
    
    # 1. Goal parsing
    goal_result = await tester.test_goal_parsing()
    if not goal_result:
        print("❌ Goal parsing failed")
        return
    
    client_profile = goal_result['data']['parsed_profile']
    
    # 2. Strategy optimization
    strategy_result = await tester.test_strategy_optimization(client_profile)
    if not strategy_result:
        print("❌ Strategy optimization failed")
        return
    
    # 3. Portfolio synthesis
    portfolio_result = await tester.test_portfolio_synthesis(client_profile)
    if not portfolio_result:
        print("❌ Portfolio synthesis failed")
        return
    
    # 4. Compliance audit
    audit_result = await tester.test_compliance_audit(client_profile)
    if not audit_result:
        print("❌ Compliance audit failed")
        return
    
    # 5. Fine-tuning optimization
    tuning_result = await tester.test_fine_tuning(client_profile)
    if not tuning_result:
        print("❌ Fine-tuning optimization failed")
        return
    
    # Test external data endpoints
    print("\n📊 EXTERNAL DATA TESTS")
    print("-" * 30)
    
    market_result = await tester.test_market_data()
    economic_result = await tester.test_economic_data()
    
    # Test complete analysis
    print("\n🌟 COMPLETE ANALYSIS TEST")
    print("-" * 35)
    
    complete_result = await tester.test_complete_analysis(client_profile)
    
    # Test summary
    total_time = time.time() - start_time
    print("\n" + "=" * 70)
    print("🎉 WEALTHFORGE FASTAPI INTEGRATION TEST COMPLETE")
    print("=" * 70)
    
    test_results = {
        "Health Check": health_ok,
        "Root Endpoint": root_ok,
        "Goal Parsing": bool(goal_result),
        "Strategy Optimization": bool(strategy_result),
        "Portfolio Synthesis": bool(portfolio_result),
        "Compliance Audit": bool(audit_result),
        "Fine-Tuning": bool(tuning_result),
        "Market Data": bool(market_result),
        "Economic Data": bool(economic_result),
        "Complete Analysis": bool(complete_result)
    }
    
    print("📊 TEST RESULTS:")
    passed = 0
    for test_name, result in test_results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"   {test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\n📈 SUMMARY:")
    print(f"   Tests Passed: {passed}/{len(test_results)}")
    print(f"   Success Rate: {passed/len(test_results):.1%}")
    print(f"   Total Execution Time: {total_time:.1f}s")
    
    if passed == len(test_results):
        print("🌟 All tests passed! WealthForge FastAPI is fully operational.")
    else:
        print("⚠️ Some tests failed. Check API logs for details.")
    
    return test_results

async def main():
    """Main test function."""
    try:
        results = await run_comprehensive_api_test()
        return results
    except Exception as e:
        print(f"❌ Test execution failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("🔧 WealthForge FastAPI Integration Tester")
    print("Make sure the API is running at http://localhost:8000")
    print("Start with: uvicorn app:app --host 0.0.0.0 --port 8000")
    print()
    
    asyncio.run(main())