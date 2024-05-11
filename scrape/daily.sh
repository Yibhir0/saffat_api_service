#!/bin/bash
source ~/env/prayer/bin/activate
cd ~/saffat/scrape/
python3 main.py >> output
deactivate
