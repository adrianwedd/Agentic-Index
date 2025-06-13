#!/usr/bin/env bash
# Install dependencies for pa11y and ensure Chrome is available
set -e

# Install pa11y globally
npm install -g pa11y

# Install Chrome for puppeteer
npx puppeteer browsers install chrome
