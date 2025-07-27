# MPI

Este repositorio contiene dos programas MPI en Python (mpi4py) para demostrar y analizar operaciones colectivas y mediciones de latencia punto a punto

## 1. Operaciones Colectivas en MPI (estadisticas_mpi.py)

Este programa calcula estadísticas globales (mínimo, máximo, promedio) de un arreglo de números aleatorios utilizando operaciones colectivas de MPI: MPI_Bcast para el tamaño, MPI_Scatter para distribuir el arreglo y MPI_Reduce para los resultados globales.

-- Instrucciones de Ejecución

 mpi4py y numpy instalados en Python

Guarda el código para la Parte A como estadisticas_mpi.py en tu directorio de trabajo.

Ejecuta el programa desde la terminal usando mpirun, especificando el número de procesos (-np) y el tamaño del arreglo (N).

Importante: El tamaño N del arreglo debe ser divisible por el número de procesos utilizados.

Ejemplo:
Para ejecutar con 4 procesos y un arreglo de 1,000,000 elementos:

Bash
mpirun -np 4 python estadisticas_mpi.py 1000000
--Resultados Esperados:

Verás una salida similar a esta, mostrando el progreso de cada proceso y finalmente las estadísticas globales calculadas por el proceso raíz (rank 0):

Proceso 0: Inicializando arreglo de 1000000 elementos.
Proceso 0: Subarreglo min=0.01, max=99.99, avg=50.00
Proceso 1: Subarreglo min=0.02, max=99.98, avg=50.01
Proceso 2: Subarreglo min=0.00, max=99.97, avg=49.99
Proceso 3: Subarreglo min=0.03, max=100.00, avg=50.02

--- Resultados Globales ---
Mínimo Global: 0.00
Máximo Global: 100.00
Promedio Global: 50.01


 ## 2. Medición de Latencia de Comunicaciones Punto a Punto (latencia_mpi.py)

Este programa mide la latencia de comunicación entre dos procesos (rank 0 y rank 1) utilizando repetidamente MPI_Send y MPI_Recv. El proceso 0 envía un mensaje al proceso 1, que lo devuelve inmediatamente. El tiempo total se mide y se calcula la latencia promedio.

--Instrucciones de Ejecución

Guarda el código como latencia_mpi.py

Ejecuta el programa desde la terminal usando mpirun, especificando exactamente 2 procesos. Debes proporcionar el número de iteraciones y, opcionalmente, el tamaño del mensaje en bytes.

Ejemplos:

Para 10,000 iteraciones con un mensaje de 1 byte:

Bash
mpirun -np 2 python latencia_mpi.py 10000 1
Para 1,000 iteraciones con un mensaje de 1024 bytes (1 KB):

Bash
mpirun -np 2 python latencia_mpi.py 1000 1024
Para 100 iteraciones con un mensaje de 1,048,576 bytes (1 MB):

Bash
mpirun -np 2 python latencia_mpi.py 100 1048576
Resultados Esperados

La salida mostrará el tamaño del mensaje, el número de transmisiones y la latencia calculada:

Mensaje de 1 byte(s) transmitido 10000 veces.
Latencia promedio por mensaje (ida y vuelta): 3.20 microsegundos
Latencia estimada unidireccional: 1.60 microsegundos
