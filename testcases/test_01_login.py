import os
import json
import unittest
import requests

from ddt import data, ddt, file_data
from tools.handle_excel import HandleExcel
from tools.handle_path import testdatas_dir
from tools.handle_requests import HandleRequests
from loguru import logger
from tools.handle_assert import assert_resp
from tools.handle_data import Data
from tools.handle_extract import extract_data_from_response_dict
# from tools.handle_assert_db import assert_db


excel_path = os.path.join(testdatas_dir, "cases.xlsx")
he = HandleExcel(excel_path, "登录")
datas = he.read_all_rows_data()

@ddt
class TestLogin(unittest.TestCase):

    name = "登录"

    @classmethod
    def setUpClass(cls) -> None:
        logger.info(f"\n============= {cls.name} 接口测试开始！ ==============")

    @classmethod
    def tearDownClass(cls) -> None:
        logger.info(f"\n============= {cls.name} 接口测试结束！ ==============")

    @data(*datas)
    def test_login(self, case):
        '''漂亮的登录测试'''
        logger.info(f"\n********* {case.get('title')} 用例 ********")

        # 发起请求 - 要加上token值作为鉴权
        hr = HandleRequests()
        if hasattr(Data,"token"):
            resp = hr.send_req(case["method"], case["url"], case['req_data'], token=getattr(Data, "token"))

        else:
            resp = hr.send_req(case["method"], case["url"], case['req_data'])
        res_dict = resp.json()
        print(f"请求结果为{res_dict}")

        # extract不为None时，从响应结果当中提取数据，并设置为全局变量
        if case["extract"]:
            extract_data_from_response_dict(res_dict, case["extract"])

        # 断言
        if case["asert_expr"]:
            self.assertTrue(assert_resp(res_dict, case["asert_expr"]))


if __name__ == '__main__':
    print(datas)