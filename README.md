# How to run?

<ol>
    <li>Clone the repository</li>
    <li>Create a new virtual environment.</li>
    <li>Install the required packages in the environment using the following command:
        <pre>pip install -r requirements.txt</pre>
    </li>
    <li>Create a file called 'db_connection.json' in the folder 'project' with the following information:
        <pre>
{
    "host": "",
    "user": "",
    "password": "",
    "port": 
}</pre>
    </li>
    <li>Create a new postgres database called 'PizzaDeliciousDb'.</li>
    <li>Run the following command to apply the migrations:
        <pre>python manage.py migrate</pre>
    <li>Run the following command to start the server:
        <pre>python manage.py runserver</pre>
    </li>
</ol>