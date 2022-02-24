from jsonpath import jsonpath
from loguru import logger


def assert_resp(resp, assert_expr):
    """
    :param resp: 字典类型
    :param assert_expr:
        断言表达式，字符串类型。是列表形式的字符串。列表当中的每个成员，是字典格式。
        [
            {"expr":"$..code","expected":0,"compare_type":"=="},
            {"expr":"$..msg","expected":"OK","compare_type":"=="},
            {"expr":"$..reg_name","expected":"小明","compare_type":"=="}
        ]
    :return: True或者False。如果为True,表示所有的断言均成功。如果为False，表示有断言失败。
    """
    if assert_expr and resp:
        assert_expr_list = eval(assert_expr)
        for assert_one in assert_expr_list:
            logger.info(f"断言表达式、期望结果和比对方式为：\n{assert_one}")
            # 通过jsonpath表达式得到实际结果,是个列表。
            actual_list = jsonpath(resp, assert_one["expr"])
            logger.info(f'提取的jsonpath表达式为：{assert_one["expr"]}')
            logger.info(f"提取之后的结果为(为列表，比对的是列表里面的值)：{actual_list}")
            logger.info(f'期望结果为：{assert_one["expected"]}')
            if assert_one["compare_type"] == "==":
                logger.info("比对期望和实际是否相等！")
                try:
                    assert actual_list[0] == assert_one["expected"]
                    logger.info("比对成功！")
                except:
                    # 写入日志
                    logger.exception("期望与实际不相等。")
                    # 如果某一个断言比对失败，那么返回False。不再进行下一个比对。
                    return False
        # 所有的断言表达式比完，返回True
        return True
    else:
        return False


if __name__ == '__main__':
    resp = {
        "code": 0,
        "msg": "OK",
        "data": {
            "id": 1236907132,
            "reg_name": "小明",
            "mobile_phone": "18688881115"
        }
    }
    assert_exprs = """[
{"expr":"$..code","expected":0,"compare_type":"=="},
{"expr":"$..msg","expected":"OK","compare_type":"=="},
{"expr":"$..reg_name","expected":"小明","compare_type":"=="}
]"""
    res = assert_resp(resp, assert_exprs)
    print(res)
