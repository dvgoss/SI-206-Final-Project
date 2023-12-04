#!/bin/bash
# Run the database-utilities file enough times (85) to fill the database with data for all the movies in the passed list. 
for i in $(seq 1 85); do
  python3 database-utilities.py
  echo "Finished running database-utilities $i times"
done
