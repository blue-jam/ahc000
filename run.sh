#!/bin/sh
# Usage:
# ./run.sh 1    # Execute the program for tools/in/0001.txt and save the stdout to tools/out/0001.txt
# ./run.sh 1 -c # Copy the stdout to the clipboard
# ./run.sh 1 -o # Print the stdout to the terminal
set -e

compile="cargo build --release"
run="cargo run --release"

if [ -z "$1" ]; then
  echo "Usage: $0 <test_number> [-c] [-o]" >&2
  exit 1
fi

test_number=$1

shift 1
while getopts "co" opt; do
  case $opt in
    c)
      copy=true
      ;;
    o)
      stdo=true
      ;;
    \?)
      echo "Invalid option: -$OPTARG" >&2
      ;;
  esac
done

if [ -n "$stdo" ] && [ -n "$copy" ]; then
  echo "Options -c and -o are mutually exclusive" >&2
  exit 1
fi

input="tools/in/$(printf "%04d" "$test_number").txt"
output="tools/out/$(printf "%04d" "$test_number").txt"

mkdir -p tools/out

$compile

if [ -z "$stdo" ]; then
  time $run < "$input" > "$output"
else
  time $run < "$input"
fi

echo >&2
echo "Executed successfully" >&2

if [ -n "$copy" ]; then
  # Check the OS
  case $(uname) in
    Darwin*)  pbcopy < "$output" ;;
    Linux*)   xclip -selection clipboard < "$output" ;;
    *)        echo "Unsupported OS: $(uname)" >&2 ;;
  esac
  echo "Copied to clipboard" >&2
fi
