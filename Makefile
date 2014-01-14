
all: run

.PHONY: run 
run: 
	python bin/run.py 

clean:
	rm -rf data/*
	rm -rf */*.pyc

.PHONY: test
test:
	python test/*.py
