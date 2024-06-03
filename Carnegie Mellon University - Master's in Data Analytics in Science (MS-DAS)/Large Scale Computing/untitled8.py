import numpy as np
from mpi4py import MPI
import time
import matplotlib.pyplot as plt

start = time.time()

# Initialize MPI
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

# Define the size of the grid
ROWS, COLUMNS = 1000, 1000
MAX_TEMP_ERROR = 0.01

# Calculate the number of rows per process (including ghost cells)
local_rows = (ROWS // size)  # Rows per process without ghost cells

local_rows_ghost = local_rows + 2

# Create local temperature arrays for each process

temperature = np.empty((local_rows, COLUMNS + 2))
temperature_last = np.empty((local_rows, COLUMNS + 2))

# Initialize temperature for each process
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


# Function to output data (visualize or save)
def output(data):
    plt.imshow(data[1:-1, 1:-1])  # Exclude ghost cells for visualization
    plt.colorbar()
    plt.savefig("temperature_plot.png")
    plt.show()

initialize_temperature(temperature_last)

# Distributing the array into 0-251 size, including 2 rows of ghost cell top and bottom
for i in range(size):
    if rank == i:
        if rank == 0:
            print("Rank", rank)
            temperature_last = temperature_last[0:((i+1)*local_rows)+1,:]
            print(temperature_last.shape) #lets me know that it is split to 251,1002
        if rank >0:
            print("Rank", rank)
            temperature_last = temperature_last[(i*local_rows):((i+1)*local_rows)+1,:]
            print(temperature_last.shape)
            
            
max_iterations = int(input("Maximum iterations: "))

dt = 100
iteration = 1

while (dt > MAX_TEMP_ERROR) and (iteration < max_iterations):
    # Perform the computation for the local rows
    for i in range(1, 250-1):  # Exclude ghost cells
        for j in range(1, 1001):
            temperature[i, j] = 0.25 * (
                temperature_last[i + 1, j] + temperature_last[i - 1, j] +
                temperature_last[i, j + 1] + temperature_last[i, j - 1]
            )
            print(temperature.shape)
            print(temperature_last.shape)
    # Communicate ghost cells between neighboring processes
    dt = 0 
    
    if rank == 0:
        comm.Send(temperature[250, 1:COLUMNS+1], dest=rank + 1)
        comm.Recv(temperature[0, 1:COLUMNS+1], source=rank + 1)
        comm.Barrier()
    if rank == 1:
        comm.Recv(temperature[0, 1:COLUMNS+1], source=rank - 1)
        comm.Send(temperature[250, 1:COLUMNS+1], dest=rank + 1)
        comm.Recv(temperature[0, 1:COLUMNS+1], source=rank + 1)
        comm.Send(temperature[250, 1:COLUMNS+1], dest=rank - 1)
        comm.Barrier()
    if rank == 2:
        comm.Recv(temperature[0, 1:COLUMNS+1], source=rank - 1)
        comm.Send(temperature[250, 1:COLUMNS+1], dest=rank + 1)
        comm.Recv(temperature[0, 1:COLUMNS+1], source=rank + 1)
        comm.Send(temperature[250, 1:COLUMNS+1], dest=rank - 1)
        comm.Barrier()
    if rank == 3:
        comm.Recv(temperature[0, 1:COLUMNS+1], source=rank - 1)
        comm.Send(temperature[250, 1:COLUMNS+1], dest=rank - 1)
        comm.Barrier()
    # Calculate the maximum temperature change (dt) for this process
    dt_local = np.max(np.abs(temperature[1:-1, 1:COLUMNS+1] - temperature_last[1:-1, 1:COLUMNS+1]))

    # Reduce dt_local values across all processes to find the global maximum
    dt = comm.allreduce(dt_local, op=MPI.MAX)

    # Update temperature_last for the next iteration
    temperature_last[1:-1, 1:COLUMNS+1] = temperature[1:-1, 1:COLUMNS+1]

    # Synchronize all processes
    comm.Barrier()

    if rank == 0:
        print("Iteration:", iteration)
        iteration += 1

output(temperature_last)

end = time.time()
print(end - start)
exit()
# =============================================================================
# def communicate_ghost_cells():
#     if size > 1:
#         # Send the last row to the next process (circular)
#         next_rank = (rank + 1) % size
#         prev_rank = (rank - 1) % size
# 
#         comm.Send(temperature[-2, 1:COLUMNS+1], dest=next_rank, tag=rank)
#         comm.Recv(temperature[-1, 1:COLUMNS+1], source=prev_rank, tag=prev_rank)
# 
# def communicate_ghost_cells():
#     if size > 1:
#         # Send the last row to the next process (linear)
#         next_rank = (rank + 1) % size
# 
#         comm.Send(temperature[-2, 1:COLUMNS+1], dest=next_rank, tag=rank)
#         comm.Recv(temperature[0, 1:COLUMNS+1], source=next_rank, tag=next_rank)
# =============================================================================
