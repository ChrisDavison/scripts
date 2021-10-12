#!/usr/bin/env bash
n_days=${1:-1}

echo "New files since $n_days days ago"
echo "(excluding deleted files)"
echo "--------------------------------"

files=$(git log --oneline --name-status --pretty="" --since="$n_days days" | sort -n | awk '/^[AM]/{print $2}' | uniq)
for f in ${files[@]}; do
    [[ -f $f ]] && echo $f
done
