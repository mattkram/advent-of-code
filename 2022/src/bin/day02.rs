
use std::{
    fs::File,
    io::{prelude::*, BufReader},
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

fn solve_part1() -> i32 {
    let lines = read_file_to_strings("data/day02.txt");
    for line in lines {
        println!("\"{}\"", line);
    }
    0
}

fn solve_part2() -> i32 {
    0
}

fn main() {
    println!("The answer to part 1 is: {}", solve_part1());
    println!("The answer to part 2 is: {}", solve_part2());
}
