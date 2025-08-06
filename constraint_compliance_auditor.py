"""
Constraint Compliance Auditor with RegulatoryTuring Agent

This module implements comprehensive compliance checking for investment strategies,
including SEC regulations, capital requirements, and contribution validations.
The RegulatoryTuring agent provides intelligent regulatory analysis and compliance oversight.
"""

import asyncio
import json
import re
from typing import Dict, List, Any, Optional, Tuple, Set, Union
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
import numpy as np
import warnings
warnings.filterwarnings('ignore')

# Import existing components
from goal_constraint_parser import parse_goal_constraints
from portfolio_surgeon import PortfolioSynthesis
from strategy_optimization_arena import AgentStrategy, MarketData


class ComplianceLevel(Enum):
    """Compliance severity levels."""
    COMPLIANT = "compliant"
    WARNING = "warning"
    VIOLATION = "violation"
    CRITICAL = "critical"


class RegulationType(Enum):
    """Types of regulatory requirements."""
    SEC_INVESTMENT_ADVISOR = "sec_investment_advisor"
    SEC_BROKER_DEALER = "sec_broker_dealer"
    FINRA_SUITABILITY = "finra_suitability"
    ERISA_FIDUCIARY = "erisa_fiduciary"
    STATE_REGISTRATION = "state_registration"
    ANTI_MONEY_LAUNDERING = "anti_money_laundering"
    KNOW_YOUR_CUSTOMER = "know_your_customer"
    ACCREDITED_INVESTOR = "accredited_investor"
    LIQUIDITY_REQUIREMENTS = "liquidity_requirements"
    CONCENTRATION_LIMITS = "concentration_limits"


class ValidationCategory(Enum):
    """Categories of validation checks."""
    CAPITAL_ADEQUACY = "capital_adequacy"
    CONTRIBUTION_LIMITS = "contribution_limits"
    RISK_TOLERANCE = "risk_tolerance"
    SUITABILITY = "suitability"
    DIVERSIFICATION = "diversification"
    LIQUIDITY = "liquidity"
    TAX_COMPLIANCE = "tax_compliance"
    REGULATORY = "regulatory"


@dataclass
class ComplianceRule:
    """Represents a compliance rule or regulation."""
    rule_id: str
    regulation_type: RegulationType
    validation_category: ValidationCategory
    description: str
    severity: ComplianceLevel
    rule_logic: str
    threshold_values: Dict[str, Any] = field(default_factory=dict)
    exemptions: List[str] = field(default_factory=list)
    citations: List[str] = field(default_factory=list)
    last_updated: datetime = field(default_factory=datetime.now)


@dataclass
class ComplianceViolation:
    """Represents a compliance violation or warning."""
    violation_id: str
    rule_id: str
    severity: ComplianceLevel
    description: str
    affected_component: str
    current_value: Any
    required_value: Any
    recommendation: str
    timestamp: datetime = field(default_factory=datetime.now)
    auto_fixable: bool = False
    fix_action: Optional[str] = None


@dataclass
class CapitalValidation:
    """Capital adequacy validation results."""
    total_capital: float
    minimum_required: float
    available_liquidity: float
    emergency_fund: float
    investment_capital: float
    compliance_status: ComplianceLevel
    warnings: List[str] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)


@dataclass
class ContributionValidation:
    """Contribution limits validation results."""
    annual_contributions: float
    contribution_frequency: str
    contribution_limits: Dict[str, float]
    ira_contributions: float
    ira_limit: float
    k401_contributions: float
    k401_limit: float
    excess_contributions: float
    compliance_status: ComplianceLevel
    violations: List[str] = field(default_factory=list)


@dataclass
class RegulatoryAnalysis:
    """Comprehensive regulatory analysis results."""
    client_classification: str
    applicable_regulations: List[RegulationType]
    suitability_assessment: Dict[str, Any]
    fiduciary_obligations: List[str]
    disclosure_requirements: List[str]
    compliance_gaps: List[str]
    regulatory_risk_score: float
    recommended_actions: List[str]


@dataclass
class ComplianceAuditReport:
    """Complete compliance audit report."""
    audit_id: str
    timestamp: datetime
    client_id: str
    portfolio_id: str
    overall_compliance: ComplianceLevel
    capital_validation: CapitalValidation
    contribution_validation: ContributionValidation
    regulatory_analysis: RegulatoryAnalysis
    violations: List[ComplianceViolation]
    recommendations: List[str]
    requires_manual_review: bool
    audit_score: float
    next_review_date: datetime


class RegulatoryTuring:
    """
    Advanced regulatory AI agent for intelligent compliance analysis.
    Simulates sophisticated regulatory knowledge and reasoning capabilities.
    """
    
    def __init__(self):
        """Initialize RegulatoryTuring agent."""
        self.regulatory_knowledge = self._initialize_regulatory_knowledge()
        self.compliance_rules = self._load_compliance_rules()
        self.precedent_database = self._initialize_precedent_database()
        self.ai_reasoning_engine = self._initialize_ai_reasoning()
        
    def _initialize_regulatory_knowledge(self) -> Dict[str, Any]:
        """Initialize comprehensive regulatory knowledge base."""
        return {
            'sec_regulations': {
                'investment_advisor_act_1940': {
                    'fiduciary_duty': 'Must act in client best interest',
                    'disclosure_requirements': ['Form ADV', 'conflicts of interest'],
                    'custody_rules': 'Client asset protection requirements',
                    'advertising_rules': 'Testimonial and performance advertising'
                },
                'securities_act_1933': {
                    'registration_requirements': 'Security offering registrations',
                    'exemptions': ['Rule 506', 'Regulation D'],
                    'anti_fraud': 'Material misstatement prohibitions'
                },
                'securities_exchange_act_1934': {
                    'broker_dealer_regulations': 'Trading and execution rules',
                    'market_manipulation': 'Anti-manipulation provisions',
                    'reporting_requirements': 'Periodic disclosure mandates'
                }
            },
            'finra_rules': {
                'suitability_rule_2111': {
                    'reasonable_basis': 'Investment strategy appropriateness',
                    'customer_specific': 'Individual suitability analysis',
                    'quantitative': 'Excessive trading controls'
                },
                'know_your_customer_rule_2090': {
                    'customer_identification': 'Identity verification requirements',
                    'risk_profile': 'Investment profile establishment',
                    'ongoing_monitoring': 'Account supervision duties'
                }
            },
            'erisa_requirements': {
                'fiduciary_standards': {
                    'prudent_expert': 'Professional investment management',
                    'diversification': 'Risk spreading requirements',
                    'plan_documents': 'Adherence to plan provisions'
                }
            },
            'tax_regulations': {
                'ira_contribution_limits': {
                    '2024_traditional': 7000,
                    '2024_roth': 7000,
                    '2024_catchup': 1000,
                    'income_limits': {'single': 153000, 'married': 228000}
                },
                '401k_contribution_limits': {
                    '2024_employee': 23000,
                    '2024_catchup': 7500,
                    '2024_total': 69000
                }
            }
        }
    
    def _load_compliance_rules(self) -> List[ComplianceRule]:
        """Load comprehensive compliance rules database."""
        rules = [
            # SEC Investment Advisor Rules
            ComplianceRule(
                rule_id="SEC_IA_001",
                regulation_type=RegulationType.SEC_INVESTMENT_ADVISOR,
                validation_category=ValidationCategory.REGULATORY,
                description="Fiduciary duty to act in client's best interest",
                severity=ComplianceLevel.CRITICAL,
                rule_logic="portfolio_recommendations_align_with_client_goals",
                citations=["Investment Advisers Act of 1940, Section 206"]
            ),
            ComplianceRule(
                rule_id="SEC_IA_002",
                regulation_type=RegulationType.SEC_INVESTMENT_ADVISOR,
                validation_category=ValidationCategory.REGULATORY,
                description="Disclosure of material conflicts of interest",
                severity=ComplianceLevel.VIOLATION,
                rule_logic="conflicts_disclosed_in_form_adv",
                citations=["Investment Advisers Act of 1940, Section 207"]
            ),
            
            # FINRA Suitability Rules
            ComplianceRule(
                rule_id="FINRA_2111_001",
                regulation_type=RegulationType.FINRA_SUITABILITY,
                validation_category=ValidationCategory.SUITABILITY,
                description="Reasonable basis suitability - investment strategy appropriateness",
                severity=ComplianceLevel.VIOLATION,
                rule_logic="strategy_has_reasonable_basis",
                citations=["FINRA Rule 2111"]
            ),
            ComplianceRule(
                rule_id="FINRA_2111_002",
                regulation_type=RegulationType.FINRA_SUITABILITY,
                validation_category=ValidationCategory.SUITABILITY,
                description="Customer-specific suitability based on investment profile",
                severity=ComplianceLevel.VIOLATION,
                rule_logic="recommendations_suitable_for_customer",
                citations=["FINRA Rule 2111"]
            ),
            
            # Capital Adequacy Rules
            ComplianceRule(
                rule_id="CAP_001",
                regulation_type=RegulationType.LIQUIDITY_REQUIREMENTS,
                validation_category=ValidationCategory.CAPITAL_ADEQUACY,
                description="Minimum emergency fund requirement",
                severity=ComplianceLevel.WARNING,
                rule_logic="emergency_fund >= monthly_expenses * 3",
                threshold_values={"min_months": 3, "recommended_months": 6}
            ),
            ComplianceRule(
                rule_id="CAP_002",
                regulation_type=RegulationType.LIQUIDITY_REQUIREMENTS,
                validation_category=ValidationCategory.CAPITAL_ADEQUACY,
                description="Investment capital adequacy for strategy",
                severity=ComplianceLevel.WARNING,
                rule_logic="investment_capital >= minimum_for_diversification",
                threshold_values={"min_investment": 10000, "min_diversified": 50000}
            ),
            
            # Contribution Limit Rules
            ComplianceRule(
                rule_id="TAX_IRA_001",
                regulation_type=RegulationType.SEC_INVESTMENT_ADVISOR,
                validation_category=ValidationCategory.CONTRIBUTION_LIMITS,
                description="IRA annual contribution limits",
                severity=ComplianceLevel.VIOLATION,
                rule_logic="ira_contributions <= annual_limit",
                threshold_values={"2024_limit": 7000, "2024_catchup": 1000}
            ),
            ComplianceRule(
                rule_id="TAX_401K_001",
                regulation_type=RegulationType.SEC_INVESTMENT_ADVISOR,
                validation_category=ValidationCategory.CONTRIBUTION_LIMITS,
                description="401(k) annual contribution limits",
                severity=ComplianceLevel.VIOLATION,
                rule_logic="401k_contributions <= annual_limit",
                threshold_values={"2024_employee": 23000, "2024_catchup": 7500}
            ),
            
            # Risk and Diversification Rules
            ComplianceRule(
                rule_id="RISK_001",
                regulation_type=RegulationType.FINRA_SUITABILITY,
                validation_category=ValidationCategory.RISK_TOLERANCE,
                description="Portfolio risk alignment with client risk tolerance",
                severity=ComplianceLevel.WARNING,
                rule_logic="portfolio_risk <= client_risk_tolerance",
                threshold_values={"conservative": 0.08, "moderate": 0.15, "aggressive": 0.25}
            ),
            ComplianceRule(
                rule_id="DIV_001",
                regulation_type=RegulationType.CONCENTRATION_LIMITS,
                validation_category=ValidationCategory.DIVERSIFICATION,
                description="Single asset concentration limits",
                severity=ComplianceLevel.WARNING,
                rule_logic="max_single_asset_weight <= concentration_limit",
                threshold_values={"max_single_asset": 0.4, "max_sector": 0.6}
            ),
            
            # Accredited Investor Rules
            ComplianceRule(
                rule_id="ACC_001",
                regulation_type=RegulationType.ACCREDITED_INVESTOR,
                validation_category=ValidationCategory.REGULATORY,
                description="Accredited investor verification for alternative investments",
                severity=ComplianceLevel.CRITICAL,
                rule_logic="alternative_investments_require_accredited_status",
                threshold_values={"min_income": 200000, "min_net_worth": 1000000}
            )
        ]
        
        return rules
    
    def _initialize_precedent_database(self) -> Dict[str, Any]:
        """Initialize regulatory precedent and case law database."""
        return {
            'sec_enforcement_actions': {
                'fiduciary_violations': [
                    'Failure to disclose conflicts - $2.5M penalty',
                    'Unsuitable investment recommendations - $1.8M penalty',
                    'Excessive fees without disclosure - $3.2M penalty'
                ],
                'suitability_violations': [
                    'Recommending high-risk investments to conservative investors',
                    'Inadequate due diligence on investment products',
                    'Failure to consider client financial situation'
                ]
            },
            'finra_enforcement': {
                'rule_2111_violations': [
                    'Excessive trading in customer accounts',
                    'Unsuitable investment recommendations',
                    'Inadequate supervision of recommendations'
                ]
            },
            'industry_best_practices': {
                'portfolio_construction': [
                    'Diversification across asset classes',
                    'Regular rebalancing schedules',
                    'Fee transparency and justification'
                ],
                'client_communication': [
                    'Clear risk disclosure',
                    'Regular performance reporting',
                    'Prompt conflict of interest disclosure'
                ]
            }
        }
    
    def _initialize_ai_reasoning(self) -> Dict[str, Any]:
        """Initialize AI reasoning capabilities for regulatory analysis."""
        return {
            'natural_language_processing': {
                'regulatory_text_analysis': True,
                'intent_recognition': True,
                'context_understanding': True
            },
            'expert_system': {
                'rule_inference_engine': True,
                'precedent_matching': True,
                'risk_assessment': True
            },
            'machine_learning': {
                'pattern_recognition': True,
                'anomaly_detection': True,
                'predictive_compliance': True
            }
        }
    
    async def analyze_regulatory_compliance(self, client_profile: Dict[str, Any], 
                                          portfolio: Dict[str, Any]) -> RegulatoryAnalysis:
        """
        Perform comprehensive regulatory compliance analysis using AI reasoning.
        """
        # Simulate AI processing time
        await asyncio.sleep(0.01)
        
        # Classify client for regulatory purposes
        client_classification = self._classify_client(client_profile)
        
        # Determine applicable regulations
        applicable_regulations = self._determine_applicable_regulations(
            client_classification, portfolio
        )
        
        # Perform suitability assessment
        suitability_assessment = self._assess_suitability(client_profile, portfolio)
        
        # Analyze fiduciary obligations
        fiduciary_obligations = self._analyze_fiduciary_obligations(
            client_classification, portfolio
        )
        
        # Determine disclosure requirements
        disclosure_requirements = self._determine_disclosure_requirements(
            client_classification, portfolio
        )
        
        # Identify compliance gaps
        compliance_gaps = self._identify_compliance_gaps(
            client_profile, portfolio, applicable_regulations
        )
        
        # Calculate regulatory risk score
        regulatory_risk_score = self._calculate_regulatory_risk_score(
            compliance_gaps, suitability_assessment, portfolio
        )
        
        # Generate recommended actions
        recommended_actions = self._generate_regulatory_recommendations(
            compliance_gaps, regulatory_risk_score
        )
        
        return RegulatoryAnalysis(
            client_classification=client_classification,
            applicable_regulations=applicable_regulations,
            suitability_assessment=suitability_assessment,
            fiduciary_obligations=fiduciary_obligations,
            disclosure_requirements=disclosure_requirements,
            compliance_gaps=compliance_gaps,
            regulatory_risk_score=regulatory_risk_score,
            recommended_actions=recommended_actions
        )
    
    def _classify_client(self, client_profile: Dict[str, Any]) -> str:
        """Classify client for regulatory purposes."""
        capital = client_profile.get('constraints', {}).get('capital', 0)
        income = client_profile.get('financial_info', {}).get('annual_income', 0)
        net_worth = client_profile.get('financial_info', {}).get('net_worth', capital * 4)
        
        # Accredited investor classification
        if (income >= 200000 and net_worth >= 1000000) or net_worth >= 1000000:
            return "accredited_investor"
        elif capital >= 100000:
            return "high_net_worth_retail"
        elif capital >= 25000:
            return "retail_investor"
        else:
            return "small_retail_investor"
    
    def _determine_applicable_regulations(self, client_classification: str, 
                                        portfolio: Dict[str, Any]) -> List[RegulationType]:
        """Determine which regulations apply to this client and portfolio."""
        regulations = [
            RegulationType.SEC_INVESTMENT_ADVISOR,
            RegulationType.FINRA_SUITABILITY,
            RegulationType.KNOW_YOUR_CUSTOMER
        ]
        
        # Add regulations based on client classification
        if client_classification == "accredited_investor":
            regulations.append(RegulationType.ACCREDITED_INVESTOR)
        
        # Add regulations based on portfolio characteristics
        allocation = portfolio.get('final_allocation', {})
        if allocation.get('Alternatives', 0) > 0.1:
            regulations.append(RegulationType.ACCREDITED_INVESTOR)
        
        if any(weight > 0.4 for weight in allocation.values()):
            regulations.append(RegulationType.CONCENTRATION_LIMITS)
        
        return regulations
    
    def _assess_suitability(self, client_profile: Dict[str, Any], 
                          portfolio: Dict[str, Any]) -> Dict[str, Any]:
        """Perform FINRA Rule 2111 suitability assessment."""
        goals = client_profile.get('goals', {})
        constraints = client_profile.get('constraints', {})
        
        # Risk tolerance assessment
        risk_tolerance = goals.get('risk_tolerance', 'moderate').lower()
        portfolio_risk = portfolio.get('risk_score', 0.15)
        
        risk_suitable = self._assess_risk_suitability(risk_tolerance, portfolio_risk)
        
        # Timeline suitability
        timeline = goals.get('timeline', '10 years')
        timeline_years = self._extract_years_from_timeline(timeline)
        timeline_suitable = self._assess_timeline_suitability(timeline_years, portfolio)
        
        # Liquidity suitability
        liquidity_needs = constraints.get('liquidity_needs', 'medium')
        liquidity_suitable = self._assess_liquidity_suitability(liquidity_needs, portfolio)
        
        # Overall suitability score
        suitability_score = (
            0.4 * risk_suitable +
            0.3 * timeline_suitable +
            0.3 * liquidity_suitable
        )
        
        return {
            'overall_score': suitability_score,
            'risk_suitable': risk_suitable,
            'timeline_suitable': timeline_suitable,
            'liquidity_suitable': liquidity_suitable,
            'suitability_level': 'suitable' if suitability_score >= 0.7 else 
                               'questionable' if suitability_score >= 0.5 else 'unsuitable'
        }
    
    def _assess_risk_suitability(self, risk_tolerance: str, portfolio_risk: float) -> float:
        """Assess risk suitability alignment."""
        risk_thresholds = {
            'conservative': 0.08,
            'low': 0.08,
            'moderate': 0.15,
            'moderate to high': 0.20,
            'high': 0.25,
            'aggressive': 0.30,
            'very high': 0.35
        }
        
        max_acceptable_risk = risk_thresholds.get(risk_tolerance, 0.15)
        
        if portfolio_risk <= max_acceptable_risk:
            return 1.0
        elif portfolio_risk <= max_acceptable_risk * 1.2:
            return 0.8
        elif portfolio_risk <= max_acceptable_risk * 1.5:
            return 0.6
        else:
            return 0.3
    
    def _extract_years_from_timeline(self, timeline: str) -> int:
        """Extract number of years from timeline string."""
        # Look for number patterns
        numbers = re.findall(r'\d+', timeline.lower())
        if numbers:
            return int(numbers[0])
        
        # Default mappings
        if 'short' in timeline.lower():
            return 2
        elif 'medium' in timeline.lower():
            return 7
        elif 'long' in timeline.lower():
            return 15
        else:
            return 10
    
    def _assess_timeline_suitability(self, timeline_years: int, portfolio: Dict[str, Any]) -> float:
        """Assess timeline suitability of portfolio."""
        allocation = portfolio.get('final_allocation', {})
        
        # Calculate portfolio liquidity score
        liquidity_weights = {
            'Cash': 1.0,
            'Stocks': 0.9,
            'Bonds': 0.8,
            'Technology': 0.9,
            'Healthcare': 0.9,
            'International': 0.8,
            'Real Estate': 0.6,
            'Commodities': 0.7,
            'Alternatives': 0.3
        }
        
        portfolio_liquidity = sum(
            weight * liquidity_weights.get(asset, 0.7)
            for asset, weight in allocation.items()
        )
        
        # Short timeline needs high liquidity
        if timeline_years <= 3:
            return min(1.0, portfolio_liquidity * 1.2)
        # Medium timeline is flexible
        elif timeline_years <= 10:
            return 0.9
        # Long timeline can handle illiquidity
        else:
            return 1.0
    
    def _assess_liquidity_suitability(self, liquidity_needs: str, portfolio: Dict[str, Any]) -> float:
        """Assess liquidity suitability of portfolio."""
        allocation = portfolio.get('final_allocation', {})
        
        # Calculate illiquid allocation
        illiquid_assets = ['Real Estate', 'Alternatives', 'Commodities']
        illiquid_allocation = sum(
            allocation.get(asset, 0) for asset in illiquid_assets
        )
        
        if 'high' in liquidity_needs.lower():
            return max(0.3, 1.0 - illiquid_allocation * 2)
        elif 'low' in liquidity_needs.lower():
            return 1.0
        else:  # Medium liquidity needs
            return max(0.6, 1.0 - illiquid_allocation)
    
    def _analyze_fiduciary_obligations(self, client_classification: str, 
                                     portfolio: Dict[str, Any]) -> List[str]:
        """Analyze fiduciary obligations applicable to this situation."""
        obligations = [
            "Act in client's best interest",
            "Provide suitable investment recommendations",
            "Disclose material conflicts of interest",
            "Maintain client confidentiality"
        ]
        
        if client_classification in ["accredited_investor", "high_net_worth_retail"]:
            obligations.extend([
                "Enhanced due diligence on alternative investments",
                "Sophisticated investor disclosures"
            ])
        
        # Check for complex products
        allocation = portfolio.get('final_allocation', {})
        if allocation.get('Alternatives', 0) > 0.05:
            obligations.append("Additional disclosures for alternative investments")
        
        if allocation.get('Commodities', 0) > 0.1:
            obligations.append("Commodity investment risk disclosures")
        
        return obligations
    
    def _determine_disclosure_requirements(self, client_classification: str, 
                                         portfolio: Dict[str, Any]) -> List[str]:
        """Determine required disclosures."""
        disclosures = [
            "Form ADV Part 2 brochure delivery",
            "Fee structure disclosure",
            "Investment strategy risks",
            "Performance calculation methods"
        ]
        
        allocation = portfolio.get('final_allocation', {})
        
        if allocation.get('Alternatives', 0) > 0:
            disclosures.extend([
                "Alternative investment liquidity risks",
                "Valuation methodology for illiquid assets",
                "Accredited investor verification requirements"
            ])
        
        if allocation.get('International', 0) > 0.2:
            disclosures.extend([
                "Foreign investment risks",
                "Currency exchange risks",
                "Political and regulatory risks"
            ])
        
        return disclosures
    
    def _identify_compliance_gaps(self, client_profile: Dict[str, Any], 
                                portfolio: Dict[str, Any], 
                                applicable_regulations: List[RegulationType]) -> List[str]:
        """Identify potential compliance gaps."""
        gaps = []
        
        # Check risk alignment
        risk_tolerance = client_profile.get('goals', {}).get('risk_tolerance', 'moderate')
        portfolio_risk = portfolio.get('risk_score', 0.15)
        
        if not self._assess_risk_suitability(risk_tolerance, portfolio_risk) >= 0.7:
            gaps.append("Portfolio risk may exceed client risk tolerance")
        
        # Check concentration
        allocation = portfolio.get('final_allocation', {})
        max_allocation = max(allocation.values()) if allocation else 0
        if max_allocation > 0.4:
            gaps.append("Excessive concentration in single asset class")
        
        # Check alternative investment compliance
        if allocation.get('Alternatives', 0) > 0.1:
            if RegulationType.ACCREDITED_INVESTOR not in applicable_regulations:
                gaps.append("Alternative investments may require accredited investor status")
        
        return gaps
    
    def _calculate_regulatory_risk_score(self, compliance_gaps: List[str], 
                                       suitability_assessment: Dict[str, Any], 
                                       portfolio: Dict[str, Any]) -> float:
        """Calculate overall regulatory risk score (0-1, higher = more risk)."""
        # Base risk from compliance gaps
        gap_risk = min(0.6, len(compliance_gaps) * 0.15)
        
        # Suitability risk
        suitability_risk = max(0, 1.0 - suitability_assessment.get('overall_score', 0.8))
        
        # Portfolio complexity risk
        allocation = portfolio.get('final_allocation', {})
        complexity_risk = min(0.3, (len(allocation) - 3) * 0.05)
        
        # Alternative investment risk
        alt_risk = allocation.get('Alternatives', 0) * 0.5
        
        total_risk = gap_risk + suitability_risk * 0.4 + complexity_risk + alt_risk * 0.3
        
        return min(1.0, total_risk)
    
    def _generate_regulatory_recommendations(self, compliance_gaps: List[str], 
                                          regulatory_risk_score: float) -> List[str]:
        """Generate regulatory compliance recommendations."""
        recommendations = []
        
        if regulatory_risk_score > 0.7:
            recommendations.append("Immediate regulatory review required")
            recommendations.append("Consider portfolio modifications to reduce regulatory risk")
        elif regulatory_risk_score > 0.5:
            recommendations.append("Enhanced compliance monitoring recommended")
        
        for gap in compliance_gaps:
            if "risk" in gap.lower():
                recommendations.append("Review and document risk tolerance assessment")
            elif "concentration" in gap.lower():
                recommendations.append("Consider portfolio diversification adjustments")
            elif "accredited" in gap.lower():
                recommendations.append("Verify accredited investor status before alternative investments")
        
        # General recommendations
        recommendations.extend([
            "Maintain comprehensive client documentation",
            "Regular suitability reviews (annually minimum)",
            "Document investment rationale and due diligence"
        ])
        
        return list(set(recommendations))  # Remove duplicates


class ConstraintComplianceAuditor:
    """
    Comprehensive constraint compliance auditor with regulatory oversight.
    Validates capital, contributions, and regulatory compliance.
    """
    
    def __init__(self):
        """Initialize the Constraint Compliance Auditor."""
        self.regulatory_turing = RegulatoryTuring()
        self.compliance_rules = self.regulatory_turing.compliance_rules
        self.audit_history: List[ComplianceAuditReport] = []
        
    async def perform_comprehensive_audit(self, client_profile: Dict[str, Any], 
                                        portfolio_result: Optional[PortfolioSynthesis] = None,
                                        agent_strategies: Optional[List[AgentStrategy]] = None) -> ComplianceAuditReport:
        """
        Perform comprehensive compliance audit of client profile and portfolio.
        """
        audit_id = f"audit_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        print(f"🔍 COMPLIANCE AUDIT: {audit_id}")
        print("   📋 Validating capital adequacy...")
        print("   💰 Checking contribution limits...")
        print("   ⚖️ Analyzing regulatory compliance...")
        
        # Parse client profile if needed
        if isinstance(client_profile, dict) and 'goals' in client_profile:
            parsed_profile = client_profile
        else:
            parsed_profile = parse_goal_constraints(client_profile)
        
        # Capital validation
        capital_validation = await self._validate_capital_adequacy(parsed_profile)
        
        # Contribution validation
        contribution_validation = await self._validate_contribution_limits(parsed_profile)
        
        # Regulatory analysis
        portfolio_dict = self._convert_portfolio_to_dict(portfolio_result)
        regulatory_analysis = await self.regulatory_turing.analyze_regulatory_compliance(
            parsed_profile, portfolio_dict
        )
        
        # Rule-based compliance checking
        violations = await self._check_compliance_rules(
            parsed_profile, portfolio_dict, agent_strategies
        )
        
        # Determine overall compliance level
        overall_compliance = self._determine_overall_compliance(
            capital_validation, contribution_validation, violations
        )
        
        # Generate recommendations
        recommendations = self._generate_audit_recommendations(
            capital_validation, contribution_validation, regulatory_analysis, violations
        )
        
        # Calculate audit score
        audit_score = self._calculate_audit_score(
            capital_validation, contribution_validation, violations, regulatory_analysis
        )
        
        # Create audit report
        audit_report = ComplianceAuditReport(
            audit_id=audit_id,
            timestamp=datetime.now(),
            client_id=parsed_profile.get('client_id', 'unknown'),
            portfolio_id=portfolio_result.portfolio_id if portfolio_result else 'none',
            overall_compliance=overall_compliance,
            capital_validation=capital_validation,
            contribution_validation=contribution_validation,
            regulatory_analysis=regulatory_analysis,
            violations=violations,
            recommendations=recommendations,
            requires_manual_review=overall_compliance in [ComplianceLevel.VIOLATION, ComplianceLevel.CRITICAL],
            audit_score=audit_score,
            next_review_date=datetime.now() + timedelta(days=365)
        )
        
        # Store in audit history
        self.audit_history.append(audit_report)
        
        print(f"   ✅ Compliance audit complete")
        print(f"   📊 Overall compliance: {overall_compliance.value}")
        print(f"   🎯 Audit score: {audit_score:.2f}/100")
        
        return audit_report
    
    async def _validate_capital_adequacy(self, client_profile: Dict[str, Any]) -> CapitalValidation:
        """Validate capital adequacy requirements."""
        constraints = client_profile.get('constraints', {})
        goals = client_profile.get('goals', {})
        
        # Extract capital information
        total_capital = float(constraints.get('capital', 0))
        monthly_expenses = constraints.get('monthly_expenses', total_capital * 0.003)  # Estimate 0.3% monthly
        target_amount = float(goals.get('target_amount', total_capital * 5))
        
        # Calculate requirements
        emergency_fund = monthly_expenses * 6  # 6 months recommended
        minimum_required = emergency_fund + 10000  # Minimum for investment
        available_liquidity = total_capital * 0.1  # Assume 10% liquid
        investment_capital = max(0, total_capital - emergency_fund)
        
        # Determine compliance status
        warnings = []
        recommendations = []
        
        if total_capital < minimum_required:
            compliance_status = ComplianceLevel.VIOLATION
            warnings.append(f"Total capital ${total_capital:,.0f} below minimum required ${minimum_required:,.0f}")
        elif investment_capital < 25000:
            compliance_status = ComplianceLevel.WARNING
            warnings.append("Limited investment capital may restrict diversification options")
        else:
            compliance_status = ComplianceLevel.COMPLIANT
        
        # Generate recommendations
        if total_capital < target_amount:
            gap = target_amount - total_capital
            recommendations.append(f"Consider increasing savings rate to bridge ${gap:,.0f} gap to target")
        
        if available_liquidity < emergency_fund:
            recommendations.append("Build emergency fund before increasing investment allocation")
        
        if investment_capital > 0:
            recommendations.append(f"${investment_capital:,.0f} available for investment strategies")
        
        return CapitalValidation(
            total_capital=total_capital,
            minimum_required=minimum_required,
            available_liquidity=available_liquidity,
            emergency_fund=emergency_fund,
            investment_capital=investment_capital,
            compliance_status=compliance_status,
            warnings=warnings,
            recommendations=recommendations
        )
    
    async def _validate_contribution_limits(self, client_profile: Dict[str, Any]) -> ContributionValidation:
        """Validate contribution limits and tax-advantaged account rules."""
        constraints = client_profile.get('constraints', {})
        additional_prefs = client_profile.get('additional_preferences', {})
        
        # Extract contribution information
        annual_contributions = float(constraints.get('contributions', 0)) * 12
        contribution_frequency = constraints.get('contribution_frequency', 'monthly')
        
        # 2024 contribution limits
        ira_limit = 7000  # 2024 IRA limit
        ira_catchup = 1000  # Age 50+ catchup
        k401_limit = 23000  # 2024 401(k) employee limit
        k401_catchup = 7500  # Age 50+ catchup
        
        # Extract specific contributions (if provided)
        ira_contributions = additional_prefs.get('ira_contributions', 0)
        k401_contributions = additional_prefs.get('401k_contributions', 0)
        
        # Calculate excess contributions
        client_age = additional_prefs.get('age', 35)
        catchup_eligible = client_age >= 50
        
        effective_ira_limit = ira_limit + (ira_catchup if catchup_eligible else 0)
        effective_k401_limit = k401_limit + (k401_catchup if catchup_eligible else 0)
        
        violations = []
        if ira_contributions > effective_ira_limit:
            violations.append(f"IRA contributions ${ira_contributions:,.0f} exceed limit ${effective_ira_limit:,.0f}")
        
        if k401_contributions > effective_k401_limit:
            violations.append(f"401(k) contributions ${k401_contributions:,.0f} exceed limit ${effective_k401_limit:,.0f}")
        
        total_tax_advantaged = ira_contributions + k401_contributions
        excess_contributions = max(0, total_tax_advantaged - (effective_ira_limit + effective_k401_limit))
        
        # Determine compliance status
        if violations:
            compliance_status = ComplianceLevel.VIOLATION
        elif total_tax_advantaged > (effective_ira_limit + effective_k401_limit) * 0.9:
            compliance_status = ComplianceLevel.WARNING
        else:
            compliance_status = ComplianceLevel.COMPLIANT
        
        contribution_limits = {
            'ira_limit': effective_ira_limit,
            '401k_limit': effective_k401_limit,
            'total_tax_advantaged': effective_ira_limit + effective_k401_limit
        }
        
        return ContributionValidation(
            annual_contributions=annual_contributions,
            contribution_frequency=contribution_frequency,
            contribution_limits=contribution_limits,
            ira_contributions=ira_contributions,
            ira_limit=effective_ira_limit,
            k401_contributions=k401_contributions,
            k401_limit=effective_k401_limit,
            excess_contributions=excess_contributions,
            compliance_status=compliance_status,
            violations=violations
        )
    
    async def _check_compliance_rules(self, client_profile: Dict[str, Any], 
                                    portfolio: Dict[str, Any], 
                                    agent_strategies: Optional[List[AgentStrategy]]) -> List[ComplianceViolation]:
        """Check all compliance rules against client profile and portfolio."""
        violations = []
        
        for rule in self.compliance_rules:
            violation = await self._evaluate_compliance_rule(rule, client_profile, portfolio)
            if violation:
                violations.append(violation)
        
        return violations
    
    async def _evaluate_compliance_rule(self, rule: ComplianceRule, 
                                      client_profile: Dict[str, Any], 
                                      portfolio: Dict[str, Any]) -> Optional[ComplianceViolation]:
        """Evaluate a specific compliance rule."""
        try:
            # Rule-specific evaluation logic
            if rule.rule_id == "CAP_001":  # Emergency fund requirement
                return self._check_emergency_fund_rule(rule, client_profile)
            elif rule.rule_id == "CAP_002":  # Investment capital adequacy
                return self._check_investment_capital_rule(rule, client_profile)
            elif rule.rule_id == "RISK_001":  # Risk tolerance alignment
                return self._check_risk_tolerance_rule(rule, client_profile, portfolio)
            elif rule.rule_id == "DIV_001":  # Concentration limits
                return self._check_concentration_rule(rule, portfolio)
            elif rule.rule_id == "ACC_001":  # Accredited investor requirements
                return self._check_accredited_investor_rule(rule, client_profile, portfolio)
            elif rule.rule_id.startswith("TAX_"):  # Tax compliance rules
                return self._check_tax_compliance_rule(rule, client_profile)
            
            return None
            
        except Exception as e:
            # Log error and continue with other rules
            print(f"Error evaluating rule {rule.rule_id}: {e}")
            return None
    
    def _check_investment_capital_rule(self, rule: ComplianceRule, 
                                     client_profile: Dict[str, Any]) -> Optional[ComplianceViolation]:
        """Check investment capital adequacy rule."""
        constraints = client_profile.get('constraints', {})
        capital = float(constraints.get('capital', 0))
        monthly_expenses = constraints.get('monthly_expenses', capital * 0.003)
        emergency_fund = monthly_expenses * 6
        investment_capital = max(0, capital - emergency_fund)
        
        min_investment = rule.threshold_values.get('min_investment', 10000)
        min_diversified = rule.threshold_values.get('min_diversified', 50000)
        
        if investment_capital < min_investment:
            return ComplianceViolation(
                violation_id=f"violation_{rule.rule_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                rule_id=rule.rule_id,
                severity=rule.severity,
                description=f"Investment capital ${investment_capital:,.0f} below minimum ${min_investment:,.0f}",
                affected_component="investment_capital",
                current_value=investment_capital,
                required_value=min_investment,
                recommendation=f"Increase investment capital to at least ${min_investment:,.0f}",
                auto_fixable=False
            )
        elif investment_capital < min_diversified:
            return ComplianceViolation(
                violation_id=f"violation_{rule.rule_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                rule_id=rule.rule_id,
                severity=ComplianceLevel.WARNING,
                description=f"Investment capital ${investment_capital:,.0f} may limit diversification options",
                affected_component="investment_capital",
                current_value=investment_capital,
                required_value=min_diversified,
                recommendation=f"Consider increasing capital to ${min_diversified:,.0f} for better diversification",
                auto_fixable=False
            )
        return None
    
    def _check_emergency_fund_rule(self, rule: ComplianceRule, 
                                 client_profile: Dict[str, Any]) -> Optional[ComplianceViolation]:
        """Check emergency fund adequacy rule."""
        constraints = client_profile.get('constraints', {})
        capital = float(constraints.get('capital', 0))
        monthly_expenses = constraints.get('monthly_expenses', capital * 0.003)
        
        min_months = rule.threshold_values.get('min_months', 3)
        required_emergency_fund = monthly_expenses * min_months
        assumed_emergency_fund = capital * 0.1  # Assume 10% kept as emergency fund
        
        if assumed_emergency_fund < required_emergency_fund:
            return ComplianceViolation(
                violation_id=f"violation_{rule.rule_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                rule_id=rule.rule_id,
                severity=rule.severity,
                description=f"Emergency fund ${assumed_emergency_fund:,.0f} below recommended ${required_emergency_fund:,.0f}",
                affected_component="capital_allocation",
                current_value=assumed_emergency_fund,
                required_value=required_emergency_fund,
                recommendation=f"Increase emergency fund to ${required_emergency_fund:,.0f} ({min_months} months expenses)",
                auto_fixable=False
            )
        return None
    
    def _check_risk_tolerance_rule(self, rule: ComplianceRule, 
                                 client_profile: Dict[str, Any], 
                                 portfolio: Dict[str, Any]) -> Optional[ComplianceViolation]:
        """Check risk tolerance alignment rule."""
        goals = client_profile.get('goals', {})
        risk_tolerance = goals.get('risk_tolerance', 'moderate').lower()
        portfolio_risk = portfolio.get('risk_score', 0.15)
        
        risk_limits = rule.threshold_values
        max_risk = risk_limits.get(risk_tolerance, risk_limits.get('moderate', 0.15))
        
        if portfolio_risk > max_risk * 1.2:  # 20% tolerance
            return ComplianceViolation(
                violation_id=f"violation_{rule.rule_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                rule_id=rule.rule_id,
                severity=rule.severity,
                description=f"Portfolio risk {portfolio_risk:.1%} exceeds client risk tolerance limit {max_risk:.1%}",
                affected_component="portfolio_risk",
                current_value=portfolio_risk,
                required_value=max_risk,
                recommendation=f"Reduce portfolio risk to below {max_risk:.1%} through reallocation",
                auto_fixable=True,
                fix_action="reduce_risk_allocation"
            )
        return None
    
    def _check_concentration_rule(self, rule: ComplianceRule, 
                                portfolio: Dict[str, Any]) -> Optional[ComplianceViolation]:
        """Check asset concentration limits."""
        allocation = portfolio.get('final_allocation', {})
        if not allocation:
            return None
        
        max_single_asset = rule.threshold_values.get('max_single_asset', 0.4)
        current_max = max(allocation.values())
        
        if current_max > max_single_asset:
            concentrated_asset = max(allocation.items(), key=lambda x: x[1])
            return ComplianceViolation(
                violation_id=f"violation_{rule.rule_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                rule_id=rule.rule_id,
                severity=rule.severity,
                description=f"Asset concentration {current_max:.1%} in {concentrated_asset[0]} exceeds limit {max_single_asset:.1%}",
                affected_component="asset_allocation",
                current_value=current_max,
                required_value=max_single_asset,
                recommendation=f"Reduce {concentrated_asset[0]} allocation to below {max_single_asset:.1%}",
                auto_fixable=True,
                fix_action="diversify_allocation"
            )
        return None
    
    def _check_accredited_investor_rule(self, rule: ComplianceRule, 
                                      client_profile: Dict[str, Any], 
                                      portfolio: Dict[str, Any]) -> Optional[ComplianceViolation]:
        """Check accredited investor requirements for alternative investments."""
        allocation = portfolio.get('final_allocation', {})
        alt_allocation = allocation.get('Alternatives', 0)
        
        if alt_allocation > 0.05:  # More than 5% in alternatives
            # Check if client meets accredited investor requirements
            financial_info = client_profile.get('financial_info', {})
            constraints = client_profile.get('constraints', {})
            
            income = financial_info.get('annual_income', 0)
            net_worth = financial_info.get('net_worth', constraints.get('capital', 0) * 4)
            
            min_income = rule.threshold_values.get('min_income', 200000)
            min_net_worth = rule.threshold_values.get('min_net_worth', 1000000)
            
            if income < min_income and net_worth < min_net_worth:
                return ComplianceViolation(
                    violation_id=f"violation_{rule.rule_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                    rule_id=rule.rule_id,
                    severity=rule.severity,
                    description=f"Alternative investments {alt_allocation:.1%} may require accredited investor status",
                    affected_component="alternative_investments",
                    current_value=alt_allocation,
                    required_value=0.05,
                    recommendation="Verify accredited investor status or reduce alternative investment allocation",
                    auto_fixable=False
                )
        return None
    
    def _check_tax_compliance_rule(self, rule: ComplianceRule, 
                                 client_profile: Dict[str, Any]) -> Optional[ComplianceViolation]:
        """Check tax-related compliance rules."""
        additional_prefs = client_profile.get('additional_preferences', {})
        
        if rule.rule_id == "TAX_IRA_001":
            ira_contributions = additional_prefs.get('ira_contributions', 0)
            limit = rule.threshold_values.get('2024_limit', 7000)
            
            if ira_contributions > limit:
                return ComplianceViolation(
                    violation_id=f"violation_{rule.rule_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                    rule_id=rule.rule_id,
                    severity=rule.severity,
                    description=f"IRA contributions ${ira_contributions:,.0f} exceed annual limit ${limit:,.0f}",
                    affected_component="ira_contributions",
                    current_value=ira_contributions,
                    required_value=limit,
                    recommendation=f"Reduce IRA contributions to ${limit:,.0f} or consider excess contribution removal",
                    auto_fixable=False
                )
        
        return None
    
    def _convert_portfolio_to_dict(self, portfolio_result: Optional[PortfolioSynthesis]) -> Dict[str, Any]:
        """Convert PortfolioSynthesis to dictionary format."""
        if not portfolio_result:
            return {}
        
        return {
            'portfolio_id': portfolio_result.portfolio_id,
            'final_allocation': portfolio_result.final_allocation,
            'expected_return': portfolio_result.expected_return,
            'risk_score': portfolio_result.risk_score,
            'cost_score': portfolio_result.cost_score,
            'sharpe_ratio': portfolio_result.sharpe_ratio,
            'synthesis_confidence': portfolio_result.synthesis_confidence
        }
    
    def _determine_overall_compliance(self, capital_validation: CapitalValidation,
                                    contribution_validation: ContributionValidation,
                                    violations: List[ComplianceViolation]) -> ComplianceLevel:
        """Determine overall compliance level."""
        # Check for critical violations
        critical_violations = [v for v in violations if v.severity == ComplianceLevel.CRITICAL]
        if critical_violations or capital_validation.compliance_status == ComplianceLevel.VIOLATION:
            return ComplianceLevel.CRITICAL
        
        # Check for violations
        violation_level = [v for v in violations if v.severity == ComplianceLevel.VIOLATION]
        if violation_level or contribution_validation.compliance_status == ComplianceLevel.VIOLATION:
            return ComplianceLevel.VIOLATION
        
        # Check for warnings
        warning_violations = [v for v in violations if v.severity == ComplianceLevel.WARNING]
        if (warning_violations or 
            capital_validation.compliance_status == ComplianceLevel.WARNING or
            contribution_validation.compliance_status == ComplianceLevel.WARNING):
            return ComplianceLevel.WARNING
        
        return ComplianceLevel.COMPLIANT
    
    def _generate_audit_recommendations(self, capital_validation: CapitalValidation,
                                      contribution_validation: ContributionValidation,
                                      regulatory_analysis: RegulatoryAnalysis,
                                      violations: List[ComplianceViolation]) -> List[str]:
        """Generate comprehensive audit recommendations."""
        recommendations = []
        
        # Capital recommendations
        recommendations.extend(capital_validation.recommendations)
        
        # Regulatory recommendations
        recommendations.extend(regulatory_analysis.recommended_actions)
        
        # Violation-specific recommendations
        for violation in violations:
            if violation.recommendation not in recommendations:
                recommendations.append(violation.recommendation)
        
        # General compliance recommendations
        recommendations.extend([
            "Conduct annual compliance review",
            "Maintain detailed client documentation",
            "Regular monitoring of regulatory changes",
            "Document investment decision rationale"
        ])
        
        return list(set(recommendations))  # Remove duplicates
    
    def _calculate_audit_score(self, capital_validation: CapitalValidation,
                             contribution_validation: ContributionValidation,
                             violations: List[ComplianceViolation],
                             regulatory_analysis: RegulatoryAnalysis) -> float:
        """Calculate overall audit score (0-100)."""
        base_score = 100.0
        
        # Deduct for capital issues
        if capital_validation.compliance_status == ComplianceLevel.VIOLATION:
            base_score -= 25
        elif capital_validation.compliance_status == ComplianceLevel.WARNING:
            base_score -= 10
        
        # Deduct for contribution issues
        if contribution_validation.compliance_status == ComplianceLevel.VIOLATION:
            base_score -= 20
        elif contribution_validation.compliance_status == ComplianceLevel.WARNING:
            base_score -= 5
        
        # Deduct for violations
        for violation in violations:
            if violation.severity == ComplianceLevel.CRITICAL:
                base_score -= 15
            elif violation.severity == ComplianceLevel.VIOLATION:
                base_score -= 10
            elif violation.severity == ComplianceLevel.WARNING:
                base_score -= 3
        
        # Deduct for regulatory risk
        regulatory_risk = regulatory_analysis.regulatory_risk_score
        base_score -= regulatory_risk * 20
        
        return max(0.0, base_score)
    
    def get_audit_summary(self, audit_report: ComplianceAuditReport) -> Dict[str, Any]:
        """Get comprehensive audit summary."""
        return {
            'audit_overview': {
                'audit_id': audit_report.audit_id,
                'timestamp': audit_report.timestamp.isoformat(),
                'overall_compliance': audit_report.overall_compliance.value,
                'audit_score': f"{audit_report.audit_score:.1f}/100",
                'requires_manual_review': audit_report.requires_manual_review
            },
            'capital_assessment': {
                'status': audit_report.capital_validation.compliance_status.value,
                'total_capital': f"${audit_report.capital_validation.total_capital:,.0f}",
                'investment_capital': f"${audit_report.capital_validation.investment_capital:,.0f}",
                'warnings': len(audit_report.capital_validation.warnings)
            },
            'contribution_assessment': {
                'status': audit_report.contribution_validation.compliance_status.value,
                'annual_contributions': f"${audit_report.contribution_validation.annual_contributions:,.0f}",
                'violations': len(audit_report.contribution_validation.violations)
            },
            'regulatory_assessment': {
                'client_classification': audit_report.regulatory_analysis.client_classification,
                'applicable_regulations': len(audit_report.regulatory_analysis.applicable_regulations),
                'suitability_level': audit_report.regulatory_analysis.suitability_assessment.get('suitability_level', 'unknown'),
                'regulatory_risk_score': f"{audit_report.regulatory_analysis.regulatory_risk_score:.2f}"
            },
            'violations_summary': {
                'total_violations': len(audit_report.violations),
                'critical': len([v for v in audit_report.violations if v.severity == ComplianceLevel.CRITICAL]),
                'violations': len([v for v in audit_report.violations if v.severity == ComplianceLevel.VIOLATION]),
                'warnings': len([v for v in audit_report.violations if v.severity == ComplianceLevel.WARNING])
            },
            'key_recommendations': audit_report.recommendations[:5],
            'next_review_date': audit_report.next_review_date.strftime('%Y-%m-%d')
        }


# Convenience function for easy integration
async def perform_compliance_audit(client_profile: Dict[str, Any],
                                 portfolio_result: Optional[PortfolioSynthesis] = None,
                                 agent_strategies: Optional[List[AgentStrategy]] = None) -> ComplianceAuditReport:
    """
    Convenience function to perform comprehensive compliance audit.
    """
    auditor = ConstraintComplianceAuditor()
    return await auditor.perform_comprehensive_audit(client_profile, portfolio_result, agent_strategies)


if __name__ == "__main__":
    # Example usage
    async def main():
        # Sample client profile for testing
        client_profile = {
            "goals": {
                "strategy": "aggressive growth",
                "timeline": "15 years",
                "target_amount": 1500000,
                "risk_tolerance": "high"
            },
            "constraints": {
                "capital": 200000,
                "contributions": 3000,
                "contribution_frequency": "monthly",
                "max_risk_percentage": 80,
                "monthly_expenses": 5000
            },
            "additional_preferences": {
                "age": 35,
                "ira_contributions": 6000,
                "401k_contributions": 15000,
                "esg_investing": True
            },
            "financial_info": {
                "annual_income": 120000,
                "net_worth": 400000
            }
        }
        
        # Perform compliance audit
        audit_report = await perform_compliance_audit(client_profile)
        
        # Display results
        auditor = ConstraintComplianceAuditor()
        summary = auditor.get_audit_summary(audit_report)
        print(json.dumps(summary, indent=2))
    
    # Run example
    asyncio.run(main())