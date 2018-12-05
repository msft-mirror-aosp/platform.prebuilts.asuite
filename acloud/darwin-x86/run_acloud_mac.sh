#!/bin/bash
# This script will check and setup the mac env to run acloud.
ACLOUD_BIN=$1

# Install macports python if it's not available.
if [[ ! -f /opt/local/bin/python2.7 ]]; then
    echo "acloud requires macports python27, installing now..."
    if ! POSIXLY_CORRECT=1 sudo /opt/local/bin/port -N install python27; then
        echo "Failed to install python27, exiting out"
        exit 1
    fi
fi

# Let's use macports python since the builtin python may be too old.
PATH=/opt/local/bin:$PATH $ACLOUD_BIN "${@:2}"
