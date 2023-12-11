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

    key, destination = "", ""
    for line in line_iter:
        if not line.strip():
            continue

        if m := re.match(r"(\w+)-to-(\w+) map:", line.strip()):
            key, destination = m.group(1), m.group(2)
            mapping[key]["destination"] = destination
            mapping[key]["submap"] = {}

        else:
            dest_start, source_start, range_len = [int(s) for s in line.split()]
            if "maps" not in mapping[key]:
                mapping[key]["maps"] = []
            mapping[key]["maps"].append((dest_start, source_start, range_len))

    return seeds_to_plant, dict(mapping)


def apply_maps_to_range(range_in, maps):
    splits = {range_in}  # Ranges that don't need to have a map applied
    ranges_out = set()  # Complete set of all ranges, with and without maps applied

    for m in maps:
        dest_start, source_start, range_len = m

        # The start and end of the map
        map_st, map_end = source_start, source_start + range_len - 1

        # The delta to add if a subrange matches the map range
        diff = dest_start - source_start

        # Make a copy so we can mutate the original
        for rng_st, rng_end in set(splits):
            tmp_rng = (rng_st, rng_end)

            if map_st <= rng_st <= rng_end <= map_end:
                # Map completely overlaps the range, remove it from the splits set
                # and apply the map.
                splits.remove((rng_st, rng_end))
                ranges_out.add((rng_st + diff, rng_end + diff))
            elif rng_st <= map_st <= map_end <= rng_end:
                # Range completely overlaps the range, we need to split it three-ways
                ranges_out.add((map_st + diff, map_end + diff))
                splits.remove(tmp_rng)
                splits.add((rng_st, map_st - 1))
                splits.add((map_end + 1, rng_end))
            elif rng_st <= map_end <= rng_end:
                # Partial overlap left
                # Apply the map to the part inside the range
                ranges_out.add((rng_st + diff, map_end + diff))

                # Remove original range
                # Split off part outside the range, don't add a delta
                splits.remove(tmp_rng)
                splits.add((map_end + 1, rng_end))
            elif rng_st <= map_st <= rng_end:
                # Partial overlap right
                # Apply the map to the part inside the range
                ranges_out.add((map_st + diff, rng_end + diff))

                # Remove original range
                # Split off part outside the range, don't add a delta
                splits.remove(tmp_rng)
                splits.add((rng_st, map_st - 1))
            else:
                # No overlap, skipping
                pass

    # Anything left in the splits, add to the result as-is
    for s in splits:
        ranges_out.add(s)

    return ranges_out


def apply_maps(ranges, maps):
    """Apply a series of maps to a set of ranges, returning the modified ranges"""
    ranges_out = set()

    for rng in ranges:
        new_ranges = apply_maps_to_range(rng, maps)
        ranges_out.update(new_ranges)

    return ranges_out


def calculate(input_str: str, ranges: bool = False) -> int:
    seeds, mapping = parse(input_str)  # noqa: F841

    if not ranges:
        # A list of individual seeds is just a set of length-one ranges
        seeds = {(i, i) for i in seeds}
    else:
        new_seeds = []
        num_pairs = len(seeds) // 2
        for pair in range(num_pairs):
            i = 2 * pair
            r = (seeds[i], seeds[i] + seeds[i + 1] - 1)
            new_seeds.append(r)
        seeds = set(new_seeds)

    destination = "seed"
    while d := mapping.get(destination):
        destination = d["destination"]
        seeds = apply_maps(seeds, d["maps"])

    return min(seeds)[0]


def main() -> None:
    with INPUTS_FILE.open() as fp:
        input_str = fp.read()
        print(f"The answer to part 1 is {calculate(input_str)}")
        print(f"The answer to part 2 is {calculate(input_str)}")


if __name__ == "__main__":
    main()
