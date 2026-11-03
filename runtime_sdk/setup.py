from setuptools import setup, find_packages

setup(
    name="aiforge-runtime",
    version="1.0.0",
    description="Universal inference runtime SDK for .aiforge model packages",
    packages=find_packages(),
    install_requires=[
        "numpy>=1.24.0",
        "pandas>=2.0.0",
        "scikit-learn>=1.3.0",
        "pillow>=10.0.0",
        "joblib>=1.3.0"
    ],
    extras_require={
        "torch": ["torch>=2.0.0", "torchvision>=0.15.0"]
    },
    python_requires=">=3.9",
)
