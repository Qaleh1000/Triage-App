from enum import Enum
from typing import NamedTuple
from app.models import Observations


class TriageCategory(str, Enum):
    """Triage color categories following industry standard."""
    RED = "RED"
    ORANGE = "ORANGE"
    YELLOW = "YELLOW"
    GREEN = "GREEN"


class TriagePriority(str, Enum):
    """Triage priority levels."""
    IMMEDIATE = "Immediate"
    URGENT = "Urgent"
    STANDARD = "Standard"
    ROUTINE = "Routine"


class TriageAssessment(NamedTuple):
    """Structured triage assessment result."""
    category: TriageCategory
    priority: TriagePriority
    reason: str


# Clinical thresholds (constants)
OXYGEN_SATURATION_CRITICAL = 92
RESPIRATORY_RATE_CRITICAL = 30
HEART_RATE_URGENT = 120
TEMPERATURE_ELEVATED = 38.5


def assess(obs: Observations) -> TriageAssessment:
    """Assess patient observations and assign triage category.
    
    Uses standardized clinical thresholds to determine urgency of care.
    Critical conditions (RED) take precedence over less urgent conditions.
    
    Args:
        obs: Patient observations including vital signs.
        
    Returns:
        TriageAssessment containing category, priority, and clinical reason.
    """
    if obs.oxygen_saturation < OXYGEN_SATURATION_CRITICAL:
        return TriageAssessment(
            TriageCategory.RED,
            TriagePriority.IMMEDIATE,
            "Low oxygen saturation"
        )

    if obs.chest_pain:
        return TriageAssessment(
            TriageCategory.RED,
            TriagePriority.IMMEDIATE,
            "Chest pain"
        )

    if obs.respiratory_rate > RESPIRATORY_RATE_CRITICAL:
        return TriageAssessment(
            TriageCategory.RED,
            TriagePriority.IMMEDIATE,
            "High respiratory rate"
        )

    if obs.heart_rate > HEART_RATE_URGENT:
        return TriageAssessment(
            TriageCategory.ORANGE,
            TriagePriority.URGENT,
            "High heart rate"
        )

    if obs.temperature > TEMPERATURE_ELEVATED:
        return TriageAssessment(
            TriageCategory.YELLOW,
            TriagePriority.STANDARD,
            "Fever"
        )

    return TriageAssessment(
        TriageCategory.GREEN,
        TriagePriority.ROUTINE,
        "Stable"
    )