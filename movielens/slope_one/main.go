package main

import "C"
import (
	"unsafe"

	"gonum.org/v1/gonum/mat"
)

// BuildSlopeOne builds deviation matrix for Slope One collaborative filtering algorithm
//export BuildSlopeOne
func BuildSlopeOne(users []int, movies []int, ratings []int) (C.size_t, *C.float) {
	userSet := make(map[int]bool)
	for _, user := range users {
		userSet[user] = true
	}

	var moviesCount int
	for _, movie := range movies {
		if movie > moviesCount {
			moviesCount = movie
		}
	}
	moviesCount++

	diffMatrix := mat.NewDense(moviesCount, moviesCount, nil)
	freqMatrix := mat.NewDense(moviesCount, moviesCount, nil)
	diffMatrix.Zero()
	freqMatrix.Zero()

	recordsCount := len(users)
	for i := 0; i < recordsCount; i++ {
		for j := 0; j < recordsCount; j++ {
			if users[i] == users[j] {
				// add ratings diff into the diff matrix
				value := diffMatrix.At(movies[i], movies[j])
				diffMatrix.Set(movies[i], movies[j], value+float64(ratings[i]-ratings[j]))
				// increment frequency
				value = freqMatrix.At(movies[i], movies[j])
				freqMatrix.Set(movies[i], movies[j], value+1)
			}
		}
	}

	// divide diff matrix by frequencies
	// diffMatrix.DivElem(diffMatrix, freqMatrix)
	for movie1 := 0; movie1 < moviesCount; movie1++ {
		diffMatrix.Set(movie1, movie1, 0)
		for movie2 := 0; movie2 < moviesCount; movie2++ {
			count := freqMatrix.At(movie1, movie2)
			if count > 0 {
				value := diffMatrix.At(movie1, movie2)
				diffMatrix.Set(movie1, movie2, value/float64(count))
			} else {
				// -20 -- special value to indicate missed cells.
				// It allows us do not store frequency matrix
				diffMatrix.Set(movie1, movie2, -20)
			}
		}
	}

	// https://stackoverflow.com/questions/43330938/export-function-that-returns-array-of-doubles
	vector := diffMatrix.RawMatrix().Data
	size := len(vector)
	p := C.malloc(C.size_t(size) * C.size_t(unsafe.Sizeof(C.float(0))))
	cVector := (*[1<<30 - 1]C.float)(p)[:size:size]

	// fill array
	for i, value := range vector {
		cVector[i] = C.float(value)
	}

	return C.size_t(size), (*C.float)(p)
}

func main() {}
