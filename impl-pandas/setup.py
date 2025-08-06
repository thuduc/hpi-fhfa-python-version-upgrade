from setuptools import setup, find_packages

setup(
    name="rsai",
    version="1.0.0",
    description="Repeat-Sales Aggregation Index (RSAI) Model Implementation",
    author="RSAI Implementation Team",
    packages=find_packages(where="rsai"),
    package_dir={"": "rsai"},
    install_requires=[
        "pandas>=2.1.0",
        "numpy>=1.26.0",
        "statsmodels>=0.14.0",
        "scikit-learn>=1.3.0",
        "scipy>=1.11.0",
        "pydantic>=2.5.0",
        "pyarrow>=15.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-cov>=4.0.0",
        ]
    },
    python_requires=">=3.12",
)