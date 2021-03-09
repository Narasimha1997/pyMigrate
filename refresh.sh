#!/bin/bash

rm -r dist/*.whl
pip3 uninstall -y py-migrate
python3 setup.py bdist_wheel
pip3 install dist/*.whl