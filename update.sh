#!/bin/sh

FILE_PATH="$1"
NEW_TAG="$2"

if [ -z "$FILE_PATH" ] || [ -z "$NEW_TAG" ]; then
  echo "Usage: $0 <file-path> <new-tag>"
  exit 1
fi

# Portable sed without -i
sed "s#\(image:.*:\).*#\1${NEW_TAG}#g" "$FILE_PATH" > "${FILE_PATH}.tmp"
mv "${FILE_PATH}.tmp" "$FILE_PATH"

echo "Updated image tag to: ${NEW_TAG} in $FILE_PATH"
