# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

medocker_a = Analysis(
    ['src/medocker.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('templates', 'templates'),
        ('config', 'config'),
        ('docs', 'docs'),
    ],
    hiddenimports=[
        'flask',
        'flask_wtf',
        'wtforms',
        'yaml',
        'waitress',
        'web',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

configure_a = Analysis(
    ['src/configure.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('config', 'config'),
    ],
    hiddenimports=[
        'yaml',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

web_a = Analysis(
    ['src/run_web.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('templates', 'templates'),
    ],
    hiddenimports=[
        'flask',
        'flask_wtf',
        'wtforms',
        'yaml',
        'waitress',
        'web',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

medocker_pyz = PYZ(medocker_a.pure, medocker_a.zipped_data, cipher=block_cipher)
configure_pyz = PYZ(configure_a.pure, configure_a.zipped_data, cipher=block_cipher)
web_pyz = PYZ(web_a.pure, web_a.zipped_data, cipher=block_cipher)

# Main CLI executable (single-file mode)
medocker_exe = EXE(
    medocker_pyz,
    medocker_a.scripts,
    medocker_a.binaries,
    medocker_a.zipfiles,
    medocker_a.datas,
    [],
    name='medocker',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

# Configure executable (single-file mode)
configure_exe = EXE(
    configure_pyz,
    configure_a.scripts,
    configure_a.binaries,
    configure_a.zipfiles,
    configure_a.datas,
    [],
    name='medocker-configure',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

# Web UI executable (single-file mode)
web_exe = EXE(
    web_pyz,
    web_a.scripts,
    web_a.binaries,
    web_a.zipfiles,
    web_a.datas,
    [],
    name='medocker-web',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
) 