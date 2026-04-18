#!/usr/bin/env python3
"""
Vulnerable Python code with Sensitive Data Exposure examples
FOR SAST TESTING ONLY - DO NOT RUN IN PRODUCTION
"""

import json
import os

from flask import Flask, jsonify, request

app = Flask(__name__)

# VULNERABLE: Hardcoded credentials
DB_PASSWORD = "super_secret_password_123"
API_KEY = "sk-1234567890abcdef1234567890abcdef"
AWS_SECRET = "AKIAIOSFODNN7EXAMPLE"
DATABASE_URL = "postgresql://admin:password123@localhost:5432/mydb"


# VULNERABLE: Hardcoded API keys in code
class PaymentProcessor:
    def __init__(self):
        # CRITICAL VULNERABILITY: Hardcoded API key
        self.stripe_key = "sk_test_1234567890abcdef"
        self.paypal_secret = "EFGHIJKLMNOPQRSTUVWXYZ123456"

    def process_payment(self, amount):
        # CRITICAL VULNERABILITY: Hardcoded credentials in method
        auth_token = "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9"
        return f"Payment processed with key: {self.stripe_key}"


# VULNERABLE: Plain text passwords in configuration
config = {
    "database": {
        "host": "localhost",
        "port": 5432,
        "username": "admin",
        "password": "mypassword123",  # CRITICAL VULNERABILITY: Plain text password
        "database": "myapp",
    },
    "redis": {
        "host": "localhost",
        "port": 6379,
        "password": "redis_password_456",  # CRITICAL VULNERABILITY: Plain text password
    },
}

# VULNERABLE: Hardcoded secrets in environment variables
os.environ["SECRET_KEY"] = "my-super-secret-key-12345"
os.environ["DATABASE_PASSWORD"] = "db_password_789"
os.environ["JWT_SECRET"] = "jwt-secret-key-abcdef"


# VULNERABLE: Sensitive data in logs
@app.route("/login")
def login():
    username = request.form.get("username")
    password = request.form.get("password")

    # CRITICAL VULNERABILITY: Password in log
    print(f"Login attempt for user: {username} with password: {password}")

    if username == "admin" and password == "admin123":
        return "Login successful"
    return "Login failed"


# VULNERABLE: API keys in response headers
@app.route("/api/data")
def get_data():
    # CRITICAL VULNERABILITY: API key in response
    response = jsonify({"data": "sensitive information"})
    response.headers["X-API-Key"] = "sk-1234567890abcdef"
    response.headers["Authorization"] = "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9"
    return response


# VULNERABLE: Database credentials in connection string
def connect_database():
    # CRITICAL VULNERABILITY: Credentials in connection string
    connection_string = "mysql://user:password123@localhost:3306/database"
    return connection_string


# VULNERABLE: Hardcoded encryption keys
ENCRYPTION_KEY = "this-is-a-very-secret-key-for-encryption"
JWT_SECRET = "jwt-secret-key-that-should-not-be-hardcoded"
HMAC_KEY = "hmac-secret-key-for-signing"

# VULNERABLE: Sensitive data in comments
# TODO: Remove these credentials before production
# Username: admin
# Password: admin123
# API Key: sk-1234567890abcdef


# VULNERABLE: Hardcoded tokens
class AuthService:
    def __init__(self):
        # CRITICAL VULNERABILITY: Hardcoded tokens
        self.access_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"
        self.refresh_token = "refresh_token_1234567890abcdef"

    def authenticate(self):
        return self.access_token


# VULNERABLE: Sensitive data in file operations
def save_credentials():
    # CRITICAL VULNERABILITY: Writing credentials to file
    credentials = {
        "username": "admin",
        "password": "admin123",
        "api_key": "sk-1234567890abcdef",
    }

    with open("credentials.json", "w") as f:
        json.dump(credentials, f)


# VULNERABLE: Hardcoded SSH keys
SSH_PRIVATE_KEY = """-----BEGIN RSA PRIVATE KEY-----
MIIEpAIBAAKCAQEA1234567890abcdef...
-----END RSA PRIVATE KEY-----"""

SSH_PUBLIC_KEY = """ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQC..."""


# VULNERABLE: Sensitive data in environment setup
def setup_environment():
    # CRITICAL VULNERABILITY: Setting sensitive environment variables
    os.environ["MYSQL_ROOT_PASSWORD"] = "root_password_123"
    os.environ["REDIS_AUTH"] = "redis_auth_password"
    os.environ["MONGODB_PASSWORD"] = "mongo_password_456"


if __name__ == "__main__":
    app.run(debug=True)
