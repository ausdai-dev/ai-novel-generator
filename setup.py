from cx_Freeze import setup, Executable

build_exe_options = {
    "packages": ["PySide6", "openai", "requests"],
    "excludes": [],
    "include_files": ["README.md"]
}

setup(
    name="AI小说生成器",
    version="1.0",
    description="AI小说生成器",
    options={"build_exe": build_exe_options},
    executables=[
        Executable(
            "novel_generator.py",
            base="Win32GUI",
            target_name="AI小说生成器.exe"
        )
    ]
) 