[app]
# (str) Title of your application
title = BLP Cyber Pong

# (str) Package name
package.name = blp_cyber_pong

# (str) Package domain (needed for android packaging)
package.domain = com.bigluiproductions

# (str) Source code directory
source.dir = .

# (list) Source files to include (let it find python files)
source.include_exts = py,png,jpg,kv,atlas

# (list) Application requirements
# Crucial: Must include python3 and pygame
requirements = python3,pygame

# (str) Supported orientations (landscape forces full widescreen mobile format)
orientation = landscape

# (int) Fullscreen mode (1 = True, removes phone notification bar)
fullscreen = 1

# (list) Permissions
android.permissions = INTERNET

# (int) Target Android API, leave default or use 33/34
android.api = 34

[buildozer]
# (int) Log level (0 = error only, 1 = info, 2 = debug)
log_level = 2
