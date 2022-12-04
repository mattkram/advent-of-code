use std::{
    fs::File,
    io::{prelude::*, BufReader},
};

/// Read the contents of a file into a list of strings.
/// Whitespace is trimmed from beginning and end of the string.
/// Empty lines are an empty string.
pub fn read_file_to_strings(filename: &str) -> Vec<String> {
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
