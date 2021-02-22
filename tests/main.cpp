
#include <cstdio>
#include <vector>
#include <iostream>

template<typename T>
const T &stack_show(const T &I) { return I; }

int fibnacci(int i) {
    return stack_show(i <=1 ? i : (fibnacci(i-1) + fibnacci(i-2)));
}

int main() {
    int fib = 0;
    scanf("%d", &fib);
    printf("%d\n", fibnacci(fib));
    std::cout << fibnacci(fib) << std::endl;
}

