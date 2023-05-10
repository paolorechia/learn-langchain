#!/bin/bash
cat generated_tasks.txt | tr -s ' ' | grep -oE '\s*[0-9]+\.[A-Za-z, ]+[A-Za-z, ]+\.' | awk 'length >= 50' | sed -e 's/[0-9\. ]*//' > filtered_generated.txt
