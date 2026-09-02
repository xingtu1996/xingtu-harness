#!/usr/bin/env bash
# XingTu Harness 安装器：一键拉取全部子模块
set -euo pipefail

echo "=============================================="
echo "  XingTu Harness · 一键安装"
echo "=============================================="

# 1. 初始化子模块
echo "[1/3] 拉取全部子模块..."
git submodule update --init --recursive

# 2. 校验
echo "[2/3] 校验子模块..."
for m in xingtu-skills xingtu-hooks xingtu-rules xingtu-sdd xingtu-mcps xingtu-cli xingtu-tools tokenhub-bench; do
  if [ -d "$m" ] && [ -f "$m/README.md" ]; then
    echo "  ✓ $m"
  else
    echo "  ✗ $m 缺失"
  fi
done

# 3. 汇总
echo "[3/3] 完成！"
echo "----------------------------------------------"
echo "  查看场景:  ./harness list"
echo "  安装场景:  ./harness install scene:<id>"
echo "----------------------------------------------"
