#!/bin/bash

PROTOBUF_MAIN="proto/main.proto"
BACK_OUT_DIR="./back"
FRONT_DIR="./front"
TS_OUT_DIR="./ts_generated"

echo $PWD

protoc \
  $PROTOBUF_DIR \	
  --python_out="${BACK_OUT_DIR}" \
  --plugin="protoc-gen-ts=${FRONT_DIR}/node_modules/.bin/protoc-gen-ts" \
  --ts_out="service=grpc-web:${TS_OUT_DIR}"
