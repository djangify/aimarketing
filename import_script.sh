#!/bin/bash
for i in {5..225..5}
do
  echo "Importing posts with offset $i"
  python3 manage.py import_wordpress export.json --download-images --limit 5 --offset $i
  sleep 2  # Small pause between imports
done
