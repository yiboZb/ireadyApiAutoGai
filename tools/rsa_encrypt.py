import rsa
import base64
from time import time


def rsaEncrypt(msg):
    """
    公钥加密
    :param msg: 要加密的内容
    :type msg: str
    :return: 加密之后的密文
    """
    server_pub_key = """
    -----BEGIN PUBLIC KEY-----
    MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDQENQujkLfZfc5Tu9Z1LprzedE
    O3F7gs+7bzrgPsMl29LX8UoPYvIG8C604CprBQ4FkfnJpnhWu2lvUB0WZyLq6sBr
    tuPorOc42+gLnFfyhJAwdZB6SqWfDg7bW+jNe5Ki1DtU7z8uF6Gx+blEMGo8Dg+S
    kKlZFc8Br7SHtbL2tQIDAQAB
    -----END PUBLIC KEY-----
    """

    # 生成公钥对象
    pub_key_byte = server_pub_key.encode("utf-8")
    # print(pub_key_byte)
    pub_key_obj = rsa.PublicKey.load_pkcs1_openssl_pem(pub_key_byte)

    # 要加密的数据转成字节对象
    content = msg.encode("utf-8")

    # 加密,返回加密文本
    cryto_msg = rsa.encrypt(content,pub_key_obj)
    # base64编码
    cipher_base64 = base64.b64encode(cryto_msg)
    # 转成字符串
    return cipher_base64.decode()


def generator_sign(token):
    # 获取token的前50位
    token_50 = token[:50]
    # 生成时间戳
    timestamp = int(time())
    # print(timestamp)
    # 接拼token前50位和时间戳
    msg = token_50 + str(timestamp)
    # 进行RSA加密，得到加密后的数据
    sign = rsaEncrypt(msg)
    return sign,timestamp





