use std::cell::RefCell;
use std::collections::HashMap;
use aoc2022;


enum NodeType {
    FILE { size: usize },
    DIRECTORY,
}

struct Node {
    node_type: NodeType,
    parent: Option<Box<Node>>,
    children: RefCell<HashMap<String, Node>>,
}

impl Node {
    fn new(node_type: NodeType) -> Self {
        Node {node_type, parent: None, children: RefCell::new(HashMap::new())}
    }

    fn get_total_size(self) -> i32 {0}
}

fn load_tree(lines: Vec<String>) -> Node {
    let mut root = Node::new(NodeType::DIRECTORY);

    // A reference to the current working directoru
    let mut cwd = &root;

    for line in lines {
        println!("{}", line);
        if line.starts_with("$ cd") {
            let mut s = line.split(" ");
            s.next();  // "$"
            s.next();  // "cd"
            let dir_name = s.next().unwrap();
            println!("  Changing directory to '{}'", dir_name);
            if dir_name == "/" {
                cwd = &root;
            } else if dir_name == ".." {
                cwd = cwd.parent.as_ref().unwrap();
            } else {
                let x = cwd.children.borrow();
                cwd = x.get(dir_name).unwrap();
            }
        } else if line.starts_with("$ ls") {
            // Do nothing
        } else if line.starts_with("dir") {
            let mut s = line.split(" ");
            s.next();  // skip the "dir"
            let dir_name = s.next().unwrap();
            println!("  Creating new directory '{}'", dir_name);
            let mut children = cwd.children;
            children.get_mut().insert(dir_name.to_string(), Node::new(NodeType::DIRECTORY));
        } else {
            // It's a file
            let mut s = line.split(" ");
            let size: usize = s.next().unwrap().parse().unwrap();
            let filename = s.next().unwrap();
            println!("  Creating new file '{}' with size {}", filename, size);
        }

    }
    root
}

fn solve_part1() -> i32 {
    let lines = aoc2022::read_file_to_strings("data/day07.txt");
    let root = load_tree(lines);
    root.get_total_size()
}

fn solve_part2() -> i32 {
    0
}

fn main() {
    println!("The answer to part 1 is: {}", solve_part1());
    println!("The answer to part 2 is: {}", solve_part2());
}
