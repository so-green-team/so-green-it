# So Green IT

Web API to respect green IT best practises

## Installation instructions

For now, So Green IT is still in development process, there is no installation procedure yet.

## API configuration

To configure the API, you'll need to provide a `config.json` file with the following informations at the root of your working directory.

The file must be filled with the following informations :

```json
{
    "type": "The type of the database used",
    "host": "The IP address of the domain name of your database",
    "port": "The port used by your database",
    "db": "The name of the database",
    "user": "The name of the user authorized to access to the database",
    "passwd": "The password of the user authorized to access to the database"
}
```

## Installation for a development environment

If you want to help us improve this API, you have to use the following command lines to set up your environment

```bash
$ git clone https://github.com/so-green-team/so-green-it.git
$ cd so-green-it
$ git checkout develop
$ pip3 install -e .
$ FLASK_APP=sogreenit FLASK_DEBUG=1 flask run
```