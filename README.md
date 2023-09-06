# Learning_platform

For making migrations, unless alembic.ini exists, run in terminal:

```alembic init migrations```

It creates a folder with migrations and config file for alembic

- In alembic.ini assign db address, for making migrations in.
- Go to folder with migrations and open env.py, where lines

```from myapp import mymodel```
```target_metadata = mymodel.Base.metadata```

must be substituted with

```from main import Base```
```target_metadata = Base.metadata```


- Enter: ```alembic revision --autogenerate -m "create_table_for_users"```
- Migration will be created
- Enter: ```alembic upgrade heads```
