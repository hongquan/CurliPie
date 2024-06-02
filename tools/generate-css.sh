#! /usr/bin/bash
set -euxo pipefail

bunx unocss 'api/**/*.jinja' -o api/_public/uno.css
