import os
OPEN_END_POINTS = os.getenv(
    "OPEN_END_POINTS", ["/auth/token", "/auth/register", "/docs"])


JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "12345_54321")

JWT_ALGORITHM = "HS256"
JWT_REFRESH_SECRET_KEY = os.getenv(
    "JWT_REFRESH_SECRET_KEY", "Refresh12345_54321Refresh")
