ifneq (,$(wildcard ./.env))
    include .env
    export
endif

.PHONY: build
build:
	py -m build

.PHONY: check
check:
	py -m twine check dist/*

.PHONY: upload
upload:
	py -m twine upload --skip-existing dist/*

.PHONY: uploadtest
uploadtest:
	py -m twine upload --repository testpypi --skip-existing dist/*

.PHONY: install
install:
	pip install .

.PHONY: devinstall
devinstall:
	pip install -e .
