package main

import (
	"github.com/stretchr/testify/assert"
	"testing"
)

func Test_CalculatePart1(t *testing.T) {
	cases := []struct {
		Input    string
		Expected int
	}{
		{">", 2},
		{"^>v<", 4},
		{"^v^v^v^v^v", 2},
	}

	for _, data := range cases {
		result := CalculatePart1(data.Input)
		assert.Equal(t, data.Expected, result)
	}
}

func Test_CalculatePart2(t *testing.T) {
	cases := []struct {
		Input    string
		Expected int
	}{
		{"^v", 3},
		{"^>v<", 3},
		{"^v^v^v^v^v", 11},
	}

	for _, data := range cases {
		result := CalculatePart2(data.Input)
		assert.Equal(t, data.Expected, result)
	}
}
