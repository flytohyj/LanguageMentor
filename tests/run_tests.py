import unittest
import os
import sys
import coverage

# 添加项目根目录到 Python 路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def run_tests():
    # 初始化覆盖率检测
    cov = coverage.Coverage(source=['src'])
    cov.start()

    # 发现并运行所有测试
    test_loader = unittest.TestLoader()
    test_suite = test_loader.discover('tests', pattern='test_*.py')

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)

    # 停止覆盖率检测并生成报告
    cov.stop()
    cov.save()
    cov.report()

    return result.wasSuccessful()

if __name__ == '__main__':
    success = run_tests()
    sys.exit(not success)