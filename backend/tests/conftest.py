import os

# Keep test tokens representative of the minimum HMAC key length recommended by JWT.
os.environ.setdefault("SPORTLOGIC_SECRET_KEY", "test-secret-key-with-at-least-32-bytes")
