from cryptography.fernet import Fernet
from os import getenv

eqSSgmnOLKv2YUUAt1eqSSgmn = getenv("SECRET_KEY")

FERNET = Fernet(bytes([i^0x1 for i in eqSSgmnOLKv2YUUAt1eqSSgmn.encode()]).decode())

async def decrypt_password(password: str) -> str:
    stored_dec_password = FERNET.decrypt(password).decode()
    return stored_dec_password
    
async def ecrypt_password(password: str) -> str:
    new_enc_password = FERNET.encrypt(password.encode()).decode()
    return new_enc_password