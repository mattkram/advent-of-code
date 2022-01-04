package main

import (
	"github.com/stretchr/testify/assert"
	"testing"
)

func Test_Calculate(t *testing.T) {
	cases := []struct {
		Input    string
		Expected int
	}{
		{"abcdef", 609043},
		{"pqrstuv", 1048970},
	}

	for _, data := range cases {
		result := Calculate(data.Input, 5)
		assert.Equal(t, data.Expected, result)
	}
}
