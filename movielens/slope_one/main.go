package main

import "C"
import "gonum.org/v1/gonum/mat"

//export BuildSlopeOne
func BuildSlopeOne(users []int32, movies []int32, ratings []int8) []C.float {
	m := mat.NewDense(3, 3, []float64{
		2.0, 9.0, 3.0,
		4.5, 6.7, 8.0,
		1.2, 3.0, 6.0,
	})
	vector := m.RawMatrix().Data
	cVector := make([]C.float, 9)
	for i, value := range vector {
		cVector[i] = C.float(value)
	}
	return cVector
}

func main() {}
