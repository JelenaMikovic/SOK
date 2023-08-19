from setuptools import setup, find_packages

setup(
    name="visualization-complex",
    version="0.1",
    packages=find_packages(),
    install_requires=['project-core>=0.1'],
    entry_points={'visualization.display':
            ['visualization_complex=visualization.visualization_complex:VisualizationComplex']},
    zip_safe=True
)
