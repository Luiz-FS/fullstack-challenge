migrate:
	-$(MAKE) run-dependecies
	docker-compose exec api python manage.py migrate --noinput
	docker-compose exec authenticator python manage.py migrate --noinput

test:
	-$(MAKE) run-dependecies
	bash test_runner.sh

run-dependecies:
	docker-compose -f docker-compose-dependecies.yml up -d

run:
	-$(MAKE) run-dependecies
	docker-compose up -d

logs:
	docker-compose logs -f

down:
	docker-compose down

down-dependecies:
	docker-compose -f docker-compose-dependecies.yml down
