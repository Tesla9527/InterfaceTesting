import optparse
import os
from xmlrunner import XMLTestRunner

from Case.AccountTest import *


def run_full_suite(env='dev', port=8080):
    print('run full suite')
    account_test_cases = unittest.TestLoader().getTestCaseNames(AccountTest)

    account_test_suite = unittest.TestSuite(AccountTest(case, env, port) for case in account_test_cases)

    suites = [account_test_suite]
    for i in range(len(suites)):
        runner = XMLTestRunner(output=file('reports/report_' + str(i) + '.xml', 'w'))
        runner.run(suites[i])


def run_smoke_suite(env='dev', port=8080):
    print('run smoke suite')
    account_test_cases = ['test_login_001_correntPassword']
    account_test_suite = unittest.TestSuite(AccountTest(case, env, port) for case in account_test_cases)
    suites = [account_test_suite]

    for i in range(len(suites)):
        runner = XMLTestRunner(output=file('reports/report_' + str(i) + '.xml', 'w'))
        runner.run(suites[i])


def run_suite(env, suite, port=8080):
    print 'run suite'
    test_cases = unittest.TestLoader().getTestCaseNames(suite)
    suite = unittest.TestSuite(suite(case, env, port) for case in test_cases)
    runner = XMLTestRunner(output=file('reports/report.xml', 'w'))
    runner.run(suite)


def clean_reports():
    folder = 'reports'
    if not os.path.exists(folder):
        os.mkdir(folder)
    for file in os.listdir(folder):
        file_path = os.path.join(folder, file)
        try:
            if os.path.isfile(file_path):
                os.remove(file_path)
        except Exception as e:
            print e


def main():
    parser = optparse.OptionParser(usage='Interface automation test', formatter=optparse.IndentedHelpFormatter())
    parser.add_option('-s', '--suite',
                      default='smoke',
                      dest='suite',
                      action='store',
                      type='string',
                      help='specify test type, smoke or full. Default = full')

    parser.add_option('-e', '--env',
                      default='dev',
                      dest='env',
                      action='store',
                      type='string',
                      help='specify a server, dev or production. Default = dev')

    parser.add_option('-p', '--port',
                      default='8080',
                      dest='port',
                      action='store',
                      type='string',
                      help='specify a port number. Default = 8080')

    (options, args) = parser.parse_args()

    env = options.env
    port = options.port
    suite = options.suite
    suite = 'full'
    clean_reports()

    if suite == 'smoke':
        run_smoke_suite(env=env, port=port)
    elif suite == 'full':
        run_full_suite(env=env, port=port)
    else:
        s = globals()[suite]
        run_suite(env=env, port=port, suite=s)


if __name__ == '__main__':
    main()
