#!/usr/bin/env sh

TOOLS=./build/tools
$TOOLS/caffe train \
  --examples/exercise-deepid1/solver.prototxt

