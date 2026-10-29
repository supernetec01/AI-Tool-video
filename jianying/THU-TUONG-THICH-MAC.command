#!/bin/bash
cd -- "$(dirname -- "$0")" || exit 1
python3 install.py --smoke "$@"
read -r -p "Nhan Enter de dong cua so... " _mombite_reply
