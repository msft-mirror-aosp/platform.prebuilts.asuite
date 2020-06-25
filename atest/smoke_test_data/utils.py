# Copyright 2020, The Android Open Source Project
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json
import os
import shutil
import subprocess

SMOKE_DIR = os.path.dirname(os.path.realpath(__file__))
TOP = 'ANDROID_BUILD_TOP'
TEST_RESULT = '/tmp/atest_result/LATEST/test_result'


def print_banner(title, passed=False):
    """Simple banner printer.

    Args:
        title: string of content that will be printed.
        passed: boolean that control the type of banner.
            True: ========================================
                  Running: --test-mapping Passed!
                  ========================================
            False:########################################
                  Running: --test-mapping
                  ########################################
    """
    banner = '#'
    content = '\nRunning: ' + title
    if passed:
        content += ' Passed!'
        banner = '='
    content += '\n'
    print('\n' + 40*banner + content + 40*banner + '\n')


def is_identical(desired, actual, target):
    """Tell whether two values are indentical or not.

    Args:
        desired: can be any type.
        actual: can be any type.
        target: A string to print before returning False.

    Returns:
        Boolean: True when they are the same, otherwise False.
    """
    if str(desired) != str(actual):
        print('{} should be {} instead of {}.'.format(target, desired, actual))
        return False
    return True


def is_passed(expected_rc, actual_rc, args, message):
    """Ensure test is passed by checking return code and test_result.

    Args:
        args: A string that passed to atest. e.g. '--test-mapping'
        expected_rc: An integer that we expected atest to return.
        actual_rc: An integer that returned by atest.
        message: A string to print before returning False.
    Returns:
        True if ['FAILED'] == 0 and the expected rc is equal to the actual rc,
        otherwise False.
    """
    # 1. Return code must be identical.
    if not is_identical(expected_rc, actual_rc, message):
        return False
    # 2. No FAILED in test_result.
    if os.path.exists(TEST_RESULT):
        with open(TEST_RESULT, 'r') as cache:
            result = json.load(cache)
        if (result['args'] == args and result['total_summary']['FAILED'] != 0):
            print("\nThe test passed but failures found in {}".format(TEST_RESULT))
            return False
    return True


def init_test_mapping_files(action='delete'):
    """Method that create or delete TEST_MAPPING while running smoke testing.

    Args:
        action: A string to decide the action: 'delete' is to remove TEST_MAPPING
               while 'create' is copying from test_mapping.json to TEST_MAPPING.
    """
    tma = [os.path.join(SMOKE_DIR, 'test_mappings/A/test_mapping.json'),
           os.path.join(SMOKE_DIR, 'test_mappings/A/TEST_MAPPING')]
    tmb = [os.path.join(SMOKE_DIR, 'test_mappings/A/B/test_mapping.json'),
           os.path.join(SMOKE_DIR, 'test_mappings/A/B/TEST_MAPPING')]
    if action == 'create':
        for tm in (tma, tmb):
            shutil.copy2(tm[0], tm[1])
    elif action == 'delete':
        cmd = 'find {} -name TEST_MAPPING -exec rm -f {{}} \;'.format(SMOKE_DIR)
        subprocess.call(cmd, shell=True)


def get_test_counts():
    """Get the number of testing targets are as expected from test_result.

    E.g. atest targetA targetB, running get_test_counts() should return 2.

    Returns:
        An integer that AtestTradefedTestRunner appears in test_result.
    """
    if os.path.exists(TEST_RESULT):
        with open(TEST_RESULT, 'r') as cache:
            result = json.load(cache)
        return len(result['test_runner']['AtestTradefedTestRunner'].keys())
    return 0


def func_wrapper(func, args):
    """This method is for the convenience of invoking the function by passing
    argument as a list.

    Args:
        func: A method name.
        args: A list of argument.
    """
    func(*args)
