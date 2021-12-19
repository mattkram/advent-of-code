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
		} else {
			panic("Invalid character!")
		}
	}
	return sum

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

	fmt.Printf("Solution to part 1: %d", CalculatePart1(inputString))
}
