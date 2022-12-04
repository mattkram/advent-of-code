
use std::{
    fs::File,
    io::{prelude::*, BufReader},
    collections::HashSet,
};

/// Read the contents of a file into a list of strings.
/// Whitespace is trimmed from beginning and end of the string.
/// Empty lines are an empty string.
fn read_file_to_strings(filename: &str) -> Vec<String> {
    let file = File::open(filename).expect(&format!("{} does not exist", filename));
    let buf = BufReader::new(file);
    let mut result: Vec<String> = Vec::new();

    for line in buf.lines() {
        if let Ok(s) = line {
            result.push(String::from(s.trim()));
        }
    }
    result
}

/// Convert a string of format 1-50 into a set of integers, inclusive.
fn range_string_to_set(s: &str) -> HashSet<i32> {
    let mut split = s.split("-");
    let start = split.next().unwrap().parse::<i32>().unwrap();
    let end = split.next().unwrap().parse::<i32>().unwrap();
    HashSet::from_iter(start..=end)
}

/// Convert a string of format 1-50,2-50 into two sets of integers, inclusive
fn string_to_sets(s: String) -> (HashSet<i32>, HashSet<i32>) {
    let mut split = s.split(",");
    let range_1 = split.next().unwrap();
    let range_2 = split.next().unwrap();
    (range_string_to_set(range_1), range_string_to_set(range_2))
}

/// Count the number of input lines corresponding to overlapping ranges.
fn count_overlapping_ranges(lines: Vec<String>) -> i32 {
    let mut result: i32 = 0;

    for line in lines {
        let (set_1, set_2) = string_to_sets(line);
        if set_1.is_subset(&set_2) || set_1.is_superset(&set_2) {
            result += 1;
        }
    }
    result
}

fn solve_part1() -> i32 {
    let lines = read_file_to_strings("data/day04.txt");
    count_overlapping_ranges(lines)
}

fn solve_part2() -> i32 {
    -1
}

fn main() {
    println!("The answer to part 1 is: {}", solve_part1());
    println!("The answer to part 2 is: {}", solve_part2());
}
