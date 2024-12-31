# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['novel_generator.py'],
    pathex=[],
    binaries=[],
    datas=[('novel_generator_ui.py', '.'), ('prompts.py', '.'), ('.env', '.'), ('02-novel.png', '.')],
    hiddenimports=['encodings.utf_8', 'codecs', 'dotenv', 'PySide6.QtCore', 'PySide6.QtWidgets', 'PySide6.QtGui'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='AI小说生成器',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    version='version.txt',
    icon=['02-novel.png'],
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='AI小说生成器',
)
