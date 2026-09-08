import os

from fastapi import Depends, FastAPI, Header, HTTPException
from pydantic import BaseModel

from app.models import Observations
from app.triage import TriageAssessment, assess


VALID_API_KEYS = {
    key.strip()
    for key in os.getenv("TRIAGE_API_KEYS", "dev-demo-key").split(",")
    if key.strip()
}


class TriageResponse(BaseModel):
    """API response for triage assessment."""

    patient_id: str | None
    triage_category: str
    priority: str
    reason: str


app = FastAPI(
    title="Clinical Triage API",
    description="Medical triage assessment service",
    version="1.0.0",
)


def require_api_key(x_api_key: str | None = Header(default=None, alias="X-API-Key")) -> str:
    """Validate the caller's API key before allowing access."""
    if not x_api_key or x_api_key not in VALID_API_KEYS:
        raise HTTPException(status_code=401, detail="Invalid or missing API key")
    return x_api_key


@app.get("/")
def home() -> dict[str, str]:
    """Service health and info endpoint."""
    return {"service": "Triage API", "status": "running"}


@app.get("/health")
def health() -> dict[str, str]:
    """Health check endpoint."""
    return {"status": "ok"}


@app.post("/triage", response_model=TriageResponse)
def triage_assessment(
    obs: Observations,
    api_key: str = Depends(require_api_key),
) -> TriageResponse:
    """Assess patient triage category based on vital observations.

    Requires a valid X-API-Key header to protect the endpoint.
    """
    _ = api_key  # keep the dependency required for auth check
    assessment: TriageAssessment = assess(obs)

    return TriageResponse(
        patient_id=obs.patient_id,
        triage_category=assessment.category.value,
        priority=assessment.priority.value,
        reason=assessment.reason,
    )