setup:
	bash scripts/setup_dev_environment.sh

test:
	bash scripts/runtests.sh

coverage:
	coverage xml

ci:
	make test
	make coverage
