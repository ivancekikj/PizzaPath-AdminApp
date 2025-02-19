# How to run?

<ol>
    <li>Clone the repository</li>
    <li>Create a new virtual environment with python >= v3.10.</li>
    <li>Install the required packages in the environment using the following command:
        <pre>pip install -r requirements.txt</pre>
    </li>
    <li>Create a file called 'config.json' in the root folder with the following information:
        <pre>
{
  "secret_key": "",
  "debug": , // true or false
  "db": {
    "host": "",
    "user": "",
    "password": "",
    "port": , // an integer
    "name": ""
  }
}</pre>
    </li>
    <li>Create a new postgres database with the name specified in the config file.</li>
    <li>Run the following command to apply the migrations:
        <pre>python manage.py migrate</pre>
    <li>Run the following command to start the server:
        <pre>python manage.py runserver</pre>
    </li>
</ol>