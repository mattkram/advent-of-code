
use std::{
    fs::File,
    io::{prelude::*, BufReader},
    collections::HashSet,
};
use std::collections::HashMap;

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


/// Convert the input list to a list of rounds
fn lines_to_priorities(lines: Vec<String>) -> Vec<i32> {
    let mut result: Vec<i32> = Vec::with_capacity(lines.len());
    for line in lines {
        let first_half = &line[..line.len() / 2];

        let second_half = &line[line.len() / 2..];
        println!("{} | {}", first_half, second_half);

        let first_set: HashSet<char> = first_half.chars().collect();
        let second_set: HashSet<char> = second_half.chars().collect();

        let mut intersection = first_set.intersection(&second_set);
        let i = intersection.next().unwrap();

        let actual: u32 = (*i).into();

        let A: u32 = 'A'.into();
        let a: u32 = 'a'.into();

        let priority = if actual > a {
            (actual as i32) - (a as i32) + 1
        } else {
            (actual as i32) - (A as i32) + 27
        };
        println!("{:?} -> {}", i, priority);
        result.push(priority);
    }
    result
}

fn solve_part1() -> i32 {
    let lines = read_file_to_strings("data/day03.txt");
    let priorities = lines_to_priorities(lines);

    priorities.iter().sum()
}

fn solve_part2() -> i32 {
    0
}

fn main() {
    println!("The answer to part 1 is: {}", solve_part1());
    println!("The answer to part 2 is: {}", solve_part2());
}
