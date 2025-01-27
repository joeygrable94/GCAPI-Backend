import base64
import json


def get_malformed_token(token: str) -> str:
    payload_encoded = token.split(".")[1]
    payload_str = base64.b64decode(f"{payload_encoded}==").decode()
    payload = json.loads(payload_str)

    payload["sub"] = "evil"
    bad_payload_str = json.dumps(payload, separators=(",", ":"))
    bad_payload_encoded = (
        base64.b64encode(bad_payload_str.encode()).decode().replace("=", "")
    )

    return token.replace(payload_encoded, bad_payload_encoded)


def get_missing_kid_token(token: str) -> str:
    header_encoded = token.split(".")[0]
    header_str = base64.b64decode(f"{header_encoded}==").decode()
    header = json.loads(header_str)

    header.pop("kid")
    bad_header_str = json.dumps(header, separators=(",", ":"))
    bad_header_encoded = (
        base64.b64encode(bad_header_str.encode()).decode().replace("=", "")
    )

    return token.replace(header_encoded, bad_header_encoded)


def get_invalid_token(token: str) -> str:
    header = token.split(".")[0]
    return token.replace(header, header[:-3])
