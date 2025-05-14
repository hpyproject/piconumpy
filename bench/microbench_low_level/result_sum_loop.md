# Microbenchmark sum_loop

We measure the performance for this function:

```python
def sum_loop(arr):
    result = 0.0
    for value in arr:
        result += value
    return result
```

One can run the benchmarks with `make bench_sum_loop`.

With PyPy3.7, I get:

```
bench sum_loop
hostname: voyage
{'cache_tag': 'pypy37',
 'version': sys.pypy_version_info(major=7, minor=3, micro=7, releaselevel='final', serial=0)}
list                          : 2.35e-05 s (  1.8 * Julia)
piconumpy.purepy              : 2.60e-05 s (  2.0 * Julia)
numpy                         : 8.97e-03 s (677.0 * Julia)
piconumpy.hpy                 : 3.73e-04 s ( 28.2 * Julia)
piconumpy.cpython_capi        : 1.75e-03 s (132.4 * Julia)
```

With CPython:

```
bench sum_loop
hostname: voyage
{'cache_tag': 'cpython-39',
 'version': sys.version_info(major=3, minor=9, micro=7, releaselevel='final', serial=0)}
list                          : 3.65e-04 s ( 27.5 * Julia)
piconumpy.purepy              : 2.17e-03 s (164.1 * Julia)
numpy                         : 1.09e-03 s ( 82.2 * Julia)
piconumpy.hpy                 : 7.39e-04 s ( 55.8 * Julia)
piconumpy.cpython_capi        : 5.07e-04 s ( 38.3 * Julia)
```

With Python 3.8.5 (GraalVM CE Native 21.3.0)

```
bench sum_loop
hostname: voyage
{'cache_tag': 'graalpython-38',
 'version': sys.version_info(major=3, minor=8, micro=5, releaselevel='alpha', serial=0)}
list                          : 1.92e-05 s (  1.4 * Julia)
piconumpy.purepy              : 3.61e-05 s (  2.7 * Julia)
numpy                         : ImportError numpy
piconumpy.hpy                 : 5.03e-04 s ( 38.0 * Julia)
piconumpy.cpython_capi        : 2.90e-03 s (219.1 * Julia)
```

## Summary

- PyPy is fast with list (1.3 * Julia, same order of magnitude than with Julia)
and as fast for a piconumpy array based on a list ("piconumpy.purepy", zero
cost abstraction!)

- Numpy and _piconumpy_cpython_capi are both much slower with PyPy than with
Cpython. We can guess that the Numpy port to HPy would fix that.

- piconumpy_hpy is a bit faster with PyPy (19 * Julia) than with CPython (40 *
Julia), however, we see that PyPy does not strongly accelerate piconumpy_hpy
(19 * Julia, 14 * piconumpy_list).

## Traces PyPy `sum_loop`

### List

```
+557: label(p0, p1, p6, p9, f35, f30, p15, p22, p26, i32, i27, p29, descr=TargetToken(140447503809120))
debug_merge_point(0, 0, 'sum_loop;bench.py:23-25~#10 FOR_ITER')
+606: i44 = uint_ge(i32, i27)
guard_false(i44, descr=<Guard0x7fbc7b939a00>) [p0, p6, p9, p15, p1, i32, i27, i44, p26, f30, f35]
+615: f45 = getarrayitem_gc_f(p29, i32, descr=<ArrayF 8>)
+622: i47 = int_add(i32, 1)
debug_merge_point(0, 0, 'sum_loop;bench.py:23-25~#12 STORE_FAST')
debug_merge_point(0, 0, 'sum_loop;bench.py:23-26~#14 LOAD_FAST')
debug_merge_point(0, 0, 'sum_loop;bench.py:23-26~#16 LOAD_FAST')
debug_merge_point(0, 0, 'sum_loop;bench.py:23-26~#18 INPLACE_ADD')
+626: f48 = float_add(f35, f45)
debug_merge_point(0, 0, 'sum_loop;bench.py:23-26~#20 STORE_FAST')
debug_merge_point(0, 0, 'sum_loop;bench.py:23-26~#22 JUMP_ABSOLUTE')
+630: setfield_gc(p15, i47, descr=<FieldS pypy.objspace.std.iterobject.W_AbstractSeqIterObject.inst_index 8>)
+634: guard_not_invalidated(descr=<Guard0x7fbc7b939a60>) [p0, p6, p9, p15, p1, f45, f48, None, None]
+634: i51 = getfield_raw_i(140447672379264, descr=<FieldS pypysig_long_struct.c_value 0>)
+647: i53 = int_sub(i51, 1)
+651: setfield_raw(140447672379264, i53, descr=<FieldS pypysig_long_struct.c_value 0>)
+654: i56 = int_lt(i53, 0)
+658: guard_false(i56, descr=<Guard0x7fbc7b939ac0>) [p0, p6, p9, p15, p1, i53, f45, f48, None, None]
debug_merge_point(0, 0, 'sum_loop;bench.py:23-25~#10 FOR_ITER')
+664: i57 = arraylen_gc(p29, descr=<ArrayF 8>)
+664: jump(p0, p1, p6, p9, f48, f45, p15, p22, p26, i47, i27, p29, descr=TargetToken(140447503809120))
```

### piconumpy purepy (based on list)

```
+705: label(p0, p1, p6, p9, f53, f46, p15, p22, i49, p29, p38, p42, i43, p45, descr=TargetToken(139748702723776))
debug_merge_point(0, 0, 'sum_loop;bench.py:23-25~#10 FOR_ITER')
+760: guard_not_invalidated(descr=<Guard0x7f19c7c97d60>) [p0, p6, p9, p15, p1, p22, i49, f46, f53]
+760: p62 = force_token()
+760: enter_portal_frame(21, 28364)
debug_merge_point(1, 1, '__getitem__;/home/pierre/Dev/piconumpy/piconumpy/purepy.py:27-28~#0 LOAD_FAST')
debug_merge_point(1, 1, '__getitem__;/home/pierre/Dev/piconumpy/piconumpy/purepy.py:27-28~#2 LOAD_ATTR')
debug_merge_point(1, 1, '__getitem__;/home/pierre/Dev/piconumpy/piconumpy/purepy.py:27-28~#4 LOAD_FAST')
debug_merge_point(1, 1, '__getitem__;/home/pierre/Dev/piconumpy/piconumpy/purepy.py:27-28~#6 BINARY_SUBSCR')
+760: i65 = uint_ge(i49, i43)
+763: guard_false(i65, descr=<Guard0x7f19ba0b44a0>) [p0, p6, p9, p15, p1, p22, i49, f46, f53]
+769: f66 = getarrayitem_gc_f(p45, i49, descr=<ArrayF 8>)
debug_merge_point(1, 1, '__getitem__;/home/pierre/Dev/piconumpy/piconumpy/purepy.py:27-28~#8 RETURN_VALUE')
+776: leave_portal_frame(21)
+776: i69 = int_add(i49, 1)
debug_merge_point(0, 0, 'sum_loop;bench.py:23-25~#12 STORE_FAST')
debug_merge_point(0, 0, 'sum_loop;bench.py:23-26~#14 LOAD_FAST')
debug_merge_point(0, 0, 'sum_loop;bench.py:23-26~#16 LOAD_FAST')
debug_merge_point(0, 0, 'sum_loop;bench.py:23-26~#18 INPLACE_ADD')
+780: f70 = float_add(f53, f66)
debug_merge_point(0, 0, 'sum_loop;bench.py:23-26~#20 STORE_FAST')
debug_merge_point(0, 0, 'sum_loop;bench.py:23-26~#22 JUMP_ABSOLUTE')
+784: i72 = getfield_raw_i(139748871243648, descr=<FieldS pypysig_long_struct.c_value 0>)
+797: i74 = int_sub(i72, 3)
+801: setfield_raw(139748871243648, i74, descr=<FieldS pypysig_long_struct.c_value 0>)
+804: setfield_gc(p15, i69, descr=<FieldS pypy.objspace.std.iterobject.W_AbstractSeqIterObject.inst_index 8>)
+808: i77 = int_lt(i74, 0)
+812: guard_false(i77, descr=<Guard0x7f19c7c97dc0>) [p0, p6, p9, p15, p1, i74, f66, f70, None, None, None]
debug_merge_point(0, 0, 'sum_loop;bench.py:23-25~#10 FOR_ITER')
+818: i78 = arraylen_gc(p45, descr=<ArrayF 8>)
+818: jump(p0, p1, p6, p9, f70, f66, p15, p22, i69, p29, p38, p42, i43, p45, descr=TargetToken(139748702723776))
```

### piconumpy hpy

```
+1339: label(p0, p1, p6, p9, f73, p63, p15, i68, p62, descr=TargetToken(139865876151520))
debug_merge_point(0, 0, 'sum_loop;bench.py:23-25~#10 FOR_ITER')
+1352: p82 = getfield_gc_r(p15, descr=<FieldP pypy.objspace.std.iterobject.W_AbstractSeqIterObject.inst_w_seq 16>)
+1356: guard_nonnull_class(p82, 139866025815200, descr=<Guard0x7f350fde1a60>) [p0, p6, p9, p63, p15, p1, p82, f73]
+1376: p84 = getfield_gc_r(p82, descr=<FieldP pypy.interpreter.typedef.W_HPyObjectUserDictWeakrefable.inst_map 16>)
+1387: guard_value(p84, ConstPtr(ptr85), descr=<Guard0x7f35021fe0b0>) [p0, p6, p9, p63, p15, p1, p82, f73]
+1396: guard_not_invalidated(descr=<Guard0x7f35021fe0f8>) [p0, p6, p9, p63, p15, p1, p82, f73]
+1403: p87 = getfield_gc_r(ConstPtr(ptr86), descr=<FieldP pypy.module._hpy_universal.interp_slot.W_SlotWrapper.inst_w_objclass 32>)
+1414: guard_value(p87, ConstPtr(ptr88), descr=<Guard0x7f350fde1ac0>) [p0, p6, p9, p63, p15, p1, p82, f73]
+1423: i90 = getfield_gc_i(ConstPtr(ptr89), descr=<FieldU pypy.module._hpy_universal.interp_slot.W_SlotWrapper.inst_cfuncptr 8>)
+1427: i92 = int_lt(i68, 0)
+1431: guard_false(i92, descr=<Guard0x7f35021fe140>) [p0, p6, p9, p63, p15, p1, p82, f73]
+1444: i94 = getfield_gc_i(ConstPtr(ptr93), descr=<FieldS list.length 8>)
+1448: i95 = int_is_zero(i94)
+1451: guard_false(i95, descr=<Guard0x7f35021fe188>) [p0, p6, p9, p63, p15, p1, p82, f73]
+1457: i97 = int_sub(i94, 1)
+1461: p99 = getfield_gc_r(ConstPtr(ptr98), descr=<FieldP list.items 16>)
+1465: i100 = getarrayitem_gc_i(p99, i97, descr=<ArrayS 8>)
+1470: i101 = arraylen_gc(p99, descr=<ArrayS 8>)
+1474: i103 = int_rshift(i101, 1)
+1477: i105 = int_sub(i103, 5)
+1481: i106 = int_lt(i97, i105)
+1484: cond_call(i106, ConstClass(_ll_list_resize_hint_really_look_inside_iff__listPtr_Signed_Bool), ConstPtr(ptr108), i97, 0, descr=<Callv 0 rii EF=5>)
+1490: guard_no_exception(descr=<Guard0x7f350fde1b20>) [p0, p6, p9, p63, p15, p1, i68, i90, i100, p82, i97, f73]
+1490: setfield_gc(ConstPtr(ptr110), i97, descr=<FieldS list.length 8>)
+1494: i112 = int_lt(i100, 0)
+1498: guard_false(i112, descr=<Guard0x7f350fde1b80>) [p0, p6, p9, p63, p15, p1, i68, i90, i100, p82, f73]
+1522: setarrayitem_gc(p62, i100, p82, descr=<ArrayP 8>)
+1527: p113 = force_token()
+1548: setfield_gc(p0, p113, descr=<FieldP pypy.interpreter.pyframe.PyFrame.vable_token 8>)
+1552: i115 = call_may_force_i(i90, 139866044538144, i100, i68, descr=<Calli 8 iii EF=7>)
+1663: guard_not_forced(descr=<Guard0x7f350fdfabe8>) [p0, p6, p9, p63, p15, p1, i100, i115, i68, p82, f73]
+1674: guard_no_exception(descr=<Guard0x7f35021fe1d0>) [p0, p6, p9, p63, p15, p1, i100, i115, i68, p82, f73]
+1688: call_n(ConstClass(close), i100, descr=<Callv 0 i EF=5>)
+1754: guard_no_exception(descr=<Guard0x7f350fde1be0>) [p0, p6, p9, p63, p15, p1, i115, i68, p82, f73]
+1768: i117 = int_is_true(i115)
+1771: guard_true(i117, descr=<Guard0x7f35021fe218>) [p0, p6, p9, p63, p15, p1, i115, i68, p82, f73]
+1784: p119 = getfield_gc_r(ConstPtr(ptr118), descr=<FieldP list.items 16>)
+1788: p120 = getarrayitem_gc_r(p119, i115, descr=<ArrayP 8>)
+1793: call_n(ConstClass(close), i115, descr=<Callv 0 i EF=5>)
+1866: guard_no_exception(descr=<Guard0x7f350fde1c40>) [p0, p6, p9, p63, p15, p1, p120, i68, p82, f73]
+1880: guard_nonnull_class(p120, ConstClass(W_FloatObject), descr=<Guard0x7f350fde1ca0>) [p0, p6, p9, p63, p15, p1, p120, i68, p82, f73]
+1907: i123 = getfield_gc_i(p15, descr=<FieldS pypy.objspace.std.iterobject.W_AbstractSeqIterObject.inst_index 8>)
+1918: i125 = int_add(i123, 1)
debug_merge_point(0, 0, 'sum_loop;bench.py:23-25~#12 STORE_FAST')
debug_merge_point(0, 0, 'sum_loop;bench.py:23-26~#14 LOAD_FAST')
debug_merge_point(0, 0, 'sum_loop;bench.py:23-26~#16 LOAD_FAST')
debug_merge_point(0, 0, 'sum_loop;bench.py:23-26~#18 INPLACE_ADD')
+1923: setfield_gc(p15, i125, descr=<FieldS pypy.objspace.std.iterobject.W_AbstractSeqIterObject.inst_index 8>)
+1927: f126 = getfield_gc_f(p120, descr=<FieldF pypy.objspace.std.floatobject.W_FloatObject.inst_floatval 8 pure>)
+1933: f127 = float_add(f73, f126)
debug_merge_point(0, 0, 'sum_loop;bench.py:23-26~#20 STORE_FAST')
debug_merge_point(0, 0, 'sum_loop;bench.py:23-26~#22 JUMP_ABSOLUTE')
+1947: guard_not_invalidated(descr=<Guard0x7f350fde1d00>) [p0, p6, p9, p120, p15, p1, f127, None, None, None]
+1947: i129 = getfield_raw_i(139866044675968, descr=<FieldS pypysig_long_struct.c_value 0>)
+1960: i131 = int_sub(i129, 3)
+1964: setfield_raw(139866044675968, i131, descr=<FieldS pypysig_long_struct.c_value 0>)
+1967: i134 = int_lt(i131, 0)
+1971: guard_false(i134, descr=<Guard0x7f350fde1d60>) [p0, p6, p9, p120, p15, p1, i131, f127, None, None, None]
debug_merge_point(0, 0, 'sum_loop;bench.py:23-25~#10 FOR_ITER')
+1977: i135 = arraylen_gc(p119, descr=<ArrayP 8>)
+1977: jump(p0, p1, p6, p9, f127, p120, p15, i125, p119, descr=TargetToken(139865876151520))
```
