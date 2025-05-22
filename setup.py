from setuptools import setup, find_packages

with open("README.md", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="meu_pacote_spark",
    version="0.1.0",
    author="Luis Felipe Pereira",
    author_email="seu.email@exemplo.com",
    description="Pacote para processamento de dados com Spark",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/lipebr321/meu-projeto-spark",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "pyspark>=3.0.0",
        "pandas>=1.0.0",
        "pytest>=6.0.0",
    ],
)
