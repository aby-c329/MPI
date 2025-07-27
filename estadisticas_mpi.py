
from mpi4py import MPI
import numpy as np
import sys

def run_collective_operations(n_elements):
    """
    Ejecuta operaciones colectivas de MPI para calcular estadísticas globales
    de un arreglo de números aleatorios.
    """
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    # Validar que N sea divisible por el número de procesos
    if n_elements % size != 0:
        if rank == 0:
            print(f"Error: El tamaño N ({n_elements}) no es divisible entre el número de procesos ({size}).")
            print("Por favor, asegúrate de que N sea un múltiplo del número de procesos.")
        comm.Abort() # Termina todos los procesos si hay un error de división
        sys.exit(1)

    global_array = None
    if rank == 0:
        # 1. El proceso de rank = 0 inicializa un arreglo de N números aleatorios entre 0 y 100.
        print(f"Proceso {rank}: Inicializando arreglo de {n_elements} elementos.")
        global_array = np.random.uniform(0, 100, n_elements)

    # 2. MPI_Bcast: para enviar el tamaño del arreglo desde el proceso raíz a los demás.
    # El tamaño N ya está disponible para todos los procesos si se pasa como argumento.
    # Sin embargo, es buena práctica hacer un Bcast si el origen del valor es solo el rank 0.
    # En este caso, n_elements se pasa como argumento, así que no es estrictamente necesario,
    # pero lo incluimos para demostrar el uso de MPI_Bcast.
    n_elements = comm.bcast(n_elements, root=0)

    # Calcular el tamaño del subarreglo para cada proceso
    elements_per_process = n_elements // size
    local_array = np.empty(elements_per_process, dtype=np.float64)

    # 3. MPI_Scatter: para distribuir partes del arreglo entre los procesos.
    comm.Scatter(global_array, local_array, root=0)

    # Cada proceso calcula el mínimo, máximo y promedio de su subarreglo.
    local_min = np.min(local_array)
    local_max = np.max(local_array)
    local_sum = np.sum(local_array)
    local_count = len(local_array)
    local_avg = local_sum / local_count

    print(f"Proceso {rank}: Subarreglo min={local_min:.2f}, max={local_max:.2f}, avg={local_avg:.2f}")

    # 4. Usando MPI_Reduce, se obtiene el mínimo, máximo y promedio global en el proceso raíz.
    global_min = comm.reduce(local_min, op=MPI.MIN, root=0)
    global_max = comm.reduce(local_max, op=MPI.MAX, root=0)
    global_sum = comm.reduce(local_sum, op=MPI.SUM, root=0)

    # El promedio global se calcula a partir de la suma global y el número total de elementos.
    global_avg = global_sum / n_elements if n_elements > 0 else 0

    # 5. El proceso raíz imprime los resultados.
    if rank == 0:
        print("\n--- Resultados Globales ---")
        print(f"Mínimo Global: {global_min:.2f}")
        print(f"Máximo Global: {global_max:.2f}")
        print(f"Promedio Global: {global_avg:.2f}")

        # MPI_Gather (opcional): para reconstruir el arreglo completo en el proceso raíz.
        # Esto es solo para demostración, ya que el proceso raíz ya tiene el arreglo completo
        # antes del Scatter. Se podría usar si el arreglo se construye en partes en los procesos.
        gathered_array = None
        if global_array is not None: # Verifica si global_array fue inicializado
            gathered_array = np.empty(n_elements, dtype=np.float64)
        comm.Gather(local_array, gathered_array, root=0)
        # print(f"Proceso {rank}: Arreglo reconstruido (primeros 10 elementos): {gathered_array[:10]}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: mpirun -np <num_procesos> python estadisticas_mpi.py <N_elementos>")
        sys.exit(1)

    try:
        N = int(sys.argv[1])
    except ValueError:
        print("Error: N_elementos debe ser un número entero.")
        sys.exit(1)

    run_collective_operations(N)
