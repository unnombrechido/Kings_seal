# -----------------------------
# QR Verification (Scanner Side)
# -----------------------------
def verify_sealed_qr(qr_content: str) -> dict:
    if not qr_content.startswith("seal:"):
        return {"trusted": False, "reason": "No seal prefix"}
    
    try:
        parts = qr_content.split("|", 2)
        if len(parts) != 3:
            return {"trusted": False, "reason": "Invalid format"}
        
        seal_part, tag_part, payload = parts
        issuer_id = seal_part.split(":", 1)[1]
        provided_tag = tag_part.split(":", 1)[1]
        
        if issuer_id not in public_registry_info:
            return {"trusted": False, "reason": "Unknown issuer"}
        
        # Recompute expected tag (in real app, fetch secret or use pre-shared mapping)
        # For demo, we simulate having access to the secret (in practice, scanner uses a verification endpoint or bundled keys)
        secret = registry[issuer_id]["secret"]
        data_to_sign = payload.encode('utf-8')
        mac = hmac.new(secret, data_to_sign, hashlib.sha256)
        expected_tag = mac.hexdigest()[:16]
        
        if hmac.compare_digest(expected_tag, provided_tag):
            return {
                "trusted": True,
                "issuer_name": public_registry_info[issuer_id],
                "payload": payload
            }
        else:
            return {"trusted": False, "reason": "Invalid tag (tampered)"}
    
    except Exception as e:
        return {"trusted": False, "reason": f"Parse error: {str(e)}"}
