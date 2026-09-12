---
name: idb-ios-sumulator-automation
description: iOS Development Bridge (idb) - Facebook's command-line tool for automating iOS simulators and devices. Use when working with iOS simulators or physical devices for tasks like app installation, file management, screenshot/video capture, running tests, crash log analysis, accessibility inspection, and device automation. Triggers on queries about iOS simulator automation, device management, xctest execution, iOS app debugging, or any iOS development tooling tasks.
---

# iOS Development Bridge (idb)

idb is a flexible command-line interface for automating iOS simulators and devices. It provides a unified interface for interacting with both simulators and physical devices.

## Installation

```bash
# Install idb-companion (required for device/simulator communication)
brew install idb-companion

# Install idb client (Python CLI)
pip install fb-idb
```

**Requirements**: macOS with Xcode installed, Python 3.7+

## Architecture

idb uses a client-companion model:
- **idb_companion**: Runs on the Mac, communicates directly with devices/simulators
- **idb client**: CLI that connects to the companion via gRPC

For local use, the companion starts automatically. For remote devices, start the companion explicitly and connect.

## Core Commands

Before log streaming or video recording, choose a maximum capture duration and, when relevant, an earlier stop event. Run the process in a controllable session and stop it at the event or deadline; do not leave a foreground stream blocking task completion.

### Device/Simulator Management

```bash
# List all available targets (simulators and devices)
idb list-targets

# List only booted targets
idb list-targets --state booted

# Boot a simulator by UDID
idb boot <UDID>

# Shutdown a simulator
idb shutdown <UDID>

# Create a new simulator
idb create "iPhone 15" "com.apple.CoreSimulator.SimDeviceType.iPhone-15" "com.apple.CoreSimulator.SimRuntime.iOS-17-0"

# Delete a simulator
idb delete <UDID>

# Focus the simulator window
idb focus
```

### App Management

```bash
# Install an app (.app bundle or .ipa)
idb install /path/to/app.app
idb install /path/to/app.ipa

# Uninstall an app
idb uninstall com.example.app

# List installed apps
idb list-apps

# Launch an app
idb launch com.example.app

# Launch with arguments and environment variables
idb launch com.example.app --args "arg1" "arg2" --env KEY=VALUE

# Terminate an app
idb terminate com.example.app
```

### File Operations

```bash
# Push files to an app's container
idb file push /local/file.txt com.example.app/Documents/

# Pull files from an app's container
idb file pull com.example.app/Documents/file.txt /local/destination/

# List files in an app's container
idb file ls com.example.app/Documents/

# Delete files in an app's container
idb file rm com.example.app/Documents/file.txt

# Create a directory
idb file mkdir com.example.app/Documents/newdir
```

### Screenshots and Video

```bash
# Take a screenshot
idb screenshot /path/to/screenshot.png

# Record video (press Ctrl+C to stop)
idb record-video /path/to/video.mp4

# Record with specific codec
idb record-video --codec h264 /path/to/video.mp4
```

### Logs and Debugging

```bash
# Stream system logs
idb log

# Stream logs with predicate filter
idb log --predicate 'subsystem == "com.example.app"'

# Get crash logs
idb crash list

# Get specific crash log
idb crash show <crash_name>

# Delete crash logs
idb crash delete <crash_name>
idb crash delete --all
```

### Testing (XCTest)

```bash
# Install a test bundle
idb xctest install /path/to/tests.xctestrun

# List installed test bundles
idb xctest list

# Run all tests in a bundle
idb xctest run <test_bundle_id>

# Run specific test class or method
idb xctest run <test_bundle_id> --tests MyTestClass
idb xctest run <test_bundle_id> --tests MyTestClass/testMethod

# Run UI tests with target app
idb xctest run ui <test_bundle_id> --app-bundle-id com.example.app
```

### UI Interaction

```bash
# Tap at coordinates
idb ui tap 100 200

# Swipe
idb ui swipe 100 200 100 500

# Type text
idb ui text "Hello World"

# Press hardware buttons
idb ui button HOME
idb ui button SIRI
idb ui button LOCK

# Key events
idb ui key 4  # Key code
idb ui key-sequence 4 5 6
```

### UI Tree and Accessibility

```bash
# Get full UI accessibility tree (shows all elements with coordinates)
idb ui describe-all --udid <UDID>

# Describe element at point
idb ui describe-point 100 200 --udid <UDID>
```

**Key fields in UI tree output**:
- `AXFrame`: `{{x, y}, {width, height}}` - element position and size (use center for taps)
- `AXLabel`: Text label of the element
- `AXUniqueId`: testID if set in code
- `type`: Element type (Button, StaticText, Image, etc.)
- `enabled`: Whether element is interactive

### Settings and Preferences

```bash
# Set location
idb set-location 37.7749 -122.4194

# Clear keychain
idb clear-keychain

# Open URL
idb open "https://example.com"
idb open "myapp://deeplink"

# Approve permissions
idb approve com.example.app photos camera location

# Revoke permissions
idb revoke com.example.app photos
```

### Contacts and Media

```bash
# Add contacts
idb contacts update /path/to/contacts.db

# Add media (photos/videos)
idb add-media /path/to/photo.jpg
idb add-media /path/to/video.mp4
```

## Target Specification

Specify target for all commands with `--udid`:

```bash
idb --udid <UDID> launch com.example.app
```

Or set default target:
```bash
export IDB_UDID=<UDID>
```

## Common Workflows

### UI Testing Workflow

```bash
# 1. Find booted simulator
xcrun simctl list devices | grep Booted

# 2. Connect IDB to simulator (required before UI commands)
idb connect <UDID>

# 3. Get UI tree to find element coordinates
idb ui describe-all --udid <UDID>

# 4. Tap button (calculate center from AXFrame coordinates)
idb ui tap 410 590 --udid <UDID>

# 5. Long press for context menu
idb ui tap 400 400 --duration 1.0 --udid <UDID>

# 6. Take screenshot to verify
idb screenshot /tmp/screenshot.png --udid <UDID>
```

### Automated Test Run

```bash
# Boot simulator, install app and tests, run tests, capture results
idb boot <UDID>
idb install /path/to/MyApp.app
idb xctest install /path/to/MyAppTests.xctestrun
idb xctest run --json MyAppTests > results.json
idb shutdown <UDID>
```

### Debug Session Setup

```bash
idb boot <UDID>
idb install /path/to/Debug.app
idb launch --wait-for com.example.app
idb log --predicate 'process == "MyApp"'
```

### Screenshot Comparison Testing

```bash
idb launch com.example.app
idb ui tap 50 100  # Navigate to screen
sleep 1
idb screenshot /screenshots/screen1.png
```

## Troubleshooting

### Python 3.14+ Compatibility

idb's `get_event_loop()` fails on Python 3.14+. Use this workaround:

```bash
# Replace YOUR_COMMAND_HERE with actual idb args (e.g., "ui", "describe-all", "--udid", "XXX")
/path/to/pipx/venvs/fb-idb/bin/python -c "
import asyncio
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
import sys
sys.argv = ['idb', 'YOUR_COMMAND_HERE']
from idb.cli.main import main
main()
"
```

### Connection Issues

```bash
# Ensure simulator is booted
xcrun simctl list devices available | grep -E "(iPhone|iPad)"

# Connect before running UI commands
idb connect <UDID>

# Verify connection
idb list-targets --state booted
```

## Detailed Reference

For complete command options and advanced usage, see [references/commands.md](references/commands.md).
