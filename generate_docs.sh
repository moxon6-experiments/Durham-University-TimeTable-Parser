#!/bin/bash
source project.conf
sudo rm -rf docs
sphinx-apidoc -A author_name -P -H project_name -M -e -f -F -o docs ${project_folder}/
python /home/martin/Documents/scripts/modify_conf.py
cd docs
make clean
make html
touch $null >> _build/html/.nojekyll
xdg-open _build/html/index.html
