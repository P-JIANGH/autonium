pip install -U setuptools
pip install -U wheel
REM Common Useful package
pip install numpy
REM Test framework
pip install selenium
pip install hypothesis
REM Web framework
pip install django
pip install django-cors-headers
REM Database Driver
pip install psycopg2
pip install .\database_driver\install_package\mysqlclient-1.3.13-cp36-cp36m-win32.whl
pip install .\database_driver\install_package\mysqlclient-1.3.13-cp37-cp37m-win_amd64.whl
pip install .\database_driver\install_package\pymssql-2.1.3-cp36-cp36m-win32.whl
pip install .\database_driver\install_package\pymssql-2.1.4-cp37-cp37m-win_amd64.whl
REM install JVM driver
pip install .\database_driver\install_package\JPype1-0.6.3-cp36-cp36m-win32.whl
pip install .\database_driver\install_package\JPype1-0.6.3-cp37-cp37m-win_amd64.whl
REM Excel
pip install xlwings
pip install Pillow
pip install tablib[pandas]
