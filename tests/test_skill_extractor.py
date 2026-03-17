from app.services.skill_extractor import extract_skills


def test_extracts_aliases_and_experience_max_value():
    text = (
        "Buscamos backend developer con 3+ years experience in Python and FastAPI, "
        "plus at least 5 years of experience with PostgreSQL and Docker."
    )

    result = extract_skills(text)

    assert "python" in result.tech_skills
    assert "fastapi" in result.tech_skills
    assert "postgresql" in result.tech_skills
    assert "docker" in result.tech_skills
    assert result.experience_years == 5


def test_extracts_symbol_based_skills():
    text = (
        "We need engineers with C++, C#, .NET, CI/CD pipelines and ASP.NET experience."
    )

    result = extract_skills(text)

    assert "c++" in result.tech_skills
    assert "c#" in result.tech_skills
    assert ".net" in result.tech_skills
    assert "ci/cd" in result.tech_skills
    assert "asp.net" in result.tech_skills
