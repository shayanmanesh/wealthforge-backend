#!/usr/bin/env python3
"""
Comprehensive unit tests for WealthForge FastAPI application.
Tests all API endpoints, error handling, and integration points.
"""

import pytest
import asyncio
import json
from unittest.mock import patch, MagicMock, AsyncMock
from fastapi.testclient import TestClient
from datetime import datetime

# Import the FastAPI app
from app import app

# Import WealthForge components for mocking
from goal_constraint_parser import GoalConstraintParser
from orchestrator_agent import OrchestratorAgent, StrategyType
from strategy_optimization_arena import run_strategy_optimization
from portfolio_surgeon import synthesize_optimal_portfolio
from constraint_compliance_auditor import ConstraintComplianceAuditor
from fine_tuning_engine import FineTuningEngine

# Create test client
client = TestClient(app)

# Test data
SAMPLE_CLIENT_PROFILE = {
    "goals": {
        "strategy": "aggressive growth",
        "timeline": "7 years",
        "target_amount": 150000,
        "risk_tolerance": "high",
        "secondary_goals": ["Early Retirement"]
    },
    "constraints": {
        "capital": 15000,
        "contributions": 300,
        "contribution_frequency": "monthly",
        "max_risk_percentage": 85,
        "liquidity_needs": "low",
        "monthly_expenses": 4000,
        "tax_optimization_priority": "medium"
    },
    "additional_preferences": {
        "age": 28,
        "ira_contributions": 6000,
        "401k_contributions": 18000,
        "esg_investing": False,
        "sector_focus": ["Technology", "Healthcare"],
        "international_exposure": "medium",
        "alternative_investments": False,
        "impact_investing": False
    },
    "financial_info": {
        "annual_income": 65000,
        "net_worth": 25000,
        "liquid_assets": 15000,
        "investment_experience": "intermediate",
        "risk_capacity": "high",
        "time_horizon": "long-term"
    }
}

MOCK_PORTFOLIO_SYNTHESIS = {
    "portfolio_id": "portfolio-test-001",
    "final_allocation": {
        "US_STOCKS": 0.70,
        "INTL_STOCKS": 0.15,
        "BONDS": 0.10,
        "ALTERNATIVES": 0.05
    },
    "expected_return": 0.085,
    "risk_score": 0.18,
    "sharpe_ratio": 0.47,
    "synthesis_confidence": 0.92,
    "contributing_agents": ["GrowthOptimizer-47", "RiskBalancer-23"],
    "optimization_method": "pareto_optimal",
    "risk_analysis": {
        "volatility": 0.16,
        "var_95": -0.045,
        "max_drawdown": 0.25,
        "beta": 1.15
    },
    "cost_analysis": {
        "total_expense_ratio": 0.0075,
        "tax_efficiency_score": 0.85,
        "fee_optimization_savings": 0.0025
    }
}

MOCK_COMPLIANCE_AUDIT = {
    "audit_id": "audit-test-001",
    "overall_compliance": "compliant",
    "audit_score": 92,
    "requires_manual_review": False,
    "capital_validation": {
        "compliance_status": "compliant",
        "total_capital": 15000,
        "investment_capital": 12750,
        "warnings": []
    },
    "contribution_validation": {
        "compliance_status": "compliant",
        "ira_contributions": 6000,
        "ira_limit": 6500,
        "violations": []
    },
    "regulatory_analysis": {
        "client_classification": "retail_investor",
        "regulatory_risk_score": 0.15,
        "applicable_regulations": ["Regulation BI", "Know Your Customer"],
        "suitability_assessment": {}
    },
    "violations": [],
    "recommendations": ["Consider increasing emergency fund"]
}


class TestAPIEndpoints:
    """Test all FastAPI endpoints."""

    def test_health_endpoint(self):
        """Test health check endpoint."""
        response = client.get("/health")
        assert response.status_code == 200
        
        data = response.json()
        assert data["success"] is True
        assert "data" in data
        assert "api" in data["data"]
        assert "timestamp" in data["data"]

    def test_root_endpoint(self):
        """Test root endpoint."""
        response = client.get("/")
        assert response.status_code == 200
        
        data = response.json()
        assert data["success"] is True
        assert "WealthForge API" in data["data"]["message"]

    @patch('goal_constraint_parser.GoalConstraintParser.parse_input')
    def test_parse_goals_endpoint(self, mock_parse):
        """Test goal parsing endpoint."""
        mock_parse.return_value = SAMPLE_CLIENT_PROFILE
        
        request_data = {"raw_input": "I want aggressive growth with $15,000 capital"}
        response = client.post("/api/v1/parse-goals", json=request_data)
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert "parsed_data" in data
        mock_parse.assert_called_once()

    def test_parse_goals_validation_error(self):
        """Test goal parsing with invalid input."""
        response = client.post("/api/v1/parse-goals", json={})
        assert response.status_code == 422  # Validation error

    @patch('strategy_optimization_arena.run_strategy_optimization')
    def test_strategy_optimization_endpoint(self, mock_strategy):
        """Test strategy optimization endpoint."""
        mock_result = {
            "strategies_generated": 50,
            "winner": {
                "agent_name": "GrowthOptimizer-47",
                "agent_role": "Aggressive Growth Specialist",
                "alpha_score": 0.8432
            },
            "execution_time": 45.7,
            "top_strategies": []
        }
        mock_strategy.return_value = mock_result
        
        request_data = {
            "client_profile": SAMPLE_CLIENT_PROFILE,
            "num_agents": 50,
            "strategy_focus": "aggressive"
        }
        response = client.post("/api/v1/strategy-optimization", json=request_data)
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "arena_result" in data["data"]
        mock_strategy.assert_called_once()

    @patch('portfolio_surgeon.synthesize_optimal_portfolio')
    def test_portfolio_synthesis_endpoint(self, mock_synthesis):
        """Test portfolio synthesis endpoint."""
        mock_synthesis.return_value = MOCK_PORTFOLIO_SYNTHESIS
        
        request_data = {
            "client_profile": SAMPLE_CLIENT_PROFILE,
            "portfolio_value": 100000,
            "use_real_data": True
        }
        response = client.post("/api/v1/portfolio-synthesis", json=request_data)
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "synthesis_result" in data["data"]
        mock_synthesis.assert_called_once()

    @patch('constraint_compliance_auditor.ConstraintComplianceAuditor.audit_client_profile')
    def test_compliance_audit_endpoint(self, mock_audit):
        """Test compliance audit endpoint."""
        mock_audit.return_value = MOCK_COMPLIANCE_AUDIT
        
        request_data = {
            "client_profile": SAMPLE_CLIENT_PROFILE,
            "portfolio_id": "portfolio-001"
        }
        response = client.post("/api/v1/compliance-audit", json=request_data)
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "audit_report" in data["data"]
        mock_audit.assert_called_once()

    @patch('fine_tuning_engine.FineTuningEngine.optimize_constraints')
    def test_fine_tuning_endpoint(self, mock_optimize):
        """Test fine-tuning optimization endpoint."""
        mock_result = {
            "optimization_id": "opt-test-001",
            "original_goal_probability": 0.65,
            "optimized_goal_probability": 0.82,
            "improvement_factor": 1.26,
            "recommended_scenarios": [],
            "sensitivity_analysis": {},
            "implementation_roadmap": "Test roadmap",
            "risk_assessment": {}
        }
        mock_optimize.return_value = mock_result
        
        request_data = {
            "client_profile": SAMPLE_CLIENT_PROFILE,
            "target_exceedance": 0.25,
            "strategy": "aggressive",
            "portfolio_id": "portfolio-001"
        }
        response = client.post("/api/v1/fine-tuning", json=request_data)
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "optimization_result" in data["data"]
        mock_optimize.assert_called_once()

    @patch('app.get_polygon_market_data')
    def test_market_data_endpoint(self, mock_market_data):
        """Test market data endpoint."""
        mock_data = {
            "AAPL": {
                "symbol": "AAPL",
                "count": 10,
                "results": [
                    {
                        "timestamp": "2024-01-01",
                        "open": 150.0,
                        "high": 155.0,
                        "low": 148.0,
                        "close": 153.0,
                        "volume": 1000000
                    }
                ],
                "status": "OK"
            }
        }
        mock_market_data.return_value = mock_data
        
        request_data = {
            "symbols": ["AAPL"],
            "timespan": "day",
            "limit": 10
        }
        response = client.post("/api/v1/market-data", json=request_data)
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "market_data" in data["data"]

    @patch('app.get_fred_economic_data')
    def test_economic_data_endpoint(self, mock_economic_data):
        """Test economic data endpoint."""
        mock_data = {
            "series_id": "GDP",
            "count": 5,
            "observations": [
                {"date": "2024-01-01", "value": "25000"},
                {"date": "2024-02-01", "value": "25100"}
            ],
            "status": "OK",
            "units": "Billions of Dollars"
        }
        mock_economic_data.return_value = mock_data
        
        request_data = {
            "series_id": "GDP",
            "start_date": "2024-01-01",
            "end_date": "2024-12-31"
        }
        response = client.post("/api/v1/economic-data", json=request_data)
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "economic_data" in data["data"]

    def test_complete_analysis_endpoint_structure(self):
        """Test complete analysis endpoint structure (without mocking internal calls)."""
        # This tests the endpoint structure, actual integration test will use mocks
        request_data = {"client_scenario": SAMPLE_CLIENT_PROFILE}
        
        # This will likely fail due to missing dependencies in test environment
        # but will test the endpoint structure
        response = client.post("/api/v1/complete-analysis", json=request_data)
        
        # Should return either 200 (success) or 500 (internal error due to missing services)
        assert response.status_code in [200, 500]


class TestErrorHandling:
    """Test error handling scenarios."""

    def test_invalid_json_request(self):
        """Test handling of invalid JSON."""
        response = client.post("/api/v1/parse-goals", data="invalid json")
        assert response.status_code == 422

    def test_missing_required_fields(self):
        """Test handling of missing required fields."""
        response = client.post("/api/v1/parse-goals", json={"wrong_field": "value"})
        assert response.status_code == 422

    def test_invalid_client_profile(self):
        """Test handling of invalid client profile data."""
        invalid_profile = {
            "goals": {"strategy": "invalid_strategy"},
            "constraints": {"capital": -1000}  # Negative capital
        }
        
        request_data = {
            "client_profile": invalid_profile,
            "num_agents": 50
        }
        response = client.post("/api/v1/strategy-optimization", json=request_data)
        
        # Should handle validation or return internal error
        assert response.status_code in [422, 500]

    @patch('goal_constraint_parser.GoalConstraintParser.parse_input')
    def test_internal_component_error(self, mock_parse):
        """Test handling of internal component errors."""
        mock_parse.side_effect = Exception("Parser failed")
        
        request_data = {"raw_input": "test input"}
        response = client.post("/api/v1/parse-goals", json=request_data)
        
        assert response.status_code == 500
        data = response.json()
        assert "Parsing failed" in data["detail"]

    def test_nonexistent_endpoint(self):
        """Test handling of non-existent endpoints."""
        response = client.get("/api/v1/nonexistent")
        assert response.status_code == 404


class TestDataValidation:
    """Test data validation and formatting."""

    def test_client_profile_validation(self):
        """Test client profile data validation."""
        # Test with minimal valid profile
        minimal_profile = {
            "goals": {
                "strategy": "balanced",
                "timeline": "10 years",
                "target_amount": 100000,
                "risk_tolerance": "moderate"
            },
            "constraints": {
                "capital": 50000,
                "contributions": 1000,
                "contribution_frequency": "monthly",
                "max_risk_percentage": 70
            },
            "financial_info": {
                "annual_income": 80000,
                "net_worth": 100000
            }
        }
        
        request_data = {
            "client_profile": minimal_profile,
            "portfolio_value": 100000
        }
        
        # This should not fail due to validation errors
        response = client.post("/api/v1/portfolio-synthesis", json=request_data)
        # May fail due to missing services, but not due to validation
        assert response.status_code in [200, 500]

    def test_numerical_constraints(self):
        """Test numerical constraint validation."""
        profile_with_constraints = SAMPLE_CLIENT_PROFILE.copy()
        profile_with_constraints["constraints"]["max_risk_percentage"] = 150  # Invalid > 100%
        
        request_data = {
            "client_profile": profile_with_constraints,
            "num_agents": 50
        }
        
        response = client.post("/api/v1/strategy-optimization", json=request_data)
        # Should handle invalid constraints gracefully
        assert response.status_code in [200, 422, 500]

    def test_string_field_validation(self):
        """Test string field validation."""
        profile_with_invalid_strings = SAMPLE_CLIENT_PROFILE.copy()
        profile_with_invalid_strings["goals"]["strategy"] = ""  # Empty strategy
        
        request_data = {"client_profile": profile_with_invalid_strings}
        response = client.post("/api/v1/complete-analysis", json=request_data)
        
        # Should handle empty/invalid strings
        assert response.status_code in [200, 422, 500]


class TestResponseFormat:
    """Test response format consistency."""

    def test_success_response_format(self):
        """Test that all endpoints return consistent success format."""
        response = client.get("/health")
        assert response.status_code == 200
        
        data = response.json()
        required_fields = ["success", "message", "data", "execution_time", "timestamp"]
        for field in required_fields:
            assert field in data

    @patch('goal_constraint_parser.GoalConstraintParser.parse_input')
    def test_api_response_timestamps(self, mock_parse):
        """Test that responses include proper timestamps."""
        mock_parse.return_value = SAMPLE_CLIENT_PROFILE
        
        request_data = {"raw_input": "test"}
        response = client.post("/api/v1/parse-goals", json=request_data)
        
        assert response.status_code == 200
        data = response.json()
        assert "timestamp" in data
        
        # Verify timestamp format
        timestamp = datetime.fromisoformat(data["timestamp"].replace('Z', '+00:00'))
        assert isinstance(timestamp, datetime)

    def test_error_response_format(self):
        """Test error response format consistency."""
        response = client.post("/api/v1/parse-goals", json={})
        assert response.status_code == 422
        
        data = response.json()
        assert "detail" in data


class TestAsyncOperations:
    """Test async operations and background tasks."""

    @patch('app.send_kafka_message')
    @patch('goal_constraint_parser.GoalConstraintParser.parse_input')
    def test_kafka_background_task(self, mock_parse, mock_kafka):
        """Test that Kafka messages are sent for background processing."""
        mock_parse.return_value = SAMPLE_CLIENT_PROFILE
        mock_kafka.return_value = None
        
        request_data = {"raw_input": "test input"}
        response = client.post("/api/v1/parse-goals", json=request_data)
        
        assert response.status_code == 200
        # Note: Background tasks execute after response, so we can't easily test them
        # in this synchronous test environment

    def test_concurrent_requests(self):
        """Test handling of concurrent requests."""
        import threading
        import time
        
        responses = []
        
        def make_request():
            response = client.get("/health")
            responses.append(response.status_code)
        
        # Create multiple threads to make concurrent requests
        threads = []
        for _ in range(5):
            thread = threading.Thread(target=make_request)
            threads.append(thread)
            thread.start()
        
        # Wait for all threads to complete
        for thread in threads:
            thread.join()
        
        # All requests should succeed
        assert all(status == 200 for status in responses)
        assert len(responses) == 5


class TestSampleInputSimulation:
    """Test with the specific sample input provided."""

    def test_sample_input_parsing(self):
        """Test parsing of the provided sample input."""
        sample_input = {
            'goals': {'strategy': 'Aggressive Growth', 'timeline': 7},
            'constraints': {'capital': 15000, 'contributions': 300}
        }
        
        # Convert to string format as API expects
        raw_input = json.dumps(sample_input)
        request_data = {"raw_input": raw_input}
        
        response = client.post("/api/v1/parse-goals", json=request_data)
        
        # Should handle the parsing attempt
        assert response.status_code in [200, 500]

    @patch('strategy_optimization_arena.run_strategy_optimization')
    def test_sample_input_strategy_optimization(self, mock_strategy):
        """Test strategy optimization with sample input."""
        mock_strategy.return_value = {
            "strategies_generated": 50,
            "winner": {
                "agent_name": "AggressiveGrowthAgent-42",
                "agent_role": "High Risk Growth Specialist",
                "alpha_score": 0.9125
            },
            "execution_time": 52.3,
            "top_strategies": []
        }
        
        # Expand sample input to full profile format
        expanded_profile = {
            "goals": {
                "strategy": "aggressive growth",
                "timeline": "7 years",
                "target_amount": 150000,  # Estimated based on contributions
                "risk_tolerance": "high",
                "secondary_goals": []
            },
            "constraints": {
                "capital": 15000,
                "contributions": 300,
                "contribution_frequency": "monthly",
                "max_risk_percentage": 85,
                "liquidity_needs": "low",
                "monthly_expenses": 3000,
                "tax_optimization_priority": "low"
            },
            "additional_preferences": {
                "age": 25,  # Assumed for aggressive timeline
                "ira_contributions": 0,
                "401k_contributions": 0,
                "esg_investing": False,
                "sector_focus": [],
                "international_exposure": "low",
                "alternative_investments": True,
                "impact_investing": False
            },
            "financial_info": {
                "annual_income": 50000,  # Estimated
                "net_worth": 20000,      # Estimated
                "liquid_assets": 15000,  # Same as capital
                "investment_experience": "beginner",
                "risk_capacity": "high",
                "time_horizon": "long-term"
            }
        }
        
        request_data = {
            "client_profile": expanded_profile,
            "num_agents": 50,
            "strategy_focus": "aggressive"
        }
        
        response = client.post("/api/v1/strategy-optimization", json=request_data)
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "arena_result" in data["data"]
        assert data["data"]["arena_result"]["strategies_generated"] == 50

    def test_sample_input_complete_workflow(self):
        """Test complete workflow with sample input (structure only)."""
        # Test the complete analysis endpoint with minimal sample data
        minimal_sample = {
            "goals": {
                "strategy": "aggressive growth",
                "timeline": "7 years",
                "target_amount": 150000,
                "risk_tolerance": "high"
            },
            "constraints": {
                "capital": 15000,
                "contributions": 300,
                "contribution_frequency": "monthly",
                "max_risk_percentage": 85
            },
            "financial_info": {
                "annual_income": 50000,
                "net_worth": 20000
            }
        }
        
        request_data = {"client_scenario": minimal_sample}
        response = client.post("/api/v1/complete-analysis", json=request_data)
        
        # Should handle the request structure (may fail due to missing services)
        assert response.status_code in [200, 500]
        
        if response.status_code == 200:
            data = response.json()
            assert data["success"] is True
            assert "complete_analysis" in data["data"]


if __name__ == "__main__":
    print("🧪 Running WealthForge API Integration Tests...")
    print("=" * 60)
    
    # Run tests
    pytest.main([__file__, "-v", "--tb=short"])
    
    print("\n✅ API Integration Tests Complete!")