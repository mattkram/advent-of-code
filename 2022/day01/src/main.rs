
use std::{
    fs::File,
    io::{prelude::*, BufReader},
    path::Path,
};

fn counts_from_file(filename: impl AsRef<Path>) -> Vec<i32> {
    let file = File::open(filename).expect("no such file");
    let buf = BufReader::new(file);
    let mut result: Vec<i32> = Vec::new();

    let mut total = 0;
    for line in buf.lines() {

        match line.unwrap().parse::<i32>() {
            // If we loaded a value, add it to the running sum.
            Ok(value) => total += value,
            Err(_) => {
                // Otherwise, it's a blank line, and we need to move to the next elf.
                result.push(total);
                total = 0;

            },
        };
    }
    result
}

fn solve_part1() -> i32 {
    let counts = counts_from_file("input.txt");
    let max_value =  counts.iter().max().unwrap().clone();
    max_value
}

fn solve_part2() -> i32 {
    let mut counts = counts_from_file("input.txt");
    counts.sort_by(|a, b| b.cmp(a));
    counts[..3].iter().sum()
}

fn main() {
    println!("The answer to part 1 is: {}", solve_part1());
    println!("The answer to part 2 is: {}", solve_part2());
}
