PROJECT_NAME=flask_wiki
ENV=~/.virtualenvs/flask-wiki
PYTHON=$(ENV)/bin/python
PIP=$(ENV)/bin/pip

source_dbname=flask_wiki
source_db_hostname=localhost
test_db_hostname=localhost
test_dbname=flask_wiki_test

init: virtualenv requirements

run:
	@$(PYTHON) manage.py runserver

shell:
	@$(PYTHON) manage.py shell

test:
	@$(PYTHON) manage.py test

createdb:
	@echo "Creating database $(PROJECT_NAME)"
	createdb -h ${source_db_hostname} -U postgres -O postgres ${source_dbname} > /dev/null
	@$(PYTHON) manage.py create_db

dropdb:
	@echo "Dropping database $(PROJECT_NAME)"
	dropdb --if-exists -h ${source_db_hostname} -U postgres ${source_dbname} > /dev/null

flushdb:
	@echo "Flushing database tables"
	dropdb
	createdb

fresh_test_db: drop_test_db create_test_db

create_test_db: check_test_db_arg_exists
	createdb -h ${source_db_hostname} -U postgres -O postgres ${test_dbname} > /dev/null
	pg_dump -U postgres -h ${source_db_hostname} -s --no-owner --no-acl ${source_dbname} | psql -U postgres -h ${test_db_hostname} ${test_dbname} > /dev/null

drop_test_db: check_test_db_arg_exists
	psql -h ${test_db_hostname} -U postgres -c "SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE datname='${test_dbname}'" > /dev/null
	dropdb --if-exists -h ${test_db_hostname} -U postgres ${test_dbname} > /dev/null

check_test_db_arg_exists:
ifndef test_dbname
	@echo "Please specify test_dbname at Makefile.my!"
	@exit 1
endif
	@echo 'OK'

virtualenv:
	@echo "Creating virtual environment within $(ENV) directory"
	@virtualenv -q $(ENV)
	@source $(ENV)/bin/activate

requirements:
	@echo "Installing requirements"
	@$(PIP) install -qr requirements.txt

clean:
	@echo "Cleaning *.pyc files"
	@find . -name "*.pyc" -exec rm -f {} \;
