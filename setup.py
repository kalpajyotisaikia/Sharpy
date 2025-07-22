"""
Setup script for Sharpy Educational App
"""
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="sharpy-educational-app",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A comprehensive educational platform with mobile authentication and gamification",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/sharpy-educational-app",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Education",
        "Topic :: Education :: Computer Aided Instruction (CAI)",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.11",
    install_requires=[
        "streamlit>=1.28.0",
        "psycopg2-binary>=2.9.7",
        "twilio>=8.2.0",
        "plotly>=5.15.0",
        "pandas>=2.0.0",
        "python-dotenv>=1.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "black>=22.0.0",
            "flake8>=5.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "sharpy-app=app:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.toml", "*.md"],
    },
)