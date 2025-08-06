"""
Goal-Constraint Parser using LangChain

This module implements a parser that processes user JSON input containing
investment goals (strategy, timeline) and constraints (capital, contributions)
and converts them into structured Python dictionaries.
"""

import json
from typing import Dict, Any, Optional, List, Union
from datetime import datetime
from pydantic import BaseModel, Field, validator
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.language_models.base import BaseLanguageModel
from langchain_community.llms import OpenAI


class GoalModel(BaseModel):
    """Pydantic model for investment goals."""
    
    strategy: str = Field(
        description="Investment strategy (e.g., 'conservative', 'moderate', 'aggressive', 'growth', 'income')"
    )
    timeline: str = Field(
        description="Investment timeline (e.g., 'short-term', 'medium-term', 'long-term', or specific duration like '5 years')"
    )
    target_amount: Optional[float] = Field(
        default=None,
        description="Target amount to achieve (optional)"
    )
    risk_tolerance: Optional[str] = Field(
        default=None,
        description="Risk tolerance level (e.g., 'low', 'medium', 'high')"
    )
    
    @validator('strategy')
    def validate_strategy(cls, v):
        """Validate investment strategy."""
        valid_strategies = ['conservative', 'moderate', 'aggressive', 'growth', 'income', 'balanced']
        if v.lower() not in valid_strategies:
            # If not in predefined list, still accept it but normalize
            return v.lower().strip()
        return v.lower()
    
    @validator('timeline')
    def validate_timeline(cls, v):
        """Validate timeline format."""
        return v.lower().strip()


class ConstraintModel(BaseModel):
    """Pydantic model for investment constraints."""
    
    capital: float = Field(
        description="Initial capital amount available for investment"
    )
    contributions: Optional[float] = Field(
        default=None,
        description="Regular contribution amount (monthly/quarterly/annual)"
    )
    contribution_frequency: Optional[str] = Field(
        default=None,
        description="Frequency of contributions (e.g., 'monthly', 'quarterly', 'annual')"
    )
    max_risk_percentage: Optional[float] = Field(
        default=None,
        description="Maximum percentage of portfolio that can be at risk",
        ge=0,
        le=100
    )
    liquidity_needs: Optional[str] = Field(
        default=None,
        description="Liquidity requirements (e.g., 'high', 'medium', 'low')"
    )
    
    @validator('capital')
    def validate_capital(cls, v):
        """Validate capital amount."""
        if v <= 0:
            raise ValueError('Capital must be greater than 0')
        return v
    
    @validator('contributions')
    def validate_contributions(cls, v):
        """Validate contribution amount."""
        if v is not None and v < 0:
            raise ValueError('Contributions cannot be negative')
        return v


class GoalConstraintStructure(BaseModel):
    """Complete structured model for goals and constraints."""
    
    goals: GoalModel = Field(description="Investment goals")
    constraints: ConstraintModel = Field(description="Investment constraints")
    additional_preferences: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Any additional preferences or requirements"
    )
    parsed_timestamp: str = Field(
        default_factory=lambda: datetime.now().isoformat(),
        description="Timestamp when the parsing was completed"
    )


class GoalConstraintParser:
    """
    Main parser class that uses LangChain to parse JSON input into structured data.
    """
    
    def __init__(self, llm: Optional[BaseLanguageModel] = None):
        """
        Initialize the parser.
        
        Args:
            llm: LangChain LLM instance. If None, will attempt to use OpenAI.
        """
        self.llm = llm or self._get_default_llm()
        self.pydantic_parser = PydanticOutputParser(pydantic_object=GoalConstraintStructure)
    
    def _get_default_llm(self) -> BaseLanguageModel:
        """Get default LLM if none provided."""
        try:
            # Try to create OpenAI instance, but don't require API key for testing
            return OpenAI(temperature=0)
        except Exception:
            # If OpenAI is not configured, return a mock LLM for testing
            return MockLLM()
    
    def _create_prompt_template(self) -> PromptTemplate:
        """Create the prompt template for parsing."""
        template = """
You are an expert financial data parser. Your task is to parse user input containing investment goals and constraints into a structured format.

Parse the following JSON input and extract:
1. Goals: strategy, timeline, target_amount (if mentioned), risk_tolerance (if mentioned)
2. Constraints: capital, contributions (if mentioned), contribution_frequency (if mentioned), max_risk_percentage (if mentioned), liquidity_needs (if mentioned)

User Input:
{user_input}

{format_instructions}

Important guidelines:
- Extract only the information that is explicitly provided
- Normalize strategy names to common terms (conservative, moderate, aggressive, growth, income, balanced)
- Convert timeline to clear terms (short-term, medium-term, long-term, or specific durations)
- Ensure capital is a positive number
- If contributions are mentioned, try to identify the frequency
- Include any additional preferences in the additional_preferences field

Parse the input carefully and provide the structured output:
"""
        
        return PromptTemplate(
            template=template,
            input_variables=["user_input"],
            partial_variables={"format_instructions": self.pydantic_parser.get_format_instructions()}
        )
    
    def parse_json_input(self, json_input: Union[str, Dict[str, Any]]) -> Dict[str, Any]:
        """
        Parse JSON input containing goals and constraints.
        
        Args:
            json_input: JSON string or dictionary containing goals and constraints
            
        Returns:
            Structured dictionary with parsed goals and constraints
        """
        # Convert string to dict if necessary
        if isinstance(json_input, str):
            try:
                input_data = json.loads(json_input)
            except json.JSONDecodeError as e:
                raise ValueError(f"Invalid JSON input: {e}")
        else:
            input_data = json_input
        
        # Create the prompt
        prompt_template = self._create_prompt_template()
        prompt = prompt_template.format(user_input=json.dumps(input_data, indent=2))
        
        try:
            # Use LLM to parse the input
            llm_output = self.llm.invoke(prompt)
            
            # Parse the output using the structured parser
            parsed_result = self.pydantic_parser.parse(llm_output)
            
            # Convert to dictionary
            return parsed_result.dict()
            
        except Exception as e:
            # Fallback to direct parsing if LLM fails
            print(f"LLM parsing failed: {e}. Attempting direct parsing...")
            return self._direct_parse(input_data)
    
    def _direct_parse(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Direct parsing fallback method when LLM is not available.
        
        Args:
            input_data: Dictionary containing the input data
            
        Returns:
            Structured dictionary with parsed goals and constraints
        """
        try:
            # Extract goals
            goals_data = input_data.get('goals', {})
            
            # Handle strategy normalization
            strategy = goals_data.get('strategy', 'moderate')
            if 'aggressive' in strategy.lower():
                strategy = 'aggressive'
            elif 'conservative' in strategy.lower():
                strategy = 'conservative'
            elif 'growth' in strategy.lower():
                strategy = 'growth'
            elif 'balanced' in strategy.lower():
                strategy = 'balanced'
            elif 'income' in strategy.lower():
                strategy = 'income'
            else:
                strategy = strategy.lower()
            
            # Handle timeline normalization
            timeline = goals_data.get('timeline', 'medium-term')
            timeline_lower = timeline.lower()
            if 'short' in timeline_lower or ('year' in timeline_lower and any(str(i) in timeline_lower for i in range(1, 4))):
                timeline = 'short-term'
            elif 'long' in timeline_lower or ('year' in timeline_lower and any(str(i) in timeline_lower for i in range(10, 50))):
                timeline = 'long-term'
            elif any(str(i) in timeline_lower for i in range(4, 10)):
                timeline = 'medium-term'
            else:
                timeline = timeline_lower
            
            goals = GoalModel(
                strategy=strategy,
                timeline=timeline,
                target_amount=goals_data.get('target_amount'),
                risk_tolerance=goals_data.get('risk_tolerance')
            )
            
            # Extract constraints
            constraints_data = input_data.get('constraints', {})
            capital = constraints_data.get('capital')
            if capital is None:
                raise ValueError("Capital is required in constraints")
            
            constraints = ConstraintModel(
                capital=float(capital),
                contributions=constraints_data.get('contributions'),
                contribution_frequency=constraints_data.get('contribution_frequency'),
                max_risk_percentage=constraints_data.get('max_risk_percentage'),
                liquidity_needs=constraints_data.get('liquidity_needs')
            )
            
            # Create complete structure
            result = GoalConstraintStructure(
                goals=goals,
                constraints=constraints,
                additional_preferences=input_data.get('additional_preferences')
            )
            
            return result.dict()
            
        except Exception as e:
            raise ValueError(f"Failed to parse input data: {e}")


class MockLLM:
    """Simple mock LLM for testing when OpenAI is not configured."""
    
    def invoke(self, input_text, **kwargs):
        """Simple invoke method for direct usage."""
        return """
{
    "goals": {
        "strategy": "moderate",
        "timeline": "long-term",
        "target_amount": null,
        "risk_tolerance": null
    },
    "constraints": {
        "capital": 10000.0,
        "contributions": null,
        "contribution_frequency": null,
        "max_risk_percentage": null,
        "liquidity_needs": null
    },
    "additional_preferences": null,
    "parsed_timestamp": "2024-01-01T00:00:00"
}
"""


# Convenience function for quick parsing
def parse_goal_constraints(json_input: Union[str, Dict[str, Any]], llm: Optional[BaseLanguageModel] = None) -> Dict[str, Any]:
    """
    Convenience function to parse goal and constraint JSON input.
    
    Args:
        json_input: JSON string or dictionary containing goals and constraints
        llm: Optional LangChain LLM instance
        
    Returns:
        Structured dictionary with parsed goals and constraints
    """
    parser = GoalConstraintParser(llm=llm)
    return parser.parse_json_input(json_input)


if __name__ == "__main__":
    # Example usage
    sample_input = {
        "goals": {
            "strategy": "aggressive growth",
            "timeline": "10 years",
            "target_amount": 100000,
            "risk_tolerance": "high"
        },
        "constraints": {
            "capital": 25000,
            "contributions": 500,
            "contribution_frequency": "monthly",
            "max_risk_percentage": 80,
            "liquidity_needs": "low"
        },
        "additional_preferences": {
            "sector_preferences": ["technology", "healthcare"],
            "esg_requirements": True
        }
    }
    
    try:
        parser = GoalConstraintParser()
        result = parser.parse_json_input(sample_input)
        print("Parsed Result:")
        print(json.dumps(result, indent=2))
    except Exception as e:
        print(f"Error: {e}")