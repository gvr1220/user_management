import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from app.services.email_service import EmailService
from app.models.user_model import User
from app.utils.template_manager import TemplateManager
from app.dependencies import get_settings
settings = get_settings()


@pytest.fixture
def email_service():
    # Mock SMTPClient and TemplateManager
    smtp_client_mock = MagicMock()
    template_manager_mock = MagicMock(spec=TemplateManager)

    # Initialize EmailService with the mocks
    email_service = EmailService(template_manager=template_manager_mock)
    email_service.smtp_client = smtp_client_mock
    return email_service


@pytest.mark.asyncio
async def test_send_user_email_invalid_type(email_service):
    user_data = {
        "email": "test@example.com",
        "name": "Test User",
    }
    with pytest.raises(ValueError):
        await email_service.send_user_email(user_data, 'invalid_email_type')


@pytest.mark.asyncio
async def test_send_verification_email(email_service):
    user = User(id=123, first_name="Test", email="test@example.com", verification_token="token123")

    expected_url = f"{settings.server_base_url}verify-email/{user.id}/{user.verification_token}"
    template_content = f"<html>Welcome {user.first_name}! Verify here: {expected_url}</html>"
    email_service.template_manager.render_template.return_value = template_content

    await email_service.send_verification_email(user)

    email_service.smtp_client.send_email.assert_called_once()
    args, kwargs = email_service.smtp_client.send_email.call_args
    subject, html_content, recipient = args

    assert subject == "Verify Your Account"
    assert recipient == user.email
    assert expected_url in html_content


@pytest.mark.asyncio
async def test_template_manager(email_service):
    # Mock data
    user_data = {
        "email": "test@example.com",
        "name": "Test User",
        "verification_url": "http://example.com/verify?token=abc123"
    }

    email_type = 'email_verification'
    template_content = "<html>Test Content</html>"

    # Setup the mock template manager to return specific content
    email_service.template_manager.render_template.return_value = template_content

    await email_service.send_user_email(user_data, email_type)

    email_service.template_manager.render_template.assert_called_once_with(email_type, **user_data)


@pytest.mark.asyncio
async def test_smtp_client_errors(email_service):
    user_data = {
        "email": "test@example.com",
        "name": "Test User",
        "verification_url": "http://example.com/verify?token=abc123"
    }

    # Mock an error in SMTP client
    email_service.smtp_client.send_email.side_effect = Exception("SMTP error")

    with pytest.raises(Exception) as exc_info:
        await email_service.send_user_email(user_data, 'email_verification')

    assert str(exc_info.value) == "SMTP error"
