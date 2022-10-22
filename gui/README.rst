Multiprocessing
===============
+ **Cpu count**
+ **Pool example**

>>> from multiprocessing import cpu_count
>>> [cpu_count()]  #doctest: +ELLIPSIS
[...]

>>> from multiprocessing.pool import Pool

>>> def function(x):
...     return x

>>> with Pool() as pool:
...     results = pool.map(function, range(10))
...     print(results)  #doctest: +ELLIPSIS
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

