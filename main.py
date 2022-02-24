import os
import time
import unittest
from BeautifulReport import BeautifulReport
from loguru import logger

from tools.handle_path import testcases_dir, report_dir, log_output_dir

# 获取当前时间
cur_time = time.strftime("%Y%m%d-%H%M%S", time.localtime())
# 添加日志输出到文件
logger.add(os.path.join(log_output_dir, "数字孪生平台-api-{}.log".format(cur_time)), encoding="utf-8")

# 收集测试用例
s = unittest.TestLoader().discover(testcases_dir)

runner = BeautifulReport(s)
runner.report(
        description="数字孪生平台-接口自动化测试报告",
        report_dir=report_dir,
        filename="python-api-autotest.html"
)



