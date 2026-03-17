from fastapi.testclient import TestClient

from app.main import app

def test_health_endpoint_contains_runtime_info():
    with TestClient(app) as client:
        response = client.get("/")

    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] in {"ok", "degraded"}
    assert "database" in payload
    assert "uptime_seconds" in payload
    assert "version" in payload


def test_full_report_endpoint_returns_consolidated_payload():
    with TestClient(app) as client:
        response = client.post(
            "/analysis/full-report",
            json={
                "profile_skills": ["python", "postgres", "teamwork"],
                "job_description": (
                    "We are looking for a Python developer with PostgreSQL, Docker, "
                    "and teamwork. 3+ years of experience required."
                ),
            },
        )

    assert response.status_code == 200
    payload = response.json()
    assert "job_analysis" in payload
    assert "profile_match" in payload
    assert "learning_path" in payload
    assert payload["profile_match"]["total_job_soft_skills"] >= 1
