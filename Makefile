
test-main: build-dir
	g++ tests/main.cpp -g -o build/test-main

build-dir:
	mkdir -p build

