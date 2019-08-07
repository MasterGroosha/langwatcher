#!/bin/bash

git pull
cd /home/botfather/langwatcher/python
bin/python watcher.py
cd ../langwatcher-site
/usr/local/bin/hugo
sleep 2s
cd ..
git add .
git commit -m "Autocommit $(date +%Y%m%d-%H:%M) GMT"
git push origin master
echo "Done"
