from setuptools import setup, find_packages

setup(
    name="visualization-simple",
    version="0.1",
    packages=find_packages(),
    install_requires=['project-core>=0.1'],
    entry_points={'visualization.display':
            ['visualization_simple=visualization.visualization_simple:VisualizationSimple']},
    zip_safe=True
)
