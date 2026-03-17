from app.services.matcher import match_profile


def test_match_profile_includes_soft_skills_in_score():
    job_description = (
        "We need Python, Docker and teamwork. "
        "At least 2 years of experience required."
    )
    profile_skills = ["python", "teamwork"]

    result = match_profile(profile_skills, job_description)

    assert result["matching_skills"] == ["python"]
    assert result["missing_skills"] == ["docker"]
    assert result["matching_soft_skills"] == ["teamwork"]
    assert result["missing_soft_skills"] == []
    assert result["total_job_skills"] == 2
    assert result["total_job_soft_skills"] == 1
    assert result["compatibility_percentage"] == 66.7
