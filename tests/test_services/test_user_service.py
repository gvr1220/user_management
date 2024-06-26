from builtins import range
import pytest
from sqlalchemy import select
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import uuid4
from datetime import datetime, timedelta
from app.dependencies import get_settings
from app.models.user_model import User, UserRole
from app.services.user_service import UserService
from app.utils.nickname_gen import generate_nickname
from app.utils.security import generate_verification_token, hash_password
from app.dependencies import get_db

pytestmark = pytest.mark.asyncio

# Test creating a user with valid data
async def test_create_user_with_valid_data(db_session, email_service):
    user_data = {
        "nickname": generate_nickname(),
        "email": "valid_user@example.com",
        "password": "ValidPassword123!",
        "role": UserRole.ADMIN.name
    }
    user = await UserService.create(db_session, user_data, email_service)
    assert user is not None
    assert user.email == user_data["email"]
    assert user.id is not None

# Test creating a user with invalid data
async def test_create_user_with_invalid_data(db_session, email_service):
    user_data = {
        "nickname": "",  # Invalid nickname
        "email": "invalidemail",  # Invalid email
        "password": "short",  # Invalid password
    }
    user = await UserService.create(db_session, user_data, email_service)
    assert user is None

# Test fetching a user by ID when the user exists
async def test_get_by_id_user_exists(db_session, user):
    retrieved_user = await UserService.get_by_id(db_session, user.id)
    assert retrieved_user.id == user.id

# Test fetching a user by ID when the user does not exist
async def test_get_by_id_user_does_not_exist(db_session):
    non_existent_user_id = "non-existent-id"
    retrieved_user = await UserService.get_by_id(db_session, non_existent_user_id)
    assert retrieved_user is None

# Test fetching a user by nickname when the user exists
async def test_get_by_nickname_user_exists(db_session, user):
    retrieved_user = await UserService.get_by_nickname(db_session, user.nickname)
    assert retrieved_user.nickname == user.nickname

# Test fetching a user by nickname when the user does not exist
async def test_get_by_nickname_user_does_not_exist(db_session):
    retrieved_user = await UserService.get_by_nickname(db_session, "non_existent_nickname")
    assert retrieved_user is None

# Test fetching a user by email when the user exists
async def test_get_by_email_user_exists(db_session, user):
    retrieved_user = await UserService.get_by_email(db_session, user.email)
    assert retrieved_user.email == user.email

# Test fetching a user by email when the user does not exist
async def test_get_by_email_user_does_not_exist(db_session):
    retrieved_user = await UserService.get_by_email(db_session, "non_existent_email@example.com")
    assert retrieved_user is None

# Test updating a user with valid data
async def test_update_user_valid_data(db_session, user):
    new_email = "updated_email@example.com"
    updated_user = await UserService.update(db_session, user.id, {"email": new_email})
    assert updated_user is not None
    assert updated_user.email == new_email

# Test updating a user with invalid data
async def test_update_user_invalid_data(db_session, user):
    updated_user = await UserService.update(db_session, user.id, {"email": "invalidemail"})
    assert updated_user is None

# Test deleting a user who exists
async def test_delete_user_exists(db_session, user):
    deletion_success = await UserService.delete(db_session, user.id)
    assert deletion_success is True

# Test attempting to delete a user who does not exist
async def test_delete_user_does_not_exist(db_session):
    non_existent_user_id = "non-existent-id"
    deletion_success = await UserService.delete(db_session, non_existent_user_id)
    assert deletion_success is False

# Test listing users with pagination
async def test_list_users_with_pagination(db_session, users_with_same_role_50_users):
    users_page_1 = await UserService.list_users(db_session, skip=0, limit=10)
    users_page_2 = await UserService.list_users(db_session, skip=10, limit=10)
    assert len(users_page_1) == 10
    assert len(users_page_2) == 10
    assert users_page_1[0].id != users_page_2[0].id

# Test registering a user with valid data
async def test_register_user_with_valid_data(db_session, email_service):
    user_data = {
        "nickname": generate_nickname(),
        "email": "register_valid_user@example.com",
        "password": "RegisterValid123!",
        "role": UserRole.ADMIN
    }
    user = await UserService.register_user(db_session, user_data, email_service)
    assert user is not None
    assert user.email == user_data["email"]

# Test attempting to register a user with invalid data
async def test_register_user_with_invalid_data(db_session, email_service):
    user_data = {
        "email": "registerinvalidemail",  # Invalid email
        "password": "short",  # Invalid password
    }
    user = await UserService.register_user(db_session, user_data, email_service)
    assert user is None

# Test successful user login
async def test_login_user_successful(db_session, verified_user):
    user_data = {
        "email": verified_user.email,
        "password": "MySuperPassword$1234",
    }
    logged_in_user = await UserService.login_user(db_session, user_data["email"], user_data["password"])
    assert logged_in_user is not None

# Test user login with incorrect email
async def test_login_user_incorrect_email(db_session):
    user = await UserService.login_user(db_session, "nonexistentuser@noway.com", "Password123!")
    assert user is None

# Test user login with incorrect password
async def test_login_user_incorrect_password(db_session, user):
    user = await UserService.login_user(db_session, user.email, "IncorrectPassword!")
    assert user is None

# Test account lock after maximum failed login attempts
async def test_account_lock_after_failed_logins(db_session, verified_user):
    max_login_attempts = get_settings().max_login_attempts
    for _ in range(max_login_attempts):
        await UserService.login_user(db_session, verified_user.email, "wrongpassword")
    
    is_locked = await UserService.is_account_locked(db_session, verified_user.email)
    assert is_locked, "The account should be locked after the maximum number of failed login attempts."

# Test resetting a user's password
async def test_reset_password(db_session, user):
    new_password = "NewPassword123!"
    reset_success = await UserService.reset_password(db_session, user.id, new_password)
    assert reset_success is True

# Test verifying a user's email with valid and invalid tokens
async def test_verify_email_with_token(db_session, user):
    token = generate_verification_token()
    user.verification_token = token
    await db_session.commit()
    result = await UserService.verify_email_with_token(db_session, user.id, token)
    assert result is True, "User's email should be verified with a valid token"
    invalid_token = "invalid_token_example"
    result = await UserService.verify_email_with_token(db_session, user.id, invalid_token)
    assert result is False, "User's email should not be verified with an invalid token"
    refreshed_user = await UserService.get_by_id(db_session, user.id)
    assert refreshed_user.verification_token is None, "The token should be cleared after verification"

# Test unlocking a user's account
async def test_unlock_user_account(db_session, locked_user):
    unlocked = await UserService.unlock_user_account(db_session, locked_user.id)
    assert unlocked, "The account should be unlocked"
    refreshed_user = await UserService.get_by_id(db_session, locked_user.id)
    assert not refreshed_user.is_locked, "The user should no longer be locked"

# Test creating a user with duplicate emails, both exact and case-insensitive
async def test_create_user_with_duplicate_emails(db_session, email_service):
    original_user_data = {
        "nickname": generate_nickname(),
        "email": "User@Example.com",  # This email will be used in the next tests
        "password": "ValidPassword123!",
        "role": UserRole.ADMIN.name
    }
    original_user = await UserService.create(db_session, original_user_data, email_service)

    # Ensure the original user is created successfully
    assert original_user is not None

    # Test creating another user with the exact same email
    exact_duplicate_user_data = {
        "nickname": generate_nickname(),
        "email": original_user.email,  # Using the same exact email
        "password": "AnotherValidPassword123!",
        "role": UserRole.ANONYMOUS.name
    }
    exact_duplicate_user = await UserService.create(db_session, exact_duplicate_user_data, email_service)

    # Ensure creation of the duplicate user with exact email fails
    assert exact_duplicate_user is None

    # Test creating another user with the same email but in different case
    case_insensitive_duplicate_user_data = {
        "nickname": generate_nickname(),
        "email": original_user.email.lower(),  # Convert original email to lowercase
        "password": "AnotherValidPassword123!",
        "role": UserRole.ANONYMOUS.name
    }
    case_insensitive_duplicate_user = await UserService.create(db_session, case_insensitive_duplicate_user_data, email_service)

    # Ensure creation of the duplicate user with case-insensitive email fails
    assert case_insensitive_duplicate_user is None

# Test search and filtering functionality for users based on different criteria
async def test_search_and_filter_users(db_session: AsyncSession):
    test_users = [
        User(
            nickname="testuser1",
            email="testuser1@example.com",
            hashed_password=hash_password("Password123!"),
            role=UserRole.AUTHENTICATED,
            is_professional=False,
            is_locked=False,
            created_at=datetime.now() - timedelta(days=10)
        ),
        User(
            nickname="testuser2",
            email="testuser2@example.com",
            hashed_password=hash_password("Password123!"),
            role=UserRole.MANAGER,
            is_professional=True,
            is_locked=True,
            created_at=datetime.now() - timedelta(days=5)
        ),
        User(
            nickname="testuser3",
            email="testuser3@example.com",
            hashed_password=hash_password("Password123!"),
            role=UserRole.ADMIN,
            is_professional=True,
            is_locked=False,
            created_at=datetime.now()
        ),
    ]

    # Add the test users to the database session
    db_session.add_all(test_users)
    await db_session.commit()

    # Test search by username (case-insensitive)
    users, total_users = await UserService.search_and_filter_users(
        db_session,
        username="TestUser1"
    )
    assert total_users == 1
    assert users[0].nickname == "testuser1"

    # Test search by email (case-insensitive)
    users, total_users = await UserService.search_and_filter_users(
        db_session,
        email="testuser2@example.com"
    )
    assert total_users == 1
    assert users[0].email == "testuser2@example.com"

    # Test search by role
    users, total_users = await UserService.search_and_filter_users(
        db_session,
        role=UserRole.MANAGER
    )
    assert total_users == 1
    assert users[0].role == UserRole.MANAGER

    # Test search by professional status
    users, total_users = await UserService.search_and_filter_users(
        db_session,
        is_professional=True
    )
    assert total_users == 2  # testuser2 and testuser3 are professionals

    # Test search by locked account status
    users, total_users = await UserService.search_and_filter_users(
        db_session,
        is_locked=True
    )
    assert total_users == 1
    assert users[0].is_locked is True

    # Test search by registration date range
    start_date = datetime.now() - timedelta(days=7)
    end_date = datetime.now()
    users, total_users = await UserService.search_and_filter_users(
        db_session,
        registration_start=start_date,
        registration_end=end_date
    )
    assert total_users == 2  # testuser2 and testuser3 were created within the date range

    # Clean up the test users from the database
    for user in test_users:
        await db_session.delete(user)
    await db_session.commit()