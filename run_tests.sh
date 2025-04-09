#!/bin/bash

BROWSER=${BROWSER:-"chromium"}
ORIGIN=${ORIGIN:-"JFK"}
DEST=${DEST:-"LHR"}
ADULTS=${ADULTS:-"2"}
CHILDREN=${CHILDREN:-"0"}
INFANTS=${INFANTS:-"0"}
CABIN=${CABIN:-"Economy"}

# Run pytest with parameters
pytest -v -s \
  --test-browser="$BROWSER" \
  --origin="$ORIGIN" \
  --destination="$DEST" \
  --adults="$ADULTS" \
  --children="$CHILDREN" \
  --infants="$INFANTS" \
  --cabin="$CABIN" \
  --html=~/Downloads/agoda/Reports/report_"$BROWSER".html \
  tests/