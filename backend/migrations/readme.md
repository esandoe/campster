Single-database configuration for Flask using Flask-Migrate. See [official docs](https://flask-migrate.readthedocs.io/en/latest/) for further info.

The database should be automatically created and migrated to the latest version the first time to start the application. Use the following commands to create new migrations or upgrade the database later.

### Add new migration
Make the necessary changes in the database models, and then run:
```console
flask db migrate -m "Increase marshmallow storage capacity"
```

Remember to use imperative form when writing migration messages!

Revise the newly created migration script (inside the /versions folder) before upgrading the database.

### Upgrade the database

If you have new migrations to apply, run the following to upgrade the database:
```console
flask db upgrade
```
