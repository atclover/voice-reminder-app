[app]
title = Voice Reminder
package.name = voicereminder
package.domain = org.remind
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1
requirements = python3,kivy,plyer,android
orientation = portrait
fullscreen = 0
android.permissions = VIBRATE,WAKE_LOCK
android.api = 31
android.minapi = 21
android.sdk = 30
android.ndk = 23b
android.archs = arm64-v8a

[buildozer]
log_level = 2
warn_on_root = 1