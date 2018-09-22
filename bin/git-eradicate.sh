if [ -z "$1" ]; then
    echo "$1"
fi
# git filter-branch -f  --index-filter \
#     'git rm --force --cached --ignore-unmatch "$1"' \
#      -- --all
# rm -Rf .git/refs/original && \
#     git reflog expire --expire=now --all && \
#     git gc --aggressive && \
#     git prune
