package main

import (
	"bufio"
	"crypto/md5"
	"encoding/hex"
	"fmt"
	"log"
	"os"
	"path/filepath"
	"strconv"
	"strings"
)

// GetMD5Hash returns the MD5 hash string of an input string
func GetMD5Hash(text string) string {
	hash := md5.Sum([]byte(text))
	return hex.EncodeToString(hash[:])
}

// Calculate iterates from 0 -> infinity until the first `numZeros` characters of the
// hash are zero.
func Calculate(secret string, numZeros int) int {
	prefix := strings.Repeat("0", numZeros)
	for i := 0; ; i += 1 {
		hash := GetMD5Hash(secret + strconv.FormatInt(int64(i), 10))
		if strings.HasPrefix(hash, prefix) {
			return i
		}
	}
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
	filename, _ := filepath.Abs("y2015/day04/input.txt")
	lines := ReadLines(filename)

	fmt.Printf("Solution to part 1: %d\n", Calculate(lines[0], 5))
	fmt.Printf("Solution to part 2: %d\n", Calculate(lines[0], 6))
}
