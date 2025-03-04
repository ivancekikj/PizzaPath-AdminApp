# Run the project

<ol>
    <li>Clone the repository</li>
    <li>Create a new virtual environment with python >= v3.10.</li>
    <li>Install the required packages in the environment using the following command:
        <pre>pip install -r requirements.txt</pre>
    </li>
    <li>Create a file called '.env' in the root folder with the following information:
        <pre>
API_KEY=
SECRET_KEY=
DEBUG=
DB_HOST=
DB_USER=
DB_PASSWORD=
DB_NAME=
DB_PORT=
</pre>
    </li>
    <li>Create a new postgres database with the name specified in the '.env' file.</li>
    <li>Run the following command to apply the migrations:
        <pre>python manage.py migrate</pre>
    <li>Run the following command to start the server:
        <pre>python manage.py runserver</pre>
    </li>
</ol>