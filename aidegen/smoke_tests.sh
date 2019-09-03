#!/usr/bin/env bash

function run_usecases() {
    cd $ANDROID_BUILD_TOP
    build/soong/soong_ui.bash --make-mode aidegen_functional_test
    aidegen_functional_test-dev -b
}

function check_env() {
    if [ -z "$ANDROID_BUILD_TOP" ]; then
        echo "Missing ANDROID_BUILD_TOP env variable. Run 'lunch' first."
        exit 1
    fi
}

function cleanup() {
    pushd $ANDROID_BUILD_TOP
    build/soong/soong_ui.bash --make-mode clean
    popd
}

check_env
cleanup
run_usecases
