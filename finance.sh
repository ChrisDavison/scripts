#!/usr/bin/env sh
if [ -z "$FINANCEFILE" ]; then
    echo "Need to define FINANCEFILE"
    return 1
fi
printf "Date: " && read ddate
printf "Cost: " && read cost
printf "Description: " && read desc
printf "Category: " && read category
echo $ddate","$cost","$desc","$category >> $FINANCEFILE
