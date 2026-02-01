#!/bin/bash
# .env 파일 접근 차단 hook

INPUT=$(cat)
FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // .tool_input.command // empty')

if [[ "$FILE_PATH" == *".env"* ]]; then
  echo ".env 파일은 보호되고 있습니다. 접근이 차단되었습니다." >&2
  exit 2
fi

exit 0
