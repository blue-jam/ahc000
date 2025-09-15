#!/bin/sh

if [ $# -eq 0 ]; then
    echo "Usage: $0 <zip_url>"
    echo "Example: $0 https://example.com/tools.zip"
    exit 1
fi

URL="$1"
TEMP_DIR=$(mktemp -d)
ZIP_FILE="$TEMP_DIR/download.zip"

echo "Downloading from: $URL"
if ! curl -L -o "$ZIP_FILE" "$URL"; then
    echo "Error: Failed to download from $URL"
    rm -rf "$TEMP_DIR"
    exit 1
fi

echo "Extracting to project root..."
if ! unzip -q "$ZIP_FILE" -d .; then
    echo "Error: Failed to extract zip file"
    rm -rf "$TEMP_DIR"
    exit 1
fi

rm -rf "$TEMP_DIR"
echo "Download and extraction completed successfully"
