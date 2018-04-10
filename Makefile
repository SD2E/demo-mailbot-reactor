.PHONY: tests container tests-local tests-reactor tests-deployed
.SILENT: tests container tests-local tests-reactor tests-deployed

clean:
	rm -rf .hypothesis .pytest_cache __pycache__ */__pycache__

container:
	abaco deploy -k -R

tests-local: clean container
	bash tests/run_container_tests.sh pytest tests -s -vvv

tests-reactor: clean
	bash tests/run_local_message.sh

tests-deployed: clean
	bash tests/run_deployed_message.sh

tests: tests-local tests-reactor
	true

deploy: clean
	bash tests/run_deploy_with_updates.sh
