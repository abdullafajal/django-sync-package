import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="django-sync-package",
    version="0.2.0",
    author="Abdulla Fajal",
    author_email="abdullafajal@gmail.com",
    description="A Django package for database synchronization",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/abdullafajal/django-sync-package",
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=[
        "Django>=3.2",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "Topic :: Database",
    ],
    python_requires='>=3.8',
    zip_safe=False,
)
