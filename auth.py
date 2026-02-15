import base64

def validate_credentials(auth_header: str):
    if not auth_header or not auth_header.startswith("Basic "):
        return None

    encoded = auth_header.split(" ")[1]
    decoded = base64.b64decode(encoded).decode()
    username, password = decoded.split(":")

    if username == "admin" and password == "password":
        return {"username": username, "role": "admin"}

    return None
