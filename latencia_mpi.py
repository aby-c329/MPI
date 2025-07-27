from mpi4py import MPI
import numpy as np
import sys
import time

def run_latency_measurement(num_iterations, message_size_bytes):
    """
    Mide la latencia de comunicaciones punto a punto entre dos procesos.
    """
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    if size != 2:
        if rank == 0:
            print("Error: Este programa debe ejecutarse con exactamente 2 procesos (mpirun -np 2).")
        sys.exit(1)

    # Crear un buffer para el mensaje con el tamaño especificado
    # Usamos np.byte para representar 1 byte. Para mensajes más grandes,
    # podrías usar np.zeros(message_size_bytes, dtype=np.byte)
    message = np.zeros(message_size_bytes, dtype=np.byte)
    
    if rank == 0:
        start_time = MPI.Wtime() # Tiempo inicial
        for _ in range(num_iterations):
            # Proceso 0 envía a Proceso 1
            comm.Send(message, dest=1, tag=0)
            # Proceso 0 recibe de Proceso 1
            comm.Recv(message, source=1, tag=1)
        end_time = MPI.Wtime() # Tiempo final

        total_time = end_time - start_time
        
        # Calcular latencia promedio por mensaje (ida y vuelta)
        # Convertir segundos a microsegundos
        avg_latency_microseconds = (total_time / num_iterations) * 1e6
        
        print(f"\nMensaje de {message_size_bytes} byte(s) transmitido {num_iterations} veces.")
        print(f"Latencia promedio por mensaje (ida y vuelta): {avg_latency_microseconds:.2f} microsegundos")
        print(f"Latencia estimada unidireccional: {avg_latency_microseconds / 2:.2f} microsegundos")

    elif rank == 1:
        for _ in range(num_iterations):
            # Proceso 1 recibe de Proceso 0
            comm.Recv(message, source=0, tag=0)
            # Proceso 1 retorna inmediatamente a Proceso 0
            comm.Send(message, dest=0, tag=1)

if __name__ == "__main__":
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print("Uso: mpirun -np 2 python latencia_mpi.py <N_iteraciones> [tamano_mensaje_bytes]")
        print("Ejemplo: mpirun -np 2 python latencia_mpi.py 10000 1")
        print("Ejemplo: mpirun -np 2 python latencia_mpi.py 10000") # Por defecto 1 byte
        sys.exit(1)

    try:
        num_iterations = int(sys.argv[1])
        message_size_bytes = 1 # Valor por defecto
        if len(sys.argv) == 3:
            message_size_bytes = int(sys.argv[2])
    except ValueError:
        print("Error: N_iteraciones y tamano_mensaje_bytes deben ser números enteros.")
        sys.exit(1)
        
    run_latency_measurement(num_iterations, message_size_bytes)
