from pydantic import BaseModel, Field


class Observations(BaseModel):
    """Patient vital observations for triage assessment.
    
    Attributes:
        patient_id: Unique identifier for patient (optional).
        heart_rate: Beats per minute (typically 60-100).
        temperature: Body temperature in Celsius.
        respiratory_rate: Breaths per minute (typically 12-20).
        oxygen_saturation: SpO2 percentage (typically 95-100).
        chest_pain: Presence of chest pain symptom.
    """
    patient_id: str | None = Field(None, description="Patient identifier")
    heart_rate: int = Field(..., gt=0, description="Beats per minute")
    temperature: float = Field(..., gt=35, lt=43, description="Temperature in Celsius")
    respiratory_rate: int = Field(..., gt=0, description="Breaths per minute")
    oxygen_saturation: int = Field(..., ge=0, le=100, description="SpO2 percentage")
    chest_pain: bool = Field(False, description="Presence of chest pain")