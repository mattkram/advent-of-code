
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


#[derive(Eq, PartialEq, Clone)]
enum Move {
    ROCK,
    PAPER,
    SCISSORS,
}

#[derive(Eq, PartialEq)]
struct Round {
    you: Move,
    them: Move,
}

enum Part {
    ONE, TWO,
}

/// Convert the input list to a list of rounds
fn lines_to_rounds(lines: Vec<String>, part: Part) -> Vec<Round> {
    let mut result: Vec<Round> = Vec::with_capacity(lines.len());
    for line in lines {
        let mut split = line.split(" ");
        let their_move = match split.next().unwrap() {
            "A" => Move::ROCK,
            "B" => Move::PAPER,
            "C" => Move::SCISSORS,
            _ => panic!("Unknown move")
        };

        let your_move = match part {
            Part::ONE => match split.next().unwrap() {
                "X" => Move::ROCK,
                "Y" => Move::PAPER,
                "Z" => Move::SCISSORS,
                _ => panic!("Unknown move"),
            }
            Part::TWO => match split.next().unwrap() {
                "X" => { // you need to lose
                    match their_move {
                        Move::ROCK => Move::SCISSORS,
                        Move::PAPER => Move::ROCK,
                        Move::SCISSORS => Move::PAPER,
                    }
                },
                "Y" => // draw
                    their_move.clone(),
                "Z" => // you need to win
                    match their_move {
                        Move::ROCK => Move::PAPER,
                        Move::PAPER => Move::SCISSORS,
                        Move::SCISSORS => Move::ROCK,
                    },
                _ => panic!("Unknown move")
            }
        };

        let game = Round {them:their_move, you: your_move};
        result.push(game);
    }
    result
}

fn rounds_to_scores(rounds: Vec<Round>) -> Vec<i32> {
    //The score for a single round is the score for the shape you selected
    // (1 for Rock, 2 for Paper, and 3 for Scissors) plus the score for the
    // outcome of the round (0 if you lost, 3 if the round was a draw, and
    // 6 if you won).
    let mut result: Vec<i32> = Vec::with_capacity(rounds.len());

    for round in rounds {
        let mut score = match round.you {
            Move::ROCK => 1,
            Move::PAPER => 2,
            Move::SCISSORS => 3,
        };

        if round.them == round.you {
            score += 3;
        } else if
            round == (Round{you: Move::ROCK, them: Move::SCISSORS}) ||
            round == (Round{you: Move::PAPER, them: Move::ROCK}) ||
            round == (Round{you: Move::SCISSORS, them: Move::PAPER}){
            score += 6;
        }
        result.push(score)
    }
    result
}

fn solve_part1() -> i32 {
    let lines = read_file_to_strings("data/day02.txt");
    let rounds = lines_to_rounds(lines, Part::ONE);
    let scores = rounds_to_scores(rounds);

    scores.iter().sum()
}

fn solve_part2() -> i32 {
    let lines = read_file_to_strings("data/day02.txt");
    let rounds = lines_to_rounds(lines, Part::TWO);
    let scores = rounds_to_scores(rounds);

    scores.iter().sum()
}

fn main() {
    println!("The answer to part 1 is: {}", solve_part1());
    println!("The answer to part 2 is: {}", solve_part2());
}
