package main

import (
	"github.com/stretchr/testify/assert"
	"testing"
)

func Test_Calculate(t *testing.T) {
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
		result := IsNice(data.Input)
		assert.Equal(t, data.Expected, result)
	}
}
