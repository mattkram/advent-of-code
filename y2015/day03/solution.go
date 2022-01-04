package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
	"path/filepath"
)

type Position struct {
	X int
	Y int
}

// CalculatePart1 In part one, we create a mapping to act as a set of all visited positions.
// It does not matter what the value is, so we use a simple boolean. By using a mapping, overlapping
// keys are handled appropriately when we visit the same position twice.
func CalculatePart1(input string) int {
	visited := make(map[Position]bool)

	visited[Position{0, 0}] = true

	position := Position{0, 0}

	for _, c := range input {
		switch c {
		case '>':
			position.X += 1
		case '<':
			position.X -= 1
		case 'v':
			position.Y += 1
		case '^':
			position.Y -= 1
		default:
			panic(fmt.Errorf("Incorrect character: %c", c))
		}
		visited[position] = true
	}
	return len(visited)
}

// CalculatePart2 is the same as previous, however we now must maintain two separate positions and
// alternate which person moves for each instruction.
func CalculatePart2(input string) int {
	visited := make(map[Position]bool)

	visited[Position{0, 0}] = true

	positions := []Position{
		{0, 0},
		{0, 0},
	}

	for i, c := range input {
		position := positions[i%2]

		switch c {
		case '>':
			position.X += 1
		case '<':
			position.X -= 1
		case 'v':
			position.Y += 1
		case '^':
			position.Y -= 1
		default:
			panic(fmt.Errorf("Incorrect character: %c", c))
		}

		positions[i%2] = position
		visited[position] = true
	}
	return len(visited)
}

// ReadLines reads the input file into an array of strings, one per line.
func ReadLines(filename string) []string {
	file, err := os.Open(filename)
	if err != nil {
		log.Fatal(err)
	}
	defer func(file *os.File) {
		_ = file.Close()
	}(file)

	scanner := bufio.NewScanner(file)
	var lines []string

	for scanner.Scan() {
		lines = append(lines, scanner.Text())
	}
	return lines
}

func main() {
	filename, _ := filepath.Abs("y2015/day03/input.txt")
	lines := ReadLines(filename)

	fmt.Printf("Solution to part 1: %d\n", CalculatePart1(lines[0]))
	fmt.Printf("Solution to part 2: %d\n", CalculatePart2(lines[0]))
}
