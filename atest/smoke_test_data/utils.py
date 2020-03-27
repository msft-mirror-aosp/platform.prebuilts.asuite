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

import os


SMOKE_DIR = os.path.dirname(os.path.realpath(__file__))
TOP = 'ANDROID_BUILD_TOP'


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

