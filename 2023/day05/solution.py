import re
from collections import defaultdict
from pathlib import Path

INPUTS_FILE = Path(__file__).parent / "input.txt"


def parse(input_str: str) -> None:
    mapping = defaultdict(dict)

    def get_line():
        lines = [s.strip() for s in input_str.splitlines() if s.strip()]
        for line in lines:
            if line.strip():
                yield line

    line_iter = get_line()

    seeds_to_plant = [int(s) for s in next(line_iter).removeprefix("seeds:").split()]
    print(seeds_to_plant)

    key, destination = "", ""
    for line in line_iter:
        if not line.strip():
            continue

        if m := re.match(r"(\w+)-to-(\w+) map:", line.strip()):
            print(m.group(1), m.group(2))
            key, destination = m.group(1), m.group(2)
            mapping[key]["destination"] = destination
            mapping[key]["submap"] = {}

        else:
            dest_start, source_start, range_len = [int(s) for s in line.split()]
            # def f(v):
            #     diff = v - source_start
            #     if diff <= range_len:
            #         return v + (source_start - dest_start)
            #     return v
            # mapping[key]['get'] = f
            if "ranges" not in mapping[key]:
                mapping[key]["ranges"] = []
            mapping[key]["ranges"].append((dest_start, source_start, range_len))
            # for i in range(range_len):
            #     mapping[key]["submap"][source_start + i] = dest_start + i
            pass

    return seeds_to_plant, dict(mapping)


def get_value(v, ranges):
    for dest_start, source_start, range_len in ranges:
        diff = v - source_start
        if 0 <= diff <= range_len:
            return dest_start + diff
    return v


def calculate(input_str: str) -> int:
    seeds, mapping = parse(input_str)  # noqa: F841

    result = 1_000_000_000
    for seed in seeds:
        print(seed)
        destination = "seed"
        val = seed
        # msg = f"{destination} {val}"
        # print(msg)

        while d := mapping.get(destination):
            destination = d["destination"]
            # s = d['submap']
            # val = s.get(val, val)
            val = get_value(val, d["ranges"])
            # msg = f"{destination} {val}"
            # print(msg)

        # print(f"Final value: {val}")
        result = min(val, result)

    return result


def main() -> None:
    with INPUTS_FILE.open() as fp:
        input_str = fp.read()
        print(f"The answer to part 1 is {calculate(input_str)}")
        print(f"The answer to part 2 is {calculate(input_str)}")


if __name__ == "__main__":
    main()
