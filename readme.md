# User Management System

Welcome to my User Management System repository! This project was an essential part of my coursework on software development for IS 219. It focuses on project management, quality assurance, and deployment. Below, you'll find information on QA issues, testing processes, the feature implementation, and DockerHub deployment.

## QA Issues and Testing

Throughout the project, I addressed several quality assurance issues:

- [Update production.yml and Dockerfile](https://github.com/gvr1220/user_management/issues/1)
- [Verification email contains incorrect link structure](https://github.com/gvr1220/user_management/issues/3)
-  [First user (Admin) receives invalid verification token link](https://github.com/gvr1220/user_management/issues/5)
- [Case-insensitive duplicate email handling in registration](https://github.com/gvr1220/user_management/issues/7)
- [OAuth2 authentication error](https://github.com/gvr1220/user_management/issues/9)
- [User profile not reflecting changes in is_professional field](https://github.com/gvr1220/user_management/issues/11)
- [Role change unauthorized during User Update](https://github.com/gvr1220/user_management/issues/13)
- [Email verification changes Admin role to Authenticated](https://github.com/gvr1220/user_management/issues/15)

The testing process played a critical role in ensuring the project's success. Here are the links to the new tests I created:

- [test_create_user_with_duplicate_emails](https://github.com/gvr1220/user_management/commit/b47fbed840f48a15cc8a8e84326469f84337b872#diff-e3f3da0661632e0add5f28cb40266e4bfbd6e0c1a23cdb5f5e8813af69cf1d5c)
- [test_login_with_default_admin_credentials](https://github.com/gvr1220/user_management/commit/7f0f337d1f4efd64ffb6055521c58ebe760a6fe0#diff-df7dfcf3734befe5032b230c4b76211088909172814f84139ffd7acc55265962)
- [test_login_with_incorrect_admin_password](https://github.com/gvr1220/user_management/commit/7f0f337d1f4efd64ffb6055521c58ebe760a6fe0)
- [test_login_with_incorrect_admin_username](https://github.com/gvr1220/user_management/commit/7f0f337d1f4efd64ffb6055521c58ebe760a6fe0)
- [test_send_user_email_invalid_type](https://github.com/gvr1220/user_management/commit/2fde48cea3189ed55c7c554c7d97941425c6b321#diff-f6c4849c9543cda32313695d741656026ce97f6b0139270a273f247961220435)
- [test_send_verification_email](https://github.com/gvr1220/user_management/commit/2fde48cea3189ed55c7c554c7d97941425c6b321#diff-f6c4849c9543cda32313695d741656026ce97f6b0139270a273f247961220435)
- [test_template_manager](https://github.com/gvr1220/user_management/commit/2fde48cea3189ed55c7c554c7d97941425c6b321#diff-f6c4849c9543cda32313695d741656026ce97f6b0139270a273f247961220435)
- [test_smtp_client_errors](https://github.com/gvr1220/user_management/commit/2fde48cea3189ed55c7c554c7d97941425c6b321#diff-f6c4849c9543cda32313695d741656026ce97f6b0139270a273f247961220435)
- [test_search_users_single_field](https://github.com/gvr1220/user_management/commit/2fde48cea3189ed55c7c554c7d97941425c6b321#diff-dbd4401236d3bb4a816be4b002737bea8a40549c90a9a4747d4b62418eb663ed)
- [test_search_users_multiple_fields_error](https://github.com/gvr1220/user_management/commit/2fde48cea3189ed55c7c554c7d97941425c6b321#diff-dbd4401236d3bb4a816be4b002737bea8a40549c90a9a4747d4b62418eb663ed)
- [test_search_users_no results](https://github.com/gvr1220/user_management/commit/2fde48cea3189ed55c7c554c7d97941425c6b321#diff-dbd4401236d3bb4a816be4b002737bea8a40549c90a9a4747d4b62418eb663ed)
- [test_search_users_invalid_input_format](https://github.com/gvr1220/user_management/commit/2fde48cea3189ed55c7c554c7d97941425c6b321#diff-dbd4401236d3bb4a816be4b002737bea8a40549c90a9a4747d4b62418eb663ed)
- [test_search_and_filter_users](https://github.com/gvr1220/user_management/commit/2fde48cea3189ed55c7c554c7d97941425c6b321#diff-e3f3da0661632e0add5f28cb40266e4bfbd6e0c1a23cdb5f5e8813af69cf1d5c)

## Feature Implementation

The new feature I implemented is the search and filter functionality, which allows users to efficiently search for other users based on criteria such as username, email, role, professional status, account locked status, and registration dates.

You can find the feature branch [here](https://github.com/gvr1220/user_management/tree/feature/search-filter).

The feature is accessible via the `/users/search` endpoint, where users can specify search criteria through query parameters. The function validates input and executes queries to filter users accordingly, with results being paginated and returned as a response.

![Screenshot of the feature](https://github.com/gvr1220/user_management/assets/110260661/2ca38bcc-88db-45d7-a354-aa924b9e7cb7)


## DockerHub Deployment

Deploying the project to DockerHub was a smooth process, thanks to the knowledge I gained in the course about Docker containerization and deployment. You can access the DockerHub repository [here](https://hub.docker.com/repository/docker/gv225/user_management/general).

![Alt text](https://private-user-images.githubusercontent.com/110260661/328701415-fc4b91fa-4f5e-41f2-b9f8-a7690cb05e2d.png?jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3MTUxMjIyMTEsIm5iZiI6MTcxNTEyMTkxMSwicGF0aCI6Ii8xMTAyNjA2NjEvMzI4NzAxNDE1LWZjNGI5MWZhLTRmNWUtNDFmMi1iOWY4LWE3NjkwY2IwNWUyZC5wbmc_WC1BbXotQWxnb3JpdGhtPUFXUzQtSE1BQy1TSEEyNTYmWC1BbXotQ3JlZGVudGlhbD1BS0lBVkNPRFlMU0E1M1BRSzRaQSUyRjIwMjQwNTA3JTJGdXMtZWFzdC0xJTJGczMlMkZhd3M0X3JlcXVlc3QmWC1BbXotRGF0ZT0yMDI0MDUwN1QyMjQ1MTFaJlgtQW16LUV4cGlyZXM9MzAwJlgtQW16LVNpZ25hdHVyZT00ZTIzMWNmYzM2NWU4NmQ4ZGI4YmY4ODdhN2M0NDk1ZmU1ZjhlMWQwMjQ3ZGU1N2EzZWUwM2U3N2RiMmE5NWJmJlgtQW16LVNpZ25lZEhlYWRlcnM9aG9zdCZhY3Rvcl9pZD0wJmtleV9pZD0wJnJlcG9faWQ9MCJ9.xegHiz8dd0ixlFxGIKrjaeYbD6MIHMxMDbYOSU89k3Q)

