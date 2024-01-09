# PurpleWig API Documentation

Welcome to the PurpleWig API documentation. This API provides functionalities for user account management, course management, and course registration. Below are the details on how to get started and make API requests.

## Table of Contents
1. [Getting Started](#getting-started)
   - [Installation](#installation)
   - [Authentication](#authentication)
2. [API Requests](#api-requests)
   - [User Account](#user-account)
     - [Create Account](#create-account)
     - [List Users](#list-users)
     - [Send Confirmation Email](#send-confirmation-email)
     - [Verify Account](#verify-account)
     - [Obtain Token](#obtain-token)
     - [Refresh Token](#refresh-token)
   - [Password Reset](#password-reset)
     - [Password Reset Request](#password-reset-request)
     - [Password Reset Confirm](#password-reset-confirm)
   - [Course](#course)
     - [Create Course](#create-course)
     - [List Courses](#list-courses)
     - [Update Course](#update-course)
     - [Delete Course](#delete-course)
     - [Create Course Registration](#create-course-registration)
   - [Service Registration](#service-registration)
     - [Create Service Registration](#create-service-registration)
   - [Models](#models)

## 1. Getting Started <a name="getting-started"></a>

### Installation <a name="installation"></a>

To use the PurpleWig API, you need to have Django and Django REST framework installed. You can install the required packages using:

```bash
pip install django djangorestframework
```
After installation, you can run the Django development server using:

```bash
python manage.py runserver
```
Visit the url http://127.0.0.1:8000 to view the API root.
## 2. Authentication <a name="authentication"></a>
The API uses JWT (JSON Web Tokens) for authentication. To obtain a token, use the /account/token/ endpoint with your credentials.
## API Requests <a name="api-requests"></a>
### User Account <a name="user-account"></a>
- **Create Account**: <a name="create-account"></a> 
`Endpoint: POST /account/create/`

    - **Parameters**:
        - `email`: User's email address
        - `password`: User's password
    - **Response Format:**

        ```json
        {
            "detail": "Account created successfully",
            "user": { "email": "example@example.com", ... }
        }

        ```
- **List Users**: <a name="list-users"></a>
`Endpoint: GET /account/list/`

    - **Response Format:**

        ```json
            {
                "users": 
                [
                    { "email": "user1@example.com", ... },
                    { "email": "user2@example.com", ... },
                ...
                ]
            }
        ```
- **Send Confirmation Email**: <a name="send-confirmation-email"></a>
`Endpoint: POST /account/send-confirmation-email/`

    - **Parameters**:
        - `email`: User's email address
    - **Response Format:**

        ```json
        {
            "detail": "Confirmation email sent"
        }
        ```
- **Verify Account**: <a name="verify-account"></a>
`Endpoint: POST /account/verify/`

    - **Parameters**:
        - `email`: User's email address
        - `otp`: Verification code sent to user's email
    - **Response Format:**

        ```json
        {
            "detail": "Account verified successfully"
        }
        ```
- **Obtain Token**: <a name="obtain-token"></a>
`Endpoint: POST /account/token/`

    - **Parameters**:
        - `email`: User's email address
        - `password`: User's password
    - **Response Format:**

        ```json
        {
            "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
            "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
        }
        ```
- **Refresh Token**: <a name="refresh-token"></a>
`Endpoint: POST /account/token/refresh/`

    - **Parameters**:
        - `refresh`: Refresh token
    - **Response Format:**

        ```json
        {
            "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
        }
        ```
### Password Reset <a name="password-reset"></a>
- **Password Reset Request**: <a name="password-reset-request"></a>
`Endpoint: POST /account/password-reset/`

    - **Parameters**:
        - `email`: User's email address
    - **Response Format:**

        ```json
        {
            "detail": "Password reset email sent"
        }
        ```
- **Password Reset Confirm**: <a name="password-reset-confirm"></a>
`Endpoint: POST /account/password-reset/confirm/`

    - **Parameters**:
        - `email`: User's email address
        - `otp`: Verification code sent to user's email
        - `password`: New password
    - **Response Format:**

        ```json
        {
            "detail": "Password reset successful"
        }
        ```
### Course <a name="course"></a>
- **Create Course**: <a name="create-course"></a>
`Endpoint: POST /course/create/`

    - **Parameters**:
        - `name`: Course name
        - `description`: Course description
    - **Response Format:**

        ```json
        {
            "courses": [
                { "title": "Course1", ... },
                { "title": "Course2", ... },
                ...
            ]
        }
        ```
- **List Courses**: <a name="list-courses"></a>
`Endpoint: GET /course/list/`

    - **Response Format:**

        ```json
        {
            "courses": [
                { "title": "Course1", ... },
                { "title": "Course2", ... },
                ...
            ]
        }
        ```
- **Update Course**: <a name="update-course"></a>
`Endpoint: PUT /course/update/`

    - **Parameters**:
        - `name`: Course name
        - `description`: Course description
    - **Response Format:**

        ```json
        {
            "detail": "Course updated successfully"
        }
        ```
- **Delete Course**: <a name="delete-course"></a>
`Endpoint: DELETE /course/delete/<int:pk>/`

    - **Response Format**:
        ```json
        {
            "detail": "Course deleted successfully"
        }
        ```
- **Create Course Registration**: <a name="create-course-registration"></a>
- `Endpoint: POST /course/registration/create/<int:pk>/`

    - **Parameters**:
        - `email`: User's email address
        - `full_name:` User's full name
        - `phone_number`: User's phone number
        - `gender`: User's gender
    - **Response Format:**

        ```json
            {
                "detail": "Course registration successful",
                "course_registration": {
                     "email": "example@example.com", ... 
                }
            }
        ```
### Service Registration <a name="service-registration"></a>
- **Create Service Registration**: <a name="create-service-registration"></a>
- `Endpoint: POST /service/register/create/<int:id>/`
    - **Parameters**:
        - `email`: User's email address
        - `full_name:` User's full name
        - `phone_number`: User's phone number
        - `gender`: User's gender
        - **Response Format:**

        ```json
            {
                "detail": "Service registration successful",
                "service_registration": {
                     "email": "example@example.com", ... 
                }
            }

        ```
