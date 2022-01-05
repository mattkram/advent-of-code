package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
	"path/filepath"
	"strings"
)

// IsNice returns true if the input string is nice, false otherwise.
// We first check for disallowed pairs of letters. Then we iterate
// through the characters, counting vowels and ensuring at least one
// duplicate letter.
func IsNice(input string) bool {

	disallowed := []string{
		"ab", "cd", "pq", "xy",
	}
	for _, d := range disallowed {
		if strings.Contains(input, d) {
			return false
		}
	}

	numVowels := 0
	hasDuplicateLetter := false
	for i, c := range input {
		switch c {
		case 'a', 'e', 'i', 'o', 'u':
			numVowels += 1
		}

		if i < len(input)-1 && c == []rune(input)[i+1] {
			hasDuplicateLetter = true
		}
	}

	return numVowels >= 3 && hasDuplicateLetter
}

// CalculatePart1 simply iterates through each line and sums the number of nice strings.
func CalculatePart1(lines []string) int {
	s := 0
	for _, line := range lines {
		if IsNice(line) {
			s += 1
		}
	}
	return s
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
	filename, _ := filepath.Abs("y2015/day05/input.txt")
	lines := ReadLines(filename)

	fmt.Printf("Solution to part 1: %d\n", CalculatePart1(lines))
	//fmt.Printf("Solution to part 2: %d\n", Calculate(lines[0], 6))
}
