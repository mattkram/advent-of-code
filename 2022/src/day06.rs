use std::collections::HashSet;
use aoc2022;


fn find_packet(signal: &String, length: usize) -> i32 {
    for (i, _) in signal.chars().enumerate() {
        // We do a look-forward because it's simpler than ensuring we consider at least 4 chars.
        let packet_candidate = &signal[i..i+length];
        let unique: HashSet<char> = HashSet::from_iter(packet_candidate.chars());
        if unique.iter().count() == length {
            return (i + length).try_into().unwrap();
        }
    }
    panic!("Never found the packet")
}

fn solve_part1() -> i32 {
    let lines = aoc2022::read_file_to_strings("data/day06.txt");
    let signal = lines.first().unwrap();
    let start = find_packet(&signal, 4);
    start
}

fn solve_part2() -> i32 {
    let lines = aoc2022::read_file_to_strings("data/day06.txt");
    let signal = lines.first().unwrap();
    let start = find_packet(&signal, 14);
    start
}

fn main() {
    println!("The answer to part 1 is: {}", solve_part1());
    println!("The answer to part 2 is: {}", solve_part2());
}
