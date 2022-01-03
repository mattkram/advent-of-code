package main

import (
	"bufio"
	"fmt"
	"log"
	"math"
	"os"
	"path/filepath"
	"strconv"
	"strings"
)

func CalculateArea(s string) int {
	sum := 0
	dimStrings := strings.Split(s, "x")

	var dims []int

	for _, i := range dimStrings {
		dim, err := strconv.Atoi(i)
		if err != nil {
			panic(err)
		}
		dims = append(dims, dim)
	}

	areas := []int{dims[0] * dims[1],
		dims[0] * dims[2],
		dims[1] * dims[2]}

	minArea := math.MaxInt
	for _, area := range areas {
		sum += 2 * area
		if area < minArea {
			minArea = area
		}
	}
	sum += minArea
	return sum
}

func CalculateRibbonLength(s string) int {
	dimStrings := strings.Split(s, "x")

	var dims []int

	for _, i := range dimStrings {
		dim, err := strconv.Atoi(i)
		if err != nil {
			panic(err)
		}
		dims = append(dims, dim)
	}

	circums := []int{
		2 * (dims[0] + dims[1]),
		2 * (dims[0] + dims[2]),
		2 * (dims[1] + dims[2]),
	}
	volume := dims[0] * dims[1] * dims[2]

	minCircum := math.MaxInt
	for _, circum := range circums {
		if circum < minCircum {
			minCircum = circum
		}
	}
	sum := minCircum + volume
	return sum
}

func CalculatePart1(lines []string) int {
	result := 0
	for _, line := range lines {
		result += CalculateArea(line)
	}
	return result

}

func CalculatePart2(lines []string) int {
	result := 0
	for _, line := range lines {
		result += CalculateRibbonLength(line)
	}
	return result

}

func main() {
	filename, _ := filepath.Abs("y2015/day02/input.txt")
	file, err := os.Open(filename)
	if err != nil {
		log.Fatal(err)
	}
	defer file.Close()

	scanner := bufio.NewScanner(file)
	var lines []string

	for scanner.Scan() {
		lines = append(lines, scanner.Text())
	}

	fmt.Printf("Solution to part 1: %d\n", CalculatePart1(lines))
	fmt.Printf("Solution to part 2: %d\n", CalculatePart2(lines))
}
