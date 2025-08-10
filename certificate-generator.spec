# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

added_files = [
    ('README.html', 'README.html'),
    ('README.md', '.'),
    ('screenshots', 'screenshots'),
    ('appicon.ico', '.'),
    ('Ephesis-Regular.ttf', '.'),
    ('BonheurRoyale-Regular.ttf', '.'),
    ('Schoolbell-Regular.ttf', '.'),
    ('Birthstone-Regular.ttf', '.'),
    ('Hurricane-Regular.ttf', '.')
]

a = Analysis(
    ['certificate-generator.py'],
    pathex=[],
    binaries=[],
    datas=added_files,
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='CertificateGenerator',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='appicon.ico',
    onefile=True
)