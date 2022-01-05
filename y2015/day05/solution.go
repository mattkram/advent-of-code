package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
	"path/filepath"
	"strings"
)

// IsNice1 returns true if the input string is nice, false otherwise.
// We first check for disallowed pairs of letters. Then we iterate
// through the characters, counting vowels and ensuring at least one
// duplicate letter.
func IsNice1(input string) bool {

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

// IsNice2 returns true if the input string is nice, false otherwise.
// We first check for pairs of letters. We store each pair, and then if we
// see it again two characters or more later, we have the necessary repeat.
// Then we check for at least one case where a letter is sandwiched between
// two others, which are identical.
func IsNice2(input string) bool {
	runes := []rune(input)
	pairs := make(map[string]int)

	hasRepeat := false
	for i := range runes[:len(runes)-1] {
		key := string(runes[i]) + string(runes[i+1])
		idx, ok := pairs[key]
		if !ok {
			// On first occurrence of pair, add to the map
			pairs[key] = i
		} else if i >= idx+2 {
			// Check for overlap
			hasRepeat = true
			break
		}
	}

	hasSandwichedLetter := false
	for i := range runes[:len(runes)-2] {
		if runes[i] == runes[i+2] {
			hasSandwichedLetter = true
			break
		}
	}

	return hasRepeat && hasSandwichedLetter
}

// Calculate simply iterates through each line and sums the number of nice strings.
func Calculate(lines []string, niceFunc func(string) bool) int {
	s := 0
	for _, line := range lines {
		if niceFunc(line) {
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

	fmt.Printf("Solution to part 1: %d\n", Calculate(lines, IsNice1))
	fmt.Printf("Solution to part 2: %d\n", Calculate(lines, IsNice2))
}
