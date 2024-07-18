#!/bin/sh
# Installer script
# Run pyinstaller
pyinstaller index.spec -y
echo "Done bundling the application. Moving on to creating dmg"
# Create a folder (named dmg) to prepare our DMG in (if it doesn't already exist).
mkdir -p dist/dmg
# Empty the dmg folder.
rm -r dist/dmg/*
# Copy the app bundle to the dmg folder.
cp -r "dist/Housify.app" dist/dmg
# If the DMG already exists, delete it.
test -f "dist/Housify.dmg" && rm "dist/Housify.dmg"
create-dmg \
  --volname "Housify" \
  --volicon "src/app.icns" \
  --window-pos 200 120 \
  --window-size 600 300 \
  --icon-size 100 \
  --icon "Housify.app" 175 120 \
  --hide-extension "Housify.app" \
  --app-drop-link 425 120 \
  "dist/dmg/Housify.dmg" \
  "dist/dmg/"

rm -r dist/dmg/Housify.app
rm -f dist/*.dmg