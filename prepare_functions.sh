#!/bin/bash

DIR_NAME=".lambda_functions"
BUILD_DIR="$DIR_NAME/"

if [ -d "$BUILD_DIR" ]; then
  rm -r "$BUILD_DIR"
fi
mkdir "$BUILD_DIR"

cp ./*.py "$BUILD_DIR"

(
  cd "$BUILD_DIR"
  zip -r "../$DIR_NAME.zip" ./*
)

rm -r "$BUILD_DIR"
