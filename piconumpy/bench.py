from transonic.util import timeit


def timeit_verbose(
    stmt,
    setup="pass",
    total_duration=2,
    globals=None,
    norm=None,
    name=None,
    print_time=False,
    max_length_name=33,
):
    if name is None:
        name = stmt.split("(")[0]

    fmt_name = f"{{:{max_length_name}s}}"
    name = fmt_name.format(name)
    print(f"{name}:", end="", flush=True)

    result = timeit(
        stmt, setup=setup, total_duration=total_duration, globals=globals
    )
    if norm is None:
        norm = result
        norm_given = False
    else:
        norm_given = True

    if print_time:
        raw_time = f" = {result:7.3g} s"
    else:
        raw_time = ""

    print(f" {result/norm:5.3g} * norm{raw_time}")
    if not norm_given and not print_time:
        print(f"norm = {norm:5.3g} s")

    return result
