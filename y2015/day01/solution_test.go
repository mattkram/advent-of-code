package main

import (
	"github.com/stretchr/testify/assert"
	"testing"
)

func Test_cases(t *testing.T) {
	result := Calculate("(())")
	assert.Equal(t, 1, result)
}
