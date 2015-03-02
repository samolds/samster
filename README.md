SAMSTER
=======
This is a simple Django blogging site for personal use


System Requirements
-------------------
* Python 2.7
* VirtualEnv


Setup Instructions
------------------
* Clone the repository

    ```
    git clone https://github.com/samolds/samster.git
    ```

* Sandbox the app with VirtualEnv

    ```
    virtualenv --no-site-packages samster
    ```

* Activate the sandbox and install dependencies with Pip

    ```
    cd samster
    source bin/activate
    pip install -r sam/requirements.txt
    ```

* Change variable values accordingly in samster/local_settings.py
* Establish a database with a superuser

    ```
    python manage.py syncdb
    ```

* Run the site

    ```
    python manage.py runserver 8000
    ```


You should now have a skeleton of the site up and running on localhost:8000. Go to 'localhost:8000/admin', log in with the user established with the 'syncdb' command, and add posts to see content appear.
Checkout the [User Guide](userguide.md) for how to use this site once you have it up and running.
