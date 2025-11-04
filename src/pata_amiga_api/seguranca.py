from pwdlib import PasswordHash

password_hash = PasswordHash.recommended()

def gerar_hash_senha(senha: str) -> str:
    return password_hash.hash(senha)

def verificar_senha(senha_plana: str, hash_salvo: str) -> bool:
    return password_hash.verify(senha_plana, hash_salvo)

