.PHONY: tests container
.SILENT: tests container

clean:
	rm -rf .hypothesis .pytest_cache __pycache__ */__pycache__

container:
	abaco deploy -k -R

tests: clean container
	bash tests/run_container_tests.sh pytest tests -s
	bash tests/run_local_message.sh
