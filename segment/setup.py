from setuptools import setup, PEP420PackageFinder

setup(
    name="segment",
    packages=PEP420PackageFinder.find("src"),
    package_dir={"": "src"},
    use_scm_version=True,
    setup_requires=["setuptools_scm"],
    install_requires=[
        "numpy",
        "pandas",
        "scipy",
    ],
    extras_require={
        "testing": ["pytest"],
        "documentation": ["sphinx", "sphinx_rtd_theme", "sphinx-autobuild", "sphinxcontrib-napoleon"],
    },
    zip_safe=False,
    classifiers=[
        "Intended Audience :: Science/Research",
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.7",
        "Topic :: Scientific/Engineering :: Statistics",
    ],
)
