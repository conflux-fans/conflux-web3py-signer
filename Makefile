.PHONY: all build push

all: build

clean:
	rm -rf dist/

build: clean
	python3 setup.py sdist bdist_wheel

publish: 
	twine upload dist/* --repository conflux-web3py-signer

test:
	pytest tests
# cd ./docs && make doctest
