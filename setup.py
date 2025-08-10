from cx_Freeze import setup, Executable

include_files = [
    "README.html",
    "README.md",
    "screenshots/",
    "appicon.ico",
    "Ephesis-Regular.ttf",
    "BonheurRoyale-Regular.ttf",
    "Schoolbell-Regular.ttf",
    "Birthstone-Regular.ttf",
    "Hurricane-Regular.ttf"
]

build_options = {
    "build_exe": "build/CertificateGenerator",
    "packages": ["PIL", "pandas", "fpdf", "os", "tkinter", "markdown2"],
    "include_files": include_files,
    "include_msvcr": True
}

setup(
    name="CertificateGenerator",
    version="1.0",
    description="Generate 3KM/5KM certificates from CSV",
    options={
        "build_exe": build_options
    },
    executables=[
        Executable(
            "certificate-generator.py",
            base="Win32GUI" if sys.platform == "win32" else None,
            icon="appicon.ico"
        )
    ]
)