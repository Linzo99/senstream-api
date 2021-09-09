from setuptools import setup


setup(
    name="senstream-api",
    version="1.0",
    py_modules=["cli"],
    install_requires = [
        'Click',
    ],
    entry_points={
        'console_scripts':[
            'senstream-api = cli:cli '
        ],
    },
)