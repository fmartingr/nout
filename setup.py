from setuptools import setup

setup(
    name='nout',
    version='0.0.1',
    author='Felipe Martin',
    author_email='me@fmartingr.com',
    url='https://github.com/fmartingr/nout',
    description='Simple note taking app',
    keywords='note taking app files markdown',
    license='MIT',
    packages=['nout'],
    install_requires=['dataset', 'click', 'watchdog'],
    entry_points={
        'console_scripts': [
            'nout=nout.cli:cli',
        ],
    },
    classifiers=[],
)
