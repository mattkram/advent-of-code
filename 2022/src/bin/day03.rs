use std::collections::HashSet;
use aoc2022;


/// Convert the input list to a list of common characters between first and second halves.
fn lines_to_common_char(lines: Vec<String>) -> Vec<char> {
    let mut result: Vec<char> = Vec::with_capacity(lines.len());
    for line in lines {
        let first_half = &line[..line.len() / 2];
        let second_half = &line[line.len() / 2..];
        // println!("{} | {}", first_half, second_half);

        let first_set: HashSet<char> = first_half.chars().collect();
        let second_set: HashSet<char> = second_half.chars().collect();

        let intersection = first_set.intersection(&second_set).next().unwrap();
        result.push(*intersection);
    }
    result
}

/// Convert the input list to a list of common characters between each three-line group.
fn lines_to_badges(lines: Vec<String>) -> Vec<char> {
    let num_groups = lines.len() / 3;
    let mut result: Vec<char> = Vec::with_capacity(num_groups);
    for i in 0..num_groups {
        let elf_0: HashSet<char> = (&lines[3*i + 0]).chars().collect();
        let elf_1: HashSet<char> = (&lines[3*i + 1]).chars().collect();
        let elf_2: HashSet<char> = (&lines[3*i + 2]).chars().collect();

        let elves_0_1: HashSet<char> = elf_0.intersection(&elf_1).map(|s| *s).collect();
        let intersection = elves_0_1.intersection(&elf_2).next().unwrap();
        result.push(*intersection);
    }
    result
}

/// Convert a vector of characters into a vector of priorities.
fn chars_to_priorities(chars: Vec<char>) -> Vec<i32> {
    let uppercase_a_ord: u32 = 'A'.into();
    let lowercase_a_ord: u32 = 'a'.into();

    let mut result: Vec<i32> = Vec::with_capacity(chars.len());
    for i in chars {
        let actual: u32 = i as u32;

        let priority = if actual > lowercase_a_ord {
            (actual as i32) - (lowercase_a_ord as i32) + 1
        } else {
            (actual as i32) - (uppercase_a_ord as i32) + 27
        };
        // println!("{:?} -> {}", i, priority);
        result.push(priority);
    }
    result
}

fn solve_part1() -> i32 {
    let lines = aoc2022::read_file_to_strings("data/day03.txt");
    let common_chars = lines_to_common_char(lines);
    let priorities = chars_to_priorities(common_chars);

    priorities.iter().sum()
}

fn solve_part2() -> i32 {
    let lines = aoc2022::read_file_to_strings("data/day03.txt");
    let common_chars = lines_to_badges(lines);
    let priorities = chars_to_priorities(common_chars);

    priorities.iter().sum()
}

fn main() {
    println!("The answer to part 1 is: {}", solve_part1());
    println!("The answer to part 2 is: {}", solve_part2());
}
