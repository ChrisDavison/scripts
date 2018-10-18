if [ -z "$1" ]; then
    echo "Must give full branch name"
    exit
fi

if [ -z "$2" ]; then
    echo "Must give full parent branch name"
    exit
fi

git checkout "$2"
git pull --rebase
git merge "$1" --no-edit
git branch -D "$1"
git push origin --delete "$1"
