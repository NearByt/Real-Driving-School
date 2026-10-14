# assemble_hub.py - Assembles all components into index.html
import sys
sys.stdout.reconfigure(encoding='utf-8')

from part_css import CSS_CONTENT
from part_html import HTML_CONTENT
from part_js_core import JS_CORE_CONTENT
from part_js_state import JS_STATE_CONTENT
from part_js_views import JS_VIEWS_CONTENT
from part_js_init import JS_INIT_CONTENT

MASTER_HEAD = r'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover">
  <title>Real Driving School | Official Portal</title>
  <link rel="icon" type="image/svg+xml" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>🏎️</text></svg>">

  <!-- Mobile PWA Meta Tags -->
  <meta name="theme-color" content="#ffffff">
  <meta name="apple-mobile-web-app-capable" content="yes">
  <meta name="apple-mobile-web-app-status-bar-style" content="default">
  <meta name="apple-mobile-web-app-title" content="RDS Portal">
  <link rel="manifest" href="data:application/manifest+json,%7B%22name%22%3A%22Real%20Driving%20School%20Portal%22%2C%22short_name%22%3A%22RDS%20Portal%22%2C%22start_url%22%3A%22.%22%2C%22display%22%3A%22standalone%22%2C%22background_color%22%3A%22%23ffffff%22%2C%22theme_color%22%3A%22%23ffffff%22%7D">
'''

full_html = MASTER_HEAD + CSS_CONTENT + HTML_CONTENT + JS_CORE_CONTENT + JS_STATE_CONTENT + JS_VIEWS_CONTENT + JS_INIT_CONTENT

with open("index.html", "w", encoding="utf-8") as f:
    f.write(full_html)

print(f"Master index.html successfully assembled! Total bytes: {len(full_html)} chars, lines: {full_html.count(chr(10))}")
