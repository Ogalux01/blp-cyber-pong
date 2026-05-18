[app]
title = BLP Cyber Pong
package.name = blp_cyber_pong
package.domain = com.bigluiproductions
source.dir = .
source.include_exts = py,png,jpg,kv,atlas

# ✅ CRUCIAL: Added the exact version number so the build doesn't crash
version = 1.0

# ✅ CRUCIAL: Locked down the exact stable Pygame version for mobile
requirements = python3,pygame==2.5.2

orientation = landscape
fullscreen = 1

# ✅ CRUCIAL: Forces the compiler to automatically accept Android SDK licenses
android.accept_licenses = 1
android.permissions = INTERNET
android.api = 34

[buildozer]
log_level = 2
