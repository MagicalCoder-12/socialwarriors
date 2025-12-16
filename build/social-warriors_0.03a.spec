# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['D:\\programs\\socialwarriors\\server.py'],
    pathex=['D:\\programs\\socialwarriors'],
    binaries=[],
    datas=[('D:\\programs\\socialwarriors\\assets', 'assets'), ('D:\\programs\\socialwarriors\\config', 'config'), ('D:\\programs\\socialwarriors\\stub', 'stub'), ('D:\\programs\\socialwarriors\\templates', 'templates'), ('D:\\programs\\socialwarriors\\villages', 'villages'), ('D:\\programs\\socialwarriors\\mods', 'mods')],
    hiddenimports=['requests', 'urllib3', 'certifi', 'jsonpatch', 'jsonpointer'],
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
    name='social-warriors_0.03a',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['D:\\programs\\socialwarriors\\build\\icon.ico'],
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=False,
    upx_exclude=[],
    name='social-warriors_0.03a',
)
