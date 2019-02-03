package main

import "C"
import (
	"fmt"
	"unsafe"

	"github.com/kniren/gota/dataframe"
	"github.com/kniren/gota/series"
	"gonum.org/v1/gonum/mat"
)

// BuildSlopeOne builds deviation matrix for Slope One collaborative filtering algorithm
//export BuildSlopeOne
func BuildSlopeOne(users []int32, movies []int32, ratings []int32) (C.size_t, *C.float) {
	userSet := make(map[int32]bool)
	for _, user := range users {
		userSet[user] = true
	}

	movieSet := make(map[int32]bool)
	for _, movie := range movies {
		movieSet[movie] = true
	}
	moviesCount := len(movieSet)

	df := dataframe.New(
		series.New(users, series.Int, "user"),
		series.New(movies, series.Int, "movie"),
		series.New(ratings, series.Int, "rating"),
	)

	diffMatrix := mat.NewDense(moviesCount, moviesCount, nil)
	freqMatrix := mat.NewDense(moviesCount, moviesCount, nil)
	diffMatrix.Zero()
	freqMatrix.Zero()
	for user := range userSet {
		fil := df.Filter(dataframe.F{
			Colname:    "user",
			Comparator: series.Eq,
			Comparando: user,
		})
		filMovies, _ := fil.Col("movie").Int()
		filRatings, _ := fil.Col("rating").Int()

		for i, movie1 := range filMovies {
			rating1 := filRatings[i]
			for j, movie2 := range filMovies {
				if movie1 != movie2 {
					rating2 := filRatings[j]
					// add ratings diff into the diff matrix
					value := diffMatrix.At(movie1, movie2)
					diffMatrix.Set(movie1, movie2, value+float64(rating1-rating2))
					// increment frequency
					value = freqMatrix.At(movie1, movie2)
					freqMatrix.Set(movie1, movie2, value+1)
				}
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
	fmt.Println("done!")

	return C.size_t(size), (*C.float)(p)
}

func main() {}
