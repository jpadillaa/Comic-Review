# Comic-Review
Un pequeño API REST con Python + Flask. Una excusa para desplegar una aplicación aprovechando diferentes servicios y recursos de AWS y/o GCP 

## apirest
Este directorio corresponde al API REST (backend) del proyecto.

## Tutorial Ambiente de Desarrollo
Realice las siguientes tareas para montar su ambiente de desarrollo.

1. En la carpeta del proyecto debe crear un ambiente virtual con la librería de `virtualenv` de python (previamente instalada). Llame el ambiente virtual `venv` para que sea ignorado por git.

2. Se debe activar el ambiente virtual (de la forma de preferencia: con VSCode o desde terminal a mano) y ejecutar `pip install -e .`. Con esto, se instalarán todas las dependencias definidas en el módulo de python creado para el backend.

3. (OPCIONAL) Instalar en VSCode el linter de preferencia para el ambiente virtual. De esta forma podrá saber mejor si está cometiendo algún error con alguna librería. Para más información siga el siguiente [enlace](https://medium.com/@aswens0276/vscode-pylint-setup-and-settings-for-python-flask-with-sqlalchemy-7ade0f14f321)

4. Cree una base de datos en postgres (motor previamente instalado). Algunos comandos que  que le pueden ayudar a crer la BD son:
    ```sql
    CREATE USER apirest;
    CREATE DATABASE api OWNER apirest;
    ALTER USER apirest WITH PASSWORD 'password';
    ```
5. Cree el archivo `.env` en la raíz del proyecto (recuerde que este archivo y el directorio instance están dentro del .gitignore por seguridad). Agregue todas las variables para que la aplicación se conecte a su base de datos:
    - **HOST** (endpoint de la BD), 
    - **DB** (Nombre de la BD), 
    - **DBUSER** (Usuario de la BD), 
    - **PORT** (Puerto de la BD default 5432), 
    - **PW** (Contraseña del usuario de la BD), 
    - **SECRET** (Contraseña de cifrado de Flask) y 
    - **JWTSECRET** (Contraseña de cifrado de JWT).

6. Abra una nueva terminal escriba los siguientes comandos para correr el proyecto:  
    En linux:
    ```bash
    $ export FLASK_APP=apirest
    $ export FLASK_ENV=development
    $ flask run
    ```
    En Windows:
    ```Powershell
    > $env:FLASK_APP="apirest"
    > $env:FLASK_ENV="development"
    > flask run --host=0.0.0.0
    ```
