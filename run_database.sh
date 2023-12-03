#!/bin/bash

for i in $(seq 1 85); do
  python3 database-utilities.py
  echo "Finished running database-utilities $i times"
done
