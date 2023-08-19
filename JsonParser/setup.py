from setuptools import setup, find_packages

setup(
    name="json-parser",
    version="0.1",
    packages=find_packages(),
    namespace_packages=['parser', 'parser.json'],
    install_requires=['project-core>=0.1'],
    entry_points={'parse.load': 
                    ['json_parser=parser.json.parser_json:JsonParser'],},
    data_files = [('files', ['files/source.json', 'files/rides.json', 'files/employees.json',  'files/products.json'])],
    zip_safe=False
)
