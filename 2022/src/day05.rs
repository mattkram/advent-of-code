use std::borrow::Borrow;
use std::cell::RefCell;
use std::collections::{HashMap, HashSet};
use aoc2022;

struct Move {
    count: i32,
    from: i32,
    to: i32,
}

fn lines_to_moves(lines: Vec<String>) -> Vec<Move> {
    let mut result = Vec::new();
    for line in lines {
        if line.starts_with("move") {
            let mut split = line.split(" ");
            split.next();
            let count= split.next().unwrap().parse::<i32>().unwrap();
            split.next();
            let from = split.next().unwrap().parse::<i32>().unwrap();
            split.next();
            let to = split.next().unwrap().parse::<i32>().unwrap();
            result.push(Move { count, from, to });
        }
    }
    result
}

fn get_stacks() -> HashMap<i32, RefCell<Vec<char>>> {
    let mut map = HashMap::new();
    // TODO: This is manual and hacky :)
    map.insert(1, RefCell::from(vec!['B', 'V', 'S', 'N', 'T', 'C', 'H', 'Q']));
    map.insert(2, RefCell::from(vec!['W', 'D', 'B', 'G']));
    map.insert(3, RefCell::from(vec!['F', 'W', 'R', 'T', 'S', 'Q', 'B']));
    map.insert(4, RefCell::from(vec!['L', 'G', 'W', 'S', 'Z', 'J', 'D', 'N']));
    map.insert(5, RefCell::from(vec!['M', 'P', 'D', 'V', 'F']));
    map.insert(6, RefCell::from(vec!['F', 'W', 'J']));
    map.insert(7, RefCell::from(vec!['L', 'N', 'Q', 'B', 'J', 'V']));
    map.insert(8, RefCell::from(vec!['G', 'T', 'R', 'C', 'J', 'Q', 'S', 'N']));
    map.insert(9, RefCell::from(vec!['J', 'S', 'Q', 'C', 'W', 'D', 'M']));
    map
}

fn perform_moves(stacks: HashMap<i32, RefCell<Vec<char>>>, moves: Vec<Move>, many: bool) -> HashMap<i32, RefCell<Vec<char>>>{
    for m in moves {
        println!("move {} from {} to {}", m.count, m.from, m.to);
        let mut from_stack = stacks.get(&m.from).unwrap().borrow_mut();
        let mut to_stack = stacks.get(&m.to).unwrap().borrow_mut();
        if !many {
            for _ in 0..m.count {
                to_stack.push(from_stack.pop().unwrap());
            }
        } else {
            // Part 2
            let mut tmp_stack: Vec<char> = Vec::new();
            for _ in 0..m.count {
                tmp_stack.push(from_stack.pop().unwrap());
            }
            for val in tmp_stack.iter().rev() {
                to_stack.push(*val);
            }
        }
    }
    stacks
}

fn solve_part1() -> String {
    let lines = aoc2022::read_file_to_strings("data/day05.txt");
    let moves = lines_to_moves(lines);
    let mut stacks = get_stacks();
    let stacks = perform_moves(stacks, moves, false);

    for (k, val) in &stacks {
        println!("{}: {}", k, val.borrow().last().unwrap());
    }

    String::from("Hello")
}

fn solve_part2() -> String {
    let lines = aoc2022::read_file_to_strings("data/day05.txt");
    let moves = lines_to_moves(lines);
    let mut stacks = get_stacks();
    let stacks = perform_moves(stacks, moves, true);

    for (k, val) in &stacks {
        println!("{}: {}", k, val.borrow().last().unwrap());
    }

    String::from("World")
}

fn main() {
    println!("The answer to part 1 is: {}", solve_part1());
    println!("The answer to part 2 is: {}", solve_part2());
}
