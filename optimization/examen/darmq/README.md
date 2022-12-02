# Tabú con RMQ

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
#Solución inicial es la trivial (todo vacio)
solucion = [0, 0, ..., 0]
bestFound = solucion
tabu = dequeue() # Lista tabu vacia

# Realiza rep pasos
for (rep in [1, 2, 3, ..., rep])  {
    mejorVecino = None
    
    # Revisa todos los vecinos, i marca el elemento cambiado
    for (i in [0, 1, 2, ..., N-1]) {
        if (i in tabu)
            continue # Este vecino viola la lista tabu

        # Obten el vector vecino de solucion con la posicion i cmabiada
        vecino = obtenVecino(solucion, i)
        # Si este es mejor vecino que los anteriores, guardalo
        if (
            mejorVecino is None
            or funcionCosto(vecino) > funcionCosto(mejorVecino)            
        ) {
            mejorVecino = vecino
        }
    }
    tabu.add(posicion donde solucion y mejorVecino difierent) # Agrega la posicion cambiada a la lista tabu

    # Si la lista tabu excede T elementos, elimina el mas viejo.
    if (size(tabu) > T) {
        tabu.removeOldest();
    }
    solucion = mejorVecino # Cambia la solucion actual por el mejor vecino encontrado.
    if (funcionCosto(solucion) > funcionCosto(bestFound)) {
        bestFound = solucion
    }
}

print(bestFound)  # Termina, bestfound es la mejor solucion encontrada.
```

Programando este algoritmo (y usando trucos para que funcionCosto corra en $O(1)$) obtenemos que este algoritmo tiene complejidad:

$O(\text{rep}\cdot N)$.

## Valor de T.
Uno de los valores que para este algoritmo el programador debe decidir es T, el tamaño de la mochila. El cual varia dependiendo de la instancia del problema.

Pero observamos que los posibles valores de la lista tabu son: $[0, N-1]$

Entonces podemos correr el algoritmo para todas las T en el rango y quedarnos con la mejor solución encontrada.

Esta fuerza bruta para encontrar la mejor T nos da de complejidad:

$$O(N^2(\text{rep}))$$

Para $N$ grandes, esta complejidad es mucha. 

### Usando RMQ
Podemos optimizarlo muchisímo, ya que es bastante fácil predecir cuál vecino va a tomar.

Definamos los siguientes dos conjuntos:

* $\text{backpack}$: Representa la lista de items que SÍ pertenecen a la solución **y que no estan en la lista tabú**.

* $\text{shelve}$: Representa la lista de items que NO pertenecen a la solución **y que no estan en la lista tabú**.



Podemos ver que el ciclo al final tiene la siguiente prioridad.

A) Si la mochila no tiene sobre peso:

* Si en $\text{shelve}$ tenemos items que pesen menor o igual $W- pesoTotal$, es decir uno que quepa. Elejirá el item con mayor costo de esos. 

* Si no puede lo de arriba, quitará de la solución el item de $\text{backpack}$ menos valioso.

* Si no puede porque $\text{backpack}$ este vacío, agregara el producto de $\text{shelve}$ de menor peso.

B) Si la mochila tiene sobre peso entonces elijirá:

* Primero, quitar el item de menor costo en $\text{backpack}$ que tenga peso mayor o igual que `pesoTotal(solucion) - W`. Es decir, el que lo pase la funcionCosto de negativo a positivo y lo haga más chido 

* Si no existe ese item, quitará el de mayor peso de $\text{backpack}$. 

* Si no puede quitar ningun item (aka $|\text{backpack}| = 0$), agregará el item de $\text{shelve}$ más ligero 

Si tenemos a las listas backpack y shelve ordenadas por peso, podemos usar un Segment Tree para  cada lista y responder esas preguntas todas en $O(logN)$ en vez de $O(N)$.

Haremos que nuestro segment tree calcule para cualquier rango:
* El elemento más barato, su precio e indice.
* El elemento más caro su precio e indice.
* El elemento más pesado, su precio e indice.
* El elemento más barato su precio e indice.

Observemos que esto es lo mismo que:

* El maximo de pairs, $(\text{costo}, \text{indice})$.
* El minimo de pairs $(\text{costo}, \text{indice})$.
* El maximo de pairs $(\text{peso}, \text{indice})$.
* El minimo de pairs $(\text{peso}, \text{indice})$.


Es decir, encontrar el mejor vecino es un problema de RMQ (Range Minimum/Maximum Query).

Para eliminar elementos del ST, lo que haremos es que para los pairs de maximos le asignaremos $(-\infty, -1)$ y para los de máximos $(infty, -1)$.