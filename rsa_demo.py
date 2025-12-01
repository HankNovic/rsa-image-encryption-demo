from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes


# =========================
# 1. 生成 RSA 密钥对
# =========================
def generate_rsa_key_pair(key_size=2048):
    """
    生成一对 RSA 公钥和私钥
    :param key_size: 密钥长度，常用 2048 或 3072
    :return: (private_key, public_key)
    """
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=key_size,
    )
    public_key = private_key.public_key()
    return private_key, public_key


# =========================
# 2. 保存密钥到 PEM 文件
# =========================
def save_private_key_to_pem(private_key, filename, password: bytes | None = None):
    """
    将私钥保存为 PEM 文件
    :param private_key: RSA 私钥对象
    :param filename: 文件名，例如 'private_key.pem'
    :param password: 保护私钥的密码（bytes 类型），如果为 None 则不加密
    """
    if password is not None:
        encryption_algo = serialization.BestAvailableEncryption(password)
    else:
        encryption_algo = serialization.NoEncryption()

    pem_data = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=encryption_algo,
    )

    with open(filename, "wb") as f:
        f.write(pem_data)


def save_public_key_to_pem(public_key, filename):
    """
    将公钥保存为 PEM 文件
    :param public_key: RSA 公钥对象
    :param filename: 文件名，例如 'public_key.pem'
    """
    pem_data = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )

    with open(filename, "wb") as f:
        f.write(pem_data)


# =========================
# 3. 从 PEM 文件加载密钥
# =========================
def load_private_key_from_pem(filename, password: bytes | None = None):
    with open(filename, "rb") as f:
        pem_data = f.read()

    private_key = serialization.load_pem_private_key(
        pem_data,
        password=password,
    )
    return private_key


def load_public_key_from_pem(filename):
    with open(filename, "rb") as f:
        pem_data = f.read()

    public_key = serialization.load_pem_public_key(pem_data)
    return public_key


# =========================
# 4. 使用公钥加密 & 私钥解密
# =========================
def rsa_encrypt(public_key, plaintext: bytes) -> bytes:
    """
    使用公钥加密
    :param public_key: RSA 公钥对象
    :param plaintext: 明文（bytes）
    :return: 密文（bytes）
    """
    ciphertext = public_key.encrypt(
        plaintext,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None,
        ),
    )
    return ciphertext


def rsa_decrypt(private_key, ciphertext: bytes) -> bytes:
    """
    使用私钥解密
    :param private_key: RSA 私钥对象
    :param ciphertext: 密文（bytes）
    :return: 明文（bytes）
    """
    plaintext = private_key.decrypt(
        ciphertext,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None,
        ),
    )
    return plaintext


# =========================
# 5. 主流程示例（可直接运行）
# =========================
def main():
    # 1. 生成密钥对
    private_key, public_key = generate_rsa_key_pair(key_size=2048)
    print("RSA 密钥对生成成功！")

    # 2. 保存密钥到文件（示例：私钥使用密码保护）
    save_private_key_to_pem(private_key, "private_key.pem", password=b"123456")
    save_public_key_to_pem(public_key, "public_key.pem")
    print("公钥和私钥已保存到 PEM 文件。")

    # 3. 从文件加载密钥（模拟在其它程序中使用）
    loaded_private_key = load_private_key_from_pem("private_key.pem", password=b"123456")
    loaded_public_key = load_public_key_from_pem("public_key.pem")
    print("从 PEM 文件加载密钥成功。")

    # 4. 测试加密解密
    message = "Hello, RSA! 这是一次加密与解密的测试。"
    print("原始明文：", message)

    ciphertext = rsa_encrypt(loaded_public_key, message.encode("utf-8"))
    print("加密后密文（十六进制展示）：", ciphertext.hex())

    decrypted = rsa_decrypt(loaded_private_key, ciphertext)
    print("解密后明文：", decrypted.decode("utf-8"))


if __name__ == "__main__":
    main()
