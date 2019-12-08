branch=${1:-$(git branch-name)}
if [ "${branch}" == "master" ]; then
    echo "Cannot finish from 'master'"
    exit -1
fi
parent=${2:-"master"}

if [ "${branch}" == "${parent}" ]; then
    echo "Cannot merge to the same branch"
    exit -2
fi

git checkout "${parent}"
git pull --rebase
git merge "${branch}" --no-edit
echo "Delete local branch ${branch}"
git branch -D "${branch}"
echo "Delete remote branch :${branch}"
git push origin --delete "${branch}"
