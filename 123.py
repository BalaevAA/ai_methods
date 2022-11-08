import time
import jwt

service_account_id = "aje7dm500hat5kh1g8sr"
key_id = "<идентификатор_открытого_ключа>"  # ID ресурса Key, который принадлежит сервисному аккаунту.

with open("<файл_закрытого_ключа>", 'r') as private:
    private_key = private.read()  # Чтение закрытого ключа из файла.

now = int(time.time())
payload = {
    'aud': 'https://iam.api.cloud.yandex.net/iam/v1/tokens',
    'iss': service_account_id,
    'iat': now,
    'exp': now + 360}

# Формирование JWT.
encoded_token = jwt.encode(
    payload,
    private_key,
    algorithm='PS256',
    headers={'kid': key_id})
