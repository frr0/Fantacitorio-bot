#!/bin/sh

snscrape --jsonl --progress --max-results 200 twitter-search "from:Fanta_citorio" > tweets.json && cat tweets.json | jq '.content' > data.txt
