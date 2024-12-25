import PyInstaller.__main__

PyInstaller.__main__.run([
    'novel_generator.py',
    '--name=AI小说生成器',
    '--onefile',
    '--windowed',
    '--clean',
    '--add-data=README.md;.',
    '--hidden-import=PySide6.QtCore',
    '--hidden-import=PySide6.QtWidgets',
    '--hidden-import=PySide6.QtGui'
]) 