package main

import "C"
import (
	"unsafe"

	"gonum.org/v1/gonum/mat"
)

//export BuildSlopeOne
func BuildSlopeOne(users []int32, movies []int32, ratings []int8) (C.size_t, *C.float) {
	m := mat.NewDense(3, 3, []float64{
		2.0, 9.0, 3.0,
		4.5, 6.7, 8.0,
		1.2, 3.0, 6.0,
	})
	vector := m.RawMatrix().Data

	// https://stackoverflow.com/questions/43330938/export-function-that-returns-array-of-doubles
	size := 9
	p := C.malloc(C.size_t(size) * C.size_t(unsafe.Sizeof(C.float(0))))
	cVector := (*[1<<30 - 1]C.float)(p)[:size:size]

	// fill array
	for i, value := range vector {
		cVector[i] = C.float(value)
	}

	return C.size_t(size), (*C.float)(p)
}

func main() {}
