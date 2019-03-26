#!/usr/bin/env bash
# Copyright 2019, The Android Open Source Project
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

# filenames that will be checked permissions.
targets="atest|acloud|aidegen"

function permission_checker() {
    invalid_items=""
    for item in "$@"; do
        if [ -n "$(echo $(basename $item)|egrep "$targets")" -a ! -x "$item" ]; then
            invalid_items="$item $invalid_items"
        fi
    done
    if [ -n "$invalid_items" ]; then
        echo -e "\nInsufficient permission detected:"
        while read line; do
            echo "- $line"
        done < <(echo $invalid_items| sed 's/\ /\n/g')
        echo "Please run the following command and try again:"
        echo "chmod 0755 $invalid_items"
        return 1
    fi
}

function release_checker_main() {
    # The main function is going to check:
    # - permission of prebuilts.
    # - integration tests.
    # - other needed tests.
    PREBUILTS_DIR=$ANDROID_BUILD_TOP/prebuilts/asuite
    permission_checker $(find $PREBUILTS_DIR/{acloud,aidegen,atest}/{linux,darwin}-x86 -type f)
    # TODO: do integration tests for asuite when they are available.
}

release_checker_main
