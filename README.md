# gdb-stack-trace

## Example

```bash
$ make test-main
$ gdb -ex "source core.py" build/test-main
>>> beg collecting of test case build/a.in...
 >>> beg execution
[Inferior 1 (process 28105) exited normally]
 <<< end execution

            _init (argc=1, argv=0x7fffffffdc18, envp=0x7fffffffdc28)
0x0000555555554880 in _start ()
    0x0000555555554b10 in __libc_csu_init ()
      0x00005555555547d8 in _init ()
main ()
  fibnacci (i=3)
    fibnacci (i=2)
      fibnacci (i=1)
        stack_show<int> (I=@0x7fffffffda74: 1)
      fibnacci (i=0)
        stack_show<int> (I=@0x7fffffffda74: 0)
      stack_show<int> (I=@0x7fffffffdab4: 1)
    fibnacci (i=1)
      stack_show<int> (I=@0x7fffffffdab4: 1)
    stack_show<int> (I=@0x7fffffffdaf4: 2)
  fibnacci (i=3)
    fibnacci (i=2)
      fibnacci (i=1)
        stack_show<int> (I=@0x7fffffffda74: 1)
      fibnacci (i=0)
        stack_show<int> (I=@0x7fffffffda74: 0)
      stack_show<int> (I=@0x7fffffffdab4: 1)
    fibnacci (i=1)
      stack_show<int> (I=@0x7fffffffdab4: 1)
    stack_show<int> (I=@0x7fffffffdaf4: 2)
          0x0000555555554b84 in _fini ()
<<< end collecting of test case...

```
