
#include <cstdio>
#include <vector>

std::vector<int> numbers;
int fibnacci(int i) {
    int res = i <=1 ? i : fibnacci(i-1) + fibnacci(i-2);
    numbers.push_back(res);
    return res;
}

int main() {
    printf("hello world");
    fibnacci(5);
    printf("%d\n", *numbers.begin());
}

