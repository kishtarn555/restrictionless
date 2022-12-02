# Tabu con RMQ

## Busqueda tabú no optimizada
Para el examen de tercer parcial implementamos busqueda Tabu a la greedy. Los pasos que realizamos son los siguientes:

El valor de una solución (función costo) lo asignamos de la siguiente manera:

### Definiciones:

* N: La cantidad de items
* W: Capacidad de la mochila
* Items[]:  arreglo de items [peso, costo]
* T : El tamaño de la lista tabu
* Lista tabu
* Reps: Cuantos pasos ejecutaremos
* Tabu: ListaTabu

### Funcion costo

La función que deseamos optimizar:
```cpp
funcionCosto(solucion) {
    if (solucion.pesoTotal <= W) {
        return solucion.valorTotal;
    } else {
        return -solucion.pesoTotal;
    }
}
```

### Vencidad

Definimos la solución como un vector binario de tamaño |Items|. donde solucion[i] = 1 si y solo si Items[i] esta en la solución.


### Algoritmo (Pseudocódigo)
```py
solucion = [0, 0, ..., 0] # Iniciar con la solucion vacia
bestFound = solucion # Llevar cuenta de la mejor solucion al momento
tabu = dequeue() # Lista tabu vacia

# Realiza rep pasos
for (rep in [1, 2, 3, ..., rep])  {
    mejorVecino = None
    
    # Revisa todos los vecinos, vecino i es el que vecino[i]!=solucion[i]
    for (i in [0, 1, 2, ..., N-1]) {
        if (i in tabu)
            continue # Este vecino viola la lista tabu
        vecino = cambio(solucion, i)         
        costo = funcionCosto(vecino)
        # Si este es mejor vecino que los anteriores, guardalo
        if (costo > funcionCosto(mejorVecino)) {
            mejorVecino = vecino
        }
    }
    tabu.addLeft(posicion donde solucion y mejorVecino difieren)
    solucion = mejorVecino # Cambia la solucion actual por el mejor vecino encontrado.
    if (funcionCosto(solucion) > )
}
```