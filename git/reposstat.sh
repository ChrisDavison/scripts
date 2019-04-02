#!/usr/bin/env bash
set -o errexit  # Exit early on error
set -o pipefail # Exit when a pipe fails
set -o nounset  # Exit when trying to use undeclared variables

for dir in $CODEDIR/*; do
    (cd "$dir" && git sstat)
done

for dir in ~/work/*; do
    (cd "$dir" && git sstat)
done
