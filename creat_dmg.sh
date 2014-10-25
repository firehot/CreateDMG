#!/bin/bash

APP_NAME="AppleTunerDemo.app"
OUTPUT_DMG="AppleTuner"
VOL_NAME="APPLETUNER"

DMG_DIR=`dirname "$0"`

rm -f $DMG_DIR/output/*

$DMG_DIR/create-dmg \
--volname $VOL_NAME \
--volicon $DMG_DIR/resource/icon.icns \
--background $DMG_DIR/resource/background.png \
--window-pos 300 300 \
--window-size 600 418 \
--icon-size 48 \
--icon $APP_NAME 450 100 \
--icon Applications 450 260 \
--hide-extension $APP_NAME \
$DMG_DIR/output/$OUTPUT_DMG.dmg \
$DMG_DIR/src
