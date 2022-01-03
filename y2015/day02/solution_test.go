package main

import (
	"github.com/stretchr/testify/assert"
	"testing"
)

func Test_CalculatePart1(t *testing.T) {
	cases := []struct {
		Input    string
		Expected int
	}{{"2x3x4", 58},
		{"1x1x10", 43},
	}

	for _, data := range cases {
		result := CalculateArea(data.Input)
		assert.Equal(t, data.Expected, result)
	}
}

func Test_CalculatePart2(t *testing.T) {
	cases := []struct {
		Input    string
		Expected int
	}{
		{"2x3x4", 34},
		{"4x2x3", 34},
		{"1x1x10", 14},
	}

	for _, data := range cases {
		result := CalculateRibbonLength(data.Input)
		assert.Equal(t, data.Expected, result)
	}
}
