
IMPLEMENTATION=$(shell python -c 'import sys; print(sys.implementation.cache_tag)')

.PHONY : clean bench_sum_loop bench_sum_loop_index bench_cort bench_init_zeros bench_instantiate

bench_sum_loop: NAME_BENCH=sum_loop
bench_sum_loop: tmp/sum_loop_julia.txt _bench

bench_sum_loop_index: NAME_BENCH=sum_loop_index
bench_sum_loop_index: tmp/sum_loop_index_julia.txt _bench

bench_cort: NAME_BENCH=cort
bench_cort: tmp/cort_julia.txt _bench

bench_init_zeros: NAME_BENCH=init_zeros
bench_init_zeros: tmp/init_zeros_julia.txt _bench

bench_board: NAME_BENCH=board
bench_board: tmp/board_julia.txt _bench

bench_instantiate: NAME_BENCH=instantiate
bench_instantiate: tmp/instantiate_julia.txt _bench

bench_element_wise: NAME_BENCH=element_wise
bench_element_wise: tmp/element_wise_julia.txt _bench

_bench:
	@echo bench $(NAME_BENCH)
	@python -c "from socket import gethostname as f; print('hostname:', f())"
	@python -c "import sys; from pprint import pprint as p; p({key: sys.implementation.__dict__[key] for key in ('cache_tag', 'version')})"
	@python bench.py list $(NAME_BENCH) | tee tmp/$(NAME_BENCH)_$(IMPLEMENTATION)_list.txt
	@python bench.py purepy $(NAME_BENCH) | tee tmp/$(NAME_BENCH)_$(IMPLEMENTATION)_purepy.txt
	@python bench.py numpy $(NAME_BENCH) | tee tmp/$(NAME_BENCH)_$(IMPLEMENTATION)_numpy.txt
	@python bench.py _piconumpy_hpy $(NAME_BENCH) | tee tmp/$(NAME_BENCH)_$(IMPLEMENTATION)_hpy.txt
	@python bench.py _piconumpy_cpython_capi $(NAME_BENCH) | tee tmp/$(NAME_BENCH)_$(IMPLEMENTATION)_cpy_api.txt

tmp/%_julia.txt: julia/bench_%.jl
	@mkdir -p tmp
	@julia julia/bench_$*.jl > $@

clean:
	rm -rf tmp

produce_traces: tmp/sum_loop_julia.txt
	@mkdir -p tmp
	PYPYLOG=jit-log-opt,jit-summary,jit-backend-counts:tmp/pypylog_list.txt pypy bench.py list
	PYPYLOG=jit-log-opt,jit-summary,jit-backend-counts:tmp/pypylog_piconumpy_list.txt pypy bench.py purepy
	PYPYLOG=jit-log-opt,jit-summary,jit-backend-counts:tmp/pypylog_piconumpy_hpy.txt pypy bench.py _piconumpy_hpy
