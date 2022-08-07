import os
from subprocess import call

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PACKAGE_DIR = os.path.join(CURRENT_DIR, '..', 'pydalle')
SOURCE_DIR = os.path.join(CURRENT_DIR, 'source')
OUTPUT_FORMATS = ["html"]

print(f"Generating API documentation for {PACKAGE_DIR}")
call(["sphinx-apidoc", "-E", "-a", "-o", SOURCE_DIR, PACKAGE_DIR])
for output_format in OUTPUT_FORMATS:
    print(f"Generating {output_format} documentation")
    call(["make", output_format], cwd=CURRENT_DIR)
