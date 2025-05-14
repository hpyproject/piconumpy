
ifeq ($(PYTHON),)
PYTHON := python
endif

ifeq ($(METHOD),)
METHOD := cpython-c-api
endif

bench_full: rm_hpy_py tmp.py tmp_result_julia.txt
	$(PYTHON) tmp.py

tmp.py: bench_array1d.py make_bench_piconumpy.py
	$(PYTHON) make_bench_piconumpy.py

clean:
	transonic -cc bench_array1d.py -f
	rm -f tmp*.py tmp*.txt

tmp_result_julia.txt:
	julia bench.jl > tmp_result_julia.txt

profile: rm_hpy_py tmp.py
	$(PYTHON) profile_piconumpy.py $(METHOD)
	# with gprof2dot and graphviz (command dot)
	gprof2dot -f pstats tmp.pstats | dot -Tpng -o tmp_$(METHOD).png
	eog tmp_$(METHOD).png

bench_hpy: rm_hpy_py
	$(PYTHON) bench_cpy_vs_hpy.py

rm_hpy_py:
	rm -f ../piconumpy/_piconumpy_hpy.py
