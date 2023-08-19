cd core
pip install .
cd ..


cd JsonParser
pip install .
cd ..

cd XMLParser
pip install .
cd ..



cd VisualizationSimple
pip install .
cd ..


cd VisualizationComplex
pip install .
cd ..


cd tim7_graph_visualization
python manage.py makemigrations
python manage.py migrate
python manage.py runserver