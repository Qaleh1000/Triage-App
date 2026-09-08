import pytest
from app.models import Observations
from app.triage import assess, TriageCategory, TriagePriority


# Test 1: Critical oxygen saturation
def test_low_oxygen_saturation():
    """Test that low oxygen saturation triggers RED alert."""
    obs = Observations(
        patient_id="P001",
        heart_rate=80,
        temperature=37.0,
        respiratory_rate=16,
        oxygen_saturation=90,  # Below 92 = critical
        chest_pain=False
    )
    
    result = assess(obs)
    
    # These assertions check that the result is correct
    assert result.category == TriageCategory.RED
    assert result.priority == TriagePriority.IMMEDIATE
    assert "oxygen" in result.reason.lower()  # Reason should mention oxygen


# Test 2: Chest pain
def test_chest_pain_alert():
    """Test that chest pain triggers RED alert."""
    obs = Observations(
        patient_id="P002",
        heart_rate=80,
        temperature=37.0,
        respiratory_rate=16,
        oxygen_saturation=98,
        chest_pain=True  # This should trigger RED
    )
    
    result = assess(obs)
    
    assert result.category == TriageCategory.RED
    assert result.priority == TriagePriority.IMMEDIATE
    assert "chest pain" in result.reason.lower()


# Test 3: High respiratory rate
def test_high_respiratory_rate():
    """Test that high respiratory rate triggers RED alert."""
    obs = Observations(
        patient_id="P003",
        heart_rate=80,
        temperature=37.0,
        respiratory_rate=35,  # Above 30 = critical
        oxygen_saturation=98,
        chest_pain=False
    )
    
    result = assess(obs)
    
    assert result.category == TriageCategory.RED
    assert result.priority == TriagePriority.IMMEDIATE


# Test 4: Elevated heart rate (not critical)
def test_elevated_heart_rate():
    """Test that elevated heart rate (but not critical) triggers ORANGE alert."""
    obs = Observations(
        patient_id="P004",
        heart_rate=130,  # Above 120 = urgent but not immediate
        temperature=37.0,
        respiratory_rate=18,
        oxygen_saturation=98,
        chest_pain=False
    )
    
    result = assess(obs)
    
    assert result.category == TriageCategory.ORANGE
    assert result.priority == TriagePriority.URGENT
    assert "heart rate" in result.reason.lower()


# Test 5: Fever
def test_fever():
    """Test that fever triggers YELLOW alert."""
    obs = Observations(
        patient_id="P005",
        heart_rate=80,
        temperature=39.0,  # Above 38.5 = fever
        respiratory_rate=18,
        oxygen_saturation=98,
        chest_pain=False
    )
    
    result = assess(obs)
    
    assert result.category == TriageCategory.YELLOW
    assert result.priority == TriagePriority.STANDARD
    assert "fever" in result.reason.lower()


# Test 6: All vitals normal
def test_stable_patient():
    """Test that all normal vitals trigger GREEN (routine) alert."""
    obs = Observations(
        patient_id="P006",
        heart_rate=72,
        temperature=37.0,
        respiratory_rate=16,
        oxygen_saturation=98,
        chest_pain=False
    )
    
    result = assess(obs)
    
    assert result.category == TriageCategory.GREEN
    assert result.priority == TriagePriority.ROUTINE
    assert "stable" in result.reason.lower()


# Test 7: Multiple conditions - RED takes precedence
def test_red_takes_precedence():
    """Test that RED takes precedence over other conditions."""
    obs = Observations(
        patient_id="P007",
        heart_rate=130,  # Would be ORANGE normally
        temperature=39.0,  # Would be YELLOW normally
        respiratory_rate=16,
        oxygen_saturation=90,  # RED - critical
        chest_pain=False
    )
    
    result = assess(obs)
    
    # Even though multiple conditions exist, RED (oxygen) takes priority
    assert result.category == TriageCategory.RED
    assert result.priority == TriagePriority.IMMEDIATE


# Test 8: Boundary condition - exactly at threshold
def test_boundary_oxygen_saturation():
    """Test edge case: oxygen saturation exactly at 92 (should be OK)."""
    obs = Observations(
        patient_id="P008",
        heart_rate=80,
        temperature=37.0,
        respiratory_rate=16,
        oxygen_saturation=92,  # Exactly at threshold (not below)
        chest_pain=False
    )
    
    result = assess(obs)
    
    # At 92 should not be RED (only below 92 is critical)
    assert result.category != TriageCategory.RED


# Test 9: No patient ID is OK
def test_no_patient_id():
    """Test that patient_id being None is acceptable."""
    obs = Observations(
        patient_id=None,  # Optional field
        heart_rate=80,
        temperature=37.0,
        respiratory_rate=16,
        oxygen_saturation=98,
        chest_pain=False
    )
    
    result = assess(obs)
    
    # Should work fine even without patient_id
    assert result.category == TriageCategory.GREEN


# Test 10: Parametrized test (test multiple scenarios in one function)
@pytest.mark.parametrize("heart_rate,expected_category", [
    (60, TriageCategory.GREEN),      # Normal
    (100, TriageCategory.GREEN),     # Still normal
    (120, TriageCategory.GREEN),     # At threshold but not over
    (121, TriageCategory.ORANGE),    # Just over threshold
    (150, TriageCategory.ORANGE),    # Definitely elevated
])
def test_heart_rate_thresholds(heart_rate, expected_category):
    """Test various heart rate values to ensure threshold is correct."""
    obs = Observations(
        patient_id="P010",
        heart_rate=heart_rate,
        temperature=37.0,
        respiratory_rate=16,
        oxygen_saturation=98,
        chest_pain=False
    )
    
    result = assess(obs)
    assert result.category == expected_category


if __name__ == "__main__":
    # You can run this file directly: python test_triage.py
    pytest.main([__file__, "-v"])