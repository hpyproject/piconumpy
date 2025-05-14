# Microbenchmarks low level Python code

We measure the performance for functions containing low level Python code.

- `sum_loop` (command `make bench`): `for value in arr` and summation

- `sum_loop_index` (command `make bench_sum_loop_index`):
  `for index in range(5000)` and summation

- `init_zeros` (command `make bench_init_zeros`): set values to zeros

- `cort` (command `make bench_cort`): normalized cosine similarity measure
  between derivatives

- `board` (command `make bench_board`): few indexing, simple float computations
  with sin/cos and instantiation of a small array.

- `instantiate` (command `make bench_instantiate`): dominated by the
  instantiation/deletion of small arrays of 4 floats.

- `element_wise` (command `make bench_element_wise`): dominated by the
  instantiation/deletion of small arrays of 4 floats and calling element-wise
  operations.

The files result_*.txt contain few results.
