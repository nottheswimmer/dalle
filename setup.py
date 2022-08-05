from setuptools import setup, find_packages

with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='pydalle',
    version='0.0.5',
    description='A library for providing programmatic access to the DALL·E 2 API',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Michael Phelps',
    author_email='michaelphelps@nottheswimmer.org',
    url='https://github.com/nottheswimmer/dalle',
    packages=find_packages(),
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
