import os

"""
配置项目下的路径
1、得到项目根目录
2、拼接根目录、子包目录得到不同层级的路径。
"""
# basedir
basedir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

conf_path = os.path.join(basedir, 'conf')

# 日志配置文件路径
log_conf_path = os.path.join(conf_path, 'log.ini')
# 日志输出路径
log_output_dir = os.path.join(basedir, 'outputs', 'logs')
# 报告输出路径
report_dir = os.path.join(basedir, 'outputs', 'reports')

# 测试数据dir
testdatas_dir = os.path.join(basedir, 'testdatas')

# 测试用例dir
testcases_dir = os.path.join(basedir, 'testcases')

if __name__ == '__main__':
    print(testcases_dir)
