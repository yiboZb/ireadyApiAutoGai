import os
import json
import requests
from configparser import ConfigParser
from tools.handle_path import conf_path
from loguru import logger
import logging
from tools.rsa_encrypt import generator_sign

logging.basicConfig(level=logging.DEBUG)


class HandleRequests:

    def __init__(self):
        # 实例化一个session类
        self.s = requests.Session()
        # 设置全局通用的请求头
        self.s.headers = {"Content-Type": "application/json"}
        # 设置全局baseurl
        conf = ConfigParser()
        server_conf = os.path.join(conf_path, "server.ini")
        conf.read(server_conf, encoding="utf-8")
        self.base_url = conf.get("base", "baseurl")

    def send_req(self, method, url, data=None, token=None, **kwargs):
        """
        :param method:
        :param url:
        :param data: 字符串类型。
        :param kwargs:
        :return:
        """
        # 处理header
        self.__header(token)
        # 处理url。
        url = self.__url(url)
        logger.info(f"请求method为：{method}")
        # 处理body.添加sign和timestamp
        # data = self.__body(req_data=data, token=token)
        if method.upper() == "GET":
            if data is not None:
                resp = self.s.get(url, params=str(data).encode("utf-8"), **kwargs)
            else:
                resp = self.s.get(url, **kwargs)
        else:
            resp = self.s.request(method, url, data=data, **kwargs)
        logger.info(f"http响应状态码为：{resp.status_code}")
        logger.info(f"响应body为：\n{resp.text}")
        return resp

    def __header(self, token=None):
        if token:
            # self.s.headers["Authorization"] = token
            self.s.headers.update({"x-access-token": token})
        logger.info(f"请求headers为：{self.s.headers}")

    def __body(self, req_data, token=None):
        if token:
            # 生成sign，和timestamp的值。
            sign, timestamp = generator_sign(token)
            temp = {"sign": sign, "timestamp": timestamp}
            # 在请求体当中，添加上sign，和timestamp字段。
            # 使用json模块把请求数据转成字典
            data_dict = json.loads(req_data)
            # 字典的update，合并2个字典
            data_dict.update(temp)
            # 转换为json格式的字符串。返回
            req_data = json.dumps(data_dict)

        logger.info(f"请求datas为：{req_data}")
        return req_data

    def __url(self, url: str):
        if url.startswith("http://") or url.startswith("https://"):
            pass
        else:
            url = self.base_url + url
        logger.info(f"请求url为：{url}")
        return url


if __name__ == '__main__':
    mr = HandleRequests()
    url = "http://192.168.88.128:20000/api/certification/modelLoginSBH"
    req_data = {
        "userName": "ireadyit",
        "password": "156b8903c4bb6fbf2b627cd65da76082",
        "modelLoginType": 2,
        "loginType": 1
}
    method = "post"
    # resp = requests.post(url, json=req_data)
    resp = mr.send_req(method, url, req_data)
    print(resp.json())
