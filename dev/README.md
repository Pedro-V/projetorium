# Projetorium Web

Aplicação Web do Projetorium, escrito em Django.

# Executando

```sh
# Primeiro, garanta que o estado da aplicação é o inicial:
$ rm -f db.sqlite3
# Execute as migrações de banco e execute a aplicação em localhost:8000.
# A migração inicial sempre cria dados fundamentais (departamentos, cursos, etc).
$ python manage.py migrate
$ python manage.py runserver
```
