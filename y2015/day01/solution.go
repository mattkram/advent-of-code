package main

import (
	"fmt"
	"os"
	"path/filepath"
)

func CalculatePart1(s string) int {
	sum := 0
	for _, c := range s {
		if c == '(' {
			sum += 1
		} else if c == ')' {
			sum -= 1
		} else if c == '\n' {
		} else {
			panic("Invalid character!")
		}
	}
	return sum

}

func CalculatePart2(s string) int {
	floor := 0
	for i, c := range s {
		if c == '(' {
			floor += 1
		} else if c == ')' {
			floor -= 1
		} else {
			panic("Invalid character!")
		}
		if floor == -1 {
			return i + 1
		}
	}
	panic("Couldn't find floor")

}

func main() {
	filename, _ := filepath.Abs("y2015/day01/input.txt")
	b, err := os.ReadFile(filename)
	if err != nil {
		panic(`Cannot read file`)
	}

	inputString := string(b)
	if len(inputString) == 0 {
		panic("Blank string")
	}

	fmt.Printf("Solution to part 1: %d\n", CalculatePart1(inputString))
	fmt.Printf("Solution to part 2: %d\n", CalculatePart2(inputString))
}
