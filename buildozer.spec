[app]
title = PayFlow QR Prototype
package.name = payflow
package.domain = com.shopnojo
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1.0
requirements = python3,kivy==2.3.1,qrcode,pillow
orientation = portrait
fullscreen = 0
android.api = 35
# Python 3.14 uses preadv/pwritev, available from Android API 24.
android.minapi = 24
android.archs = arm64-v8a, armeabi-v7a
android.accept_sdk_license = True

[buildozer]
log_level = 2
warn_on_root = 1
