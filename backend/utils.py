import base64
import hashlib
import hmac
from replacement_twitter.settings import SECRET_KEY

def encrypt(data):
    message = base64.b64encode(bytes(data, 'utf-8'));
    hash = hmac.new(SECRET_KEY, message, hashlib.sha256);
    hash =  base64.b64encode(hash.digest());
    hash = hash.decode("utf-8");
    return hash
