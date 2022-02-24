from jsonpath import jsonpath
from .handle_data import Data

from loguru import logger

def extract_data_from_response_dict(resp_dict,exprs):
    """
    从响应结果当中，提取值并设置为全局变量类Data的属性。
    :param resp_dict: 接口响应数据，字典类型。
    :param exprs: excel当中，extract列的值。字符串类型
    :return:
    """
    # 把表达式转换成字典
    exprs_dict = eval(exprs)

    for key, value in exprs_dict.items():
        logger.info("提取的变量名是：{}，提取的jsonpath表达式是：{}".format(key, value))
        # 根据jsonpath的表达式，提取到值。提出出来后是个列表
        actual_data = jsonpath(resp_dict, value)
        logger.info("jsonpath提取之后的值为:{}".format(actual_data))
        # 如果提取到了值
        if actual_data:
            # 设置为数据类(全局变量)的属性。统一转换成字符串。替换的时候只能是字符串替换。
            setattr(Data, key, str(actual_data[0]))
            logger.info("提取的变量名是：{}，提取到的值是：{},并设置为Data类实例化对象的属性和值。".format(key, str(actual_data[0])))
        else:
            logger.warning("没有提取到数据，提取结果为{}".format(actual_data))