from environment.incidents import Incident


def test_incident_creation():
    incident = Incident(
        incident_id="I1",
        position=(10, 15),
        severity=5,
        resource_type="ambulance"
    )

    assert incident.incident_id == "I1"
    assert incident.position == (10, 15)
    assert incident.severity == 5
    assert incident.resource_type == "ambulance"
    assert incident.completed is False


def test_incident_completion():
    incident = Incident(
        incident_id="I2",
        position=(5, 5),
        severity=3,
        resource_type="response_unit"
    )

    incident.complete()

    assert incident.completed is True