import numpy as np
import matplotlib as plt
from mpi4py import MPI
import time

start = time.time()


ROWS_total, COLUMNS_total = 1000 , 1000
ROWS, COLUMNS = 250, 250
MAX_TEMP_ERROR = 0.01
temperature	 = np.empty(( ROWS+2 , COLUMNS+2 ))
temperature_last = np.empty(( ROWS+2 ,COLUMNS+2  ))

def initialize_temperature(temp):

    temp[:,:] = 0

    #Set right side boundery condition
    for i in range(ROWS+1):
        temp[ i , COLUMNS+1 ] = ( 100/ROWS ) * i

    #Set bottom boundery condition
    for i in range(COLUMNS+1):
        temp[ ROWS+1 , i ] = ( 100/ROWS ) * i

    return temp


def output(data):
    plt.pyplot.imshow(data)
    data.tofile("plate.out")
    #bottom corner
    plt.pyplot.imshow(data[-1000:,-1000:])
    #plate = np.fromfile("plate.out", dtype=float).reshape((1002,1002))
    #plt.pyplot.imshow(plate. norm=plt.color.LogNorm(0.1,50,clip=Ture))

initialize_temperature(temperature_last)

max_iterations = int (input("Maximum iterations: "))

dt = 100
iteration = 1

while ( dt > MAX_TEMP_ERROR ) and ( iteration < max_iterations ):

    for i in range( 1 , ROWS+1 ):
        for j in range( 1 , COLUMNS+1 ):
            temperature[ i , j ] = 0.25 * ( temperature_last[i+1,j] + temperature_last[i-1,j] +
                                            temperature_last[i,j+1] + temperature_last[i,j-1]   )

    dt = 0

    for i in range( 1 , ROWS+1 ):
        for j in range( 1 , COLUMNS+1 ):
            dt = max( dt, temperature[i,j] - temperature_last[i,j])
            temperature_last[ i , j ] = temperature [ i , j ]

    print(iteration)
    iteration += 1

output(temperature_last)

end = time.time()
print(end - start)