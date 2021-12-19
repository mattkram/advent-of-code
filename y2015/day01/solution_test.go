package main

import (
	"github.com/stretchr/testify/assert"
	"testing"
)

func Test_CalculatePart1(t *testing.T) {
	result := CalculatePart1("(())")
	assert.Equal(t, 0, result)
}
