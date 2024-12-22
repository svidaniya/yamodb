from setuptools import setup, find_packages

setup(
    name="yamodb",  # Nome da biblioteca
    version="0.0.1",     # Versão inicial
    description="powerful and lightweight library designed for data and database.",
    long_description=open("README.md", "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="svidaniya",
    author_email="seuemail@example.com",
    url="https://github.com/svidaniya/yamodb",  # Repositório do projeto
    packages=find_packages(),
    include_package_data=True,
    package_data={                                                          
        "yamodb": ["placeholder_database/*.json"],
    },  # Descobre pacotes automaticamente
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=["cryptography==3.4", "python-dateutil==2.9.0.post0", "PyYAML==6.0.2", "six==1.17.0"],
    python_requires=">=3.6",
)
