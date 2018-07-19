cd %~dp0
mkdir bin
javac -encoding utf-8 -classpath lib\ojdbc7.jar -d bin src\cn\com\transcosmos\OracleConnector.java
jar cvfm ..\oracle_connector.jar META-INF\MANIFEST.MF -C bin cn
rmdir /S /Q bin
cd ..\..
