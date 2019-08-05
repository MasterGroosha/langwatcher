#!/bin/bash

cd /home/botfather/langwatcher/python
bin/python watcher.py
cd ..
git pull
cd langwatcher-site
hugo
cd ..
git add .
git commit -m "Autocommit $(date +%Y%m%d-%H:%M)"
git push origin master
echo "Done"
