from setuptools import setup, find_packages

setup(
    name="quickping",
    version="1.0.0",
    description="QuickPing – Terminal-based internet speed test",
    author="Augustin William",
    packages=find_packages(),   # automatically find 'quickping'
    install_requires=[
        "rich>=13.0.0",
        "pyfiglet>=0.8.post1",
        "speedtest-cli>=2.1.3"
    ],
    entry_points={
        "console_scripts": [
            "quickping=quickping.main:main",
        ],
    },
    python_requires=">=3.8",
)
