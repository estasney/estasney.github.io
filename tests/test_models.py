from mypage.models import Resume


def test_resume_model_validates(me_yml_data):
    """Smoke test: Validate that me.yml data can be loaded into Resume model."""
    
    resume = Resume.model_validate(me_yml_data)
    assert resume is not None
    
