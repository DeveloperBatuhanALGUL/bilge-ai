from setuptools import setup, find_packages

setup(
    name="bilge-ai-sdk",
    version="0.1.0-alpha",
    author="Batuhan ALGÜL",
    author_email="batuhanalgul@proton.me",
    description="Bilge Ulusal Açık Kaynak Zekâ Çerçevesi için Python İstemcisi",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/DeveloperBatuhanALGUL/bilge-ai",
    packages=find_packages(include=['sdk']),
    install_requires=[
        'requests>=2.31.0',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    python_requires='>=3.9',
)
