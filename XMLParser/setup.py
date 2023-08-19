from setuptools import setup, find_packages

setup(
    name="xml-parser",
    version="0.1",
    packages=find_packages(),
    namespace_packages=['parser', 'parser.xml'],
    install_requires=['project-core>=0.1'],
    entry_points={'parse.load': ['xml_parser=parser.xml.parser_xml:XMLParser']},
    data_files = [('files', ['files/source.xml', 'files/android.xml', 'files/foodmenu.xml', 'files/cds.xml' ])],
    zip_safe=False
)
