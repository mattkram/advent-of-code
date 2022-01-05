package main

import (
	"github.com/stretchr/testify/assert"
	"testing"
)

func Test_IsNice1(t *testing.T) {
	cases := []struct {
		Input    string
		Expected bool
	}{
		{"ugknbfddgicrmopn", true},
		{"aaa", true},
		{"jchzalrnumimnmhp", false},
		{"haegwjzuvuyypxyu", false},
		{"dvszwmarrgswjxmb", false},
	}

	for _, data := range cases {
		result := IsNice1(data.Input)
		assert.Equal(t, data.Expected, result)
	}
}

func Test_IsNice2(t *testing.T) {
	cases := []struct {
		Input    string
		Expected bool
	}{
		{"qjhvhtzxzqqjkmpb", true},
		{"xxyxx", true},
		{"uurcxstgmygtbstg", false},
		{"ieodomkazucvgmuy", false},
		{"aaaxyxy", true},
	}

	for _, data := range cases {
		result := IsNice2(data.Input)
		assert.Equal(t, data.Expected, result)
	}
}
