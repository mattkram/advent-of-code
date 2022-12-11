use std::collections::HashSet;
use aoc2022;


fn find_packet(signal: &String) -> i32 {
    for (i, _) in signal.chars().enumerate() {
        // We do a look-forward because it's simpler than ensuring we consider at least 4 chars.
        let next_four = &signal[i..i+4];
        let unique: HashSet<char> = HashSet::from_iter(next_four.chars());
        if unique.iter().count() == 4 {
            return (i + 4).try_into().unwrap();
        }
    }
    panic!("Never found the packet")
}

fn solve_part1() -> i32 {
    let lines = aoc2022::read_file_to_strings("data/day06.txt");
    let signal = lines.first().unwrap();
    let start = find_packet(&signal);
    start
}

fn solve_part2() -> i32 {
    0
}

fn main() {
    println!("The answer to part 1 is: {}", solve_part1());
    println!("The answer to part 2 is: {}", solve_part2());
}
