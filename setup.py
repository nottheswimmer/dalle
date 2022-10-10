from setuptools import setup, find_packages

REPO_URL = 'https://github.com/nottheswimmer/dalle'
REPO_BLOB_PREFIX = f'{REPO_URL}/blob/main/'


def github_md_to_setup_md(md: str) -> str:
    # Replace relative links with absolute links to blobs in the repo
    md = md.replace('](./', f']({REPO_BLOB_PREFIX}')
    return md


with open('README.md', encoding='utf-8') as f:
    long_description = github_md_to_setup_md(f.read())

setup(
    name='pydalle',
    version='0.2.0',
    description='A library for providing programmatic access to the DALL·E 2 API',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Michael Phelps',
    author_email='michaelphelps@nottheswimmer.org',
    url=REPO_URL,
    packages=find_packages(),
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    extras_require={
        'async': ['aiofiles', 'aiohttp'],
        'sync': ['requests'],
        'images': ['pillow', 'numpy'],
        'all': ['aiofiles', 'aiohttp', 'requests', 'pillow', 'numpy'],
    },
)
