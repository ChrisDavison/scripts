#!/usr/bin/env bash
set -euo pipefail

sudo sh -c "echo 3 > '/proc/sys/vm/drop_caches' && swapoff -a && swapon -a && echo 'RAM-Cache and Swap Cleared'"
