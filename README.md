# gdb-stack-trace

## Example

```bash
$ make test-main
$ gdb -ex "source core.py" build/test-main
GNU gdb (Ubuntu 8.1.1-0ubuntu1) 8.1.1
Copyright (C) 2018 Free Software Foundation, Inc.
License GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>
This is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.  Type "show copying"
and "show warranty" for details.
This GDB was configured as "x86_64-linux-gnu".
Type "show configuration" for configuration details.
For bug reporting instructions, please see:
<http://www.gnu.org/software/gdb/bugs/>.
Find the GDB manual and other documentation resources online at:
<http://www.gnu.org/software/gdb/documentation/>.
For help, type "help".
Type "apropos word" to search for commands related to "word"...
Reading symbols from build/test-main...done.
T:['_fini', '_init', '__libc_csu_fini', '__libc_csu_init', 'main', '_start', '_Z8fibnaccii']
W:['_ZNSt6vectorIiSaIiEE9push_backERKi']
>>> beg collecting of test case None...
 >>> beg execution
[Inferior 1 (process 22985) exited normally]
 <<< end execution

            _init (argc=1, argv=0x7fffffffdbf8, envp=0x7fffffffdc08)
0x00005555555549c0 in _start ()
    0x0000555555555880 in __libc_csu_init ()
      0x00005555555548c0 in _init ()
main ()
  fibnacci (i=5)
    fibnacci (i=4)
      fibnacci (i=3)
        fibnacci (i=2)
          fibnacci (i=1)
            vector::push_back (this=0x555555757030 <numbers>, __x=@0x7fffffffd9d4: 1)
          fibnacci (i=0)
            vector::push_back (this=0x555555757030 <numbers>, __x=@0x7fffffffd9d4: 0)
          vector::push_back (this=0x555555757030 <numbers>, __x=@0x7fffffffda14: 1)
        fibnacci (i=1)
          vector::push_back (this=0x555555757030 <numbers>, __x=@0x7fffffffda14: 1)
        vector::push_back (this=0x555555757030 <numbers>, __x=@0x7fffffffda54: 2)
      fibnacci (i=2)
        fibnacci (i=1)
          vector::push_back (this=0x555555757030 <numbers>, __x=@0x7fffffffda14: 1)
        fibnacci (i=0)
          vector::push_back (this=0x555555757030 <numbers>, __x=@0x7fffffffda14: 0)
        vector::push_back (this=0x555555757030 <numbers>, __x=@0x7fffffffda54: 1)
      vector::push_back (this=0x555555757030 <numbers>, __x=@0x7fffffffda94: 3)
    fibnacci (i=3)
      fibnacci (i=2)
        fibnacci (i=1)
          vector::push_back (this=0x555555757030 <numbers>, __x=@0x7fffffffda14: 1)
        fibnacci (i=0)
          vector::push_back (this=0x555555757030 <numbers>, __x=@0x7fffffffda14: 0)
        vector::push_back (this=0x555555757030 <numbers>, __x=@0x7fffffffda54: 1)
      fibnacci (i=1)
        vector::push_back (this=0x555555757030 <numbers>, __x=@0x7fffffffda54: 1)
      vector::push_back (this=0x555555757030 <numbers>, __x=@0x7fffffffda94: 2)
    vector::push_back (this=0x555555757030 <numbers>, __x=@0x7fffffffdad4: 5)
          0x00005555555558f4 in _fini ()
<<< end collecting of test case...

```
