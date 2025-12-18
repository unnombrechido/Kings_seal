import hmac
import hashlib
import base64
import qrcode
from io import BytesIO

# -----------------------------
# Registry Setup (Server Side)
# -----------------------------
# In a real system, this would be a secure database.
# Verified issuers apply and get a secret key.
registry = {
    "starbucks-official": {
        "secret": b"super-secret-key-starbucks-2025",  # Random, high-entropy bytes
        "display_name": "Starbucks"
    },
    "mcdonalds-official": {
        "secret": b"another-very-secret-key-mcd-2025",
        "display_name": "McDonald's"
    },
    # Add more verified issuers here...
}

# Public mapping for scanners (could be bundled in app or fetched once)
public_registry_info = {
    "starbucks-official": "Starbucks",
    "mcdonalds-official": "McDonald's"
}

# -----------------------------
# QR Generation (Issuer Tool)
# -----------------------------
def generate_sealed_qr(issuer_id: str, payload: str) -> BytesIO:
    if issuer_id not in registry:
        raise ValueError("Unknown issuer")
    
    secret = registry[issuer_id]["secret"]
    
    # Normalize data for signing
    data_to_sign = payload.encode('utf-8')
    
    # Compute HMAC-SHA256
    mac = hmac.new(secret, data_to_sign, hashlib.sha256)
    tag = mac.hexdigest()[:16]  # Use first 16 hex chars (~64 bits) for compactness
    
    # Assemble QR content
    qr_content = f"seal:{issuer_id}|tag:{tag}|{payload}"
    
    # Generate QR code
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(qr_content)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    buf = BytesIO()
    img.save(buf, format='PNG')
    buf.seek(0)
    return buf

"""
# Example usage
payload = "https://bit.ly/starbucks-menu-dec2025"  # shortened URL
issuer = "starbucks-official"
sealed_qr_img = generate_sealed_qr(issuer, payload)
# sealed_qr_img now contains the PNG bytes — save or display it
"""

