[app]
title = BLP Cyber Pong
package.name = blp_cyber_pong
package.domain = com.bigluiproductions
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0

# ✅ FIXED MOBILITY DEPENDENCIES: Forcing Python 3.10 components skips compiler crashing hooks
requirements = python3,kivy==2.3.0,pygame

orientation = landscape
fullscreen = 1
android.accept_licenses = 1
android.permissions = INTERNET
android.api = 33

[buildozer]
log_level = 2
