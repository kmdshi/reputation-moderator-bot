import hashlib


async def encrypt_name(name_id) -> str:
    number_str = str(name_id)
    hashed_value = hashlib.sha256(number_str.encode('utf-8')).hexdigest()
    
    return hashed_value