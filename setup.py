import setuptools

setuptools.setup(
    name="UM40_SMART_JSON_API_Framework",
    version="1.5.1",
    author="Buslin Nicolay",
    author_email="n.Buslin@allmonitoring.ru",
    description="This package is needed to forward and easy work with JSON to the required API for UM 40 SMART",
    # long_description=long_description, <<---README.md
    packages=setuptools.find_packages(),

    install_requires=[
        'paramiko', 'docker', 'virtualbox'
    ]
)
