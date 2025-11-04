from fastapi.security import OAuth2PasswordBearer
from pwdlib import PasswordHash
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

password_hash = PasswordHash.recommended()

def gerar_hash_senha(senha: str) -> str:
    return password_hash.hash(senha)

def verificar_senha(senha_plana: str, hash_salvo: str) -> bool:
    return password_hash.verify(senha_plana, hash_salvo)


# def authenticate_user(fake_db, username: str, password: str):
#     user = get_user(fake_db, username)
#     if not user:
#         return False
#     if not verify_password(password, user.hashed_password):
#         return False
#     return user