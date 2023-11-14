# El problema

Queremos implementar búsqueda tabú para el problema de la mochila.
# Búsqueda tabú no optimizada
Para el examen de tercer parcial implementamos búsqueda Tabu a la greedy. Los pasos que realizamos son los siguientes:

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

# Valor de T.
Uno de los valores que para este algoritmo el programador debe decidir es T, el tamaño de la mochila. El cual varia dependiendo de la instancia del problema.

Pero observamos que los posibles valores de la lista tabu son: $[0, N-1]$

Entonces podemos correr el algoritmo para todas las T en el rango y quedarnos con la mejor solución encontrada.

Esta fuerza bruta para encontrar la mejor T nos da de complejidad:
Entonces, la complejidad de este algoritmo es N multiplicado por la complejidad de taboo:

$$O(N\cdot \text{Taboo})$$

$$= O(N(N\cdot \text{rep}))$$
$$= O(N^2(\text{rep}))$$

Para $N$ grandes, esta complejidad es mucha. 

# Usando RMQ
Podemos optimizarlo muchísimo, ya que es bastante fácil predecir cuál vecino va a tomar.

Definamos los siguientes dos conjuntos:

* $\text{backpack}$: Representa la lista de items que SÍ pertenecen a la solución **y que no están en la lista tabú**.

* $\text{shelf}$: Representa la lista de items que NO pertenecen a la solución **y que no están en la lista tabú**.

Es decir, $\text{shelf} \cup \text{backpack}$ es la lista de todos los items que no están en la lista tabú. Y por lo tanto donde podemos buscar el siguiente vecino.

Podemos ver que el ciclo al final tiene la siguiente prioridad.

A) Si la mochila no tiene sobre peso:

* Si en $\text{shelf}$ tenemos items que pesen menor o igual $W- pesoTotal$, es decir uno que quepa. Elegirá el item con mayor costo de esos. 

* Si no puede lo de arriba, quitará de la solución el item de $\text{backpack}$ menos valioso.

* Si no puede porque $\text{backpack}$ este vacío, agregara el producto de $\text{shelf}$ de menor peso.

B) Si la mochila tiene sobre peso entonces elegirá:

* Primero, quitar el item de menor costo en $\text{backpack}$ que tenga peso mayor o igual que `pesoTotal(solucion) - W`. Es decir, el que lo pase la funcionCosto de negativo a positivo y lo haga más valioso. 

* Si no existe ese item, quitará el de mayor peso de $\text{backpack}$. 

* Si no puede quitar ningun item (aka $|\text{backpack}| = 0$), agregará el item de $\text{shelf}$ más ligero 

Si tenemos a las listas backpack y shelf ordenadas por peso, podemos usar un [Segment Tree][1] para  cada lista y responder esas preguntas todas en $O(logN)$ en vez de $O(N)$.

Haremos que nuestro segment tree calcule para cualquier rango:
* El elemento más barato, su precio e indice.
* El elemento más caro su precio e indice.
* El elemento más pesado, su precio e indice.
* El elemento más barato su precio e indice.

Observemos que esto es lo mismo que:

* El máximo de pairs, $(\text{costo}, \text{indice})$.
* El mínimo de pairs $(\text{costo}, \text{indice})$.
* El máximo de pairs $(\text{peso}, \text{indice})$.
* El mínimo de pairs $(\text{peso}, \text{indice})$.


Es decir, encontrar el mejor vecino es un problema de RMQ (Range Minimum/Maximum Query).

Para eliminar elementos del ST, lo que haremos es que para los pairs de máximos le asignaremos $(-\infty, -1)$ y para los de máximos $(\infty, -1)$.

Esto nos permite reducir la complejidad significativamente.


Nuestro algoritmo descrito hasta ahorita se puede ver en el siguiente pseudocódigo:


```py
#Solución inicial es la trivial (todo vacio)
solucion = [0, 0, ..., 0]
bestFound = solucion
tabu = dequeue() # Lista tabu vacia

# Construye las listas como ST, shelf tiene todo al inicio, mientras que backpack inicia sin nada.
shelf = buildSegmentTree(items)
backpack = buildSegmentTree([-1,-1,...,-1])
# Realiza rep pasos
for (rep in [1, 2, 3, ..., rep])  {
    mejorVecino = None
    offset = W- pesoTotal(solucion)
    if (offset <= 0) {
        # Estamos debajo del limite de peso
        
        if (shelf.hasItemInRange(0, offset)) {
            # Si existe item de peso valido, agregalo:
            solution[shelf.MostExpensive(0, offset).index] =1
        } else if (backpack.hasAnyItem()) {
            # Quita el elemento mas barato de la mochila
            solution[backpack.cheapest().index] = 0
        } else if (shelf.hasAnyItem()) {
            # Agrega el elemento mas ligero
            solution[backpack.lightest().index] = 1
        }
    } else {
        offset = pesoTotal(solucion)- W
        # estamos en sobrepeso, prioritiza bajar
        if (backack.hasItemInRange(offset, inf)) {
            # Quitamos el item mas barato que nos baje de peso
            solucion[backpack.cheapestItem(offset, inf)] = 0
        } else if (backpack.hasAnyItem()) {
            # Quitamos el item mas pesado
            solucion[backpack.mostHeavy()]= 0
        } else {            
            # Agregamos el item mas ligero
            solucion[shelf.lightest()]= 1        
        }

    }
     
    # Agrega la posicion cambiada a la lista tabu
    positionChanged = solution.lastChanged
    tabu.add(positionChange) 
    #Remueve elemento tabu de la lista de movs. validos
    shelf[positionChanged] = -1
    backpack[positionChanged] = -1

    # Si la lista tabu excede T elementos, elimina el mas viejo.
    if (size(tabu) > T) {
        oldest= tabu.oldest()
        tabu.removeOldest()
        # Regresa el elemento a la lista de movimientos validos
        if (oldest in solution)
            backpack.add(oldest)
        else
            shelve.add(oldest)
    }
    solucion = mejorVecino # Cambia la solucion actual por el mejor vecino encontrado.
    if (funcionCosto(solucion) > funcionCosto(bestFound)) {
        bestFound = solucion
    }
}
```

Nos deshicimos del ciclo, pero si nos fijamos atentamente la complejidad no ha mejorado tanto como queríamos. Analicemos.

Principalmente se debe a que construir un ST es lento, es lineal sobre $N$.

La complejidad de la búsqueda tabú cambió de la siguiente manera:
$$O(N\cdot \text{rep})$$
$$\downarrow$$

$$O(\text{construir}+\text{rep}\cdot \text{buscar})$$ 
$$ = O(N+\text{rep}\cdot \text{log}N)$$

Y por lo tanto, la completa cambió de:
$O(N^2\cdot \text{rep})$ a $O(N^2+\text{rep}\cdot N\text{log}N)$.

Mientras que es una mejoría, Todavía tiene un término cuadrático. Podemos mejorar.

La observación clave es que estamos haciendo lo siguiente:

* construye segment tree para T=0 O(N)
* modifica segment tree para T=0 O(rep*logN)
* reconstruye segment tree para T=1 O(N)
* modifica segment tree para T=1 O(rep*logN)
* reconstruye segment tree para T=2 O(N)
* modifica segment tree para T=2 O(rep*logN)
* $etc \ldots$

Pero cada construcción restaura el segment tree siempre al mismo estado. Entonces podemos arreglar esto de una forma sencilla:

### Opción 1: Usa un Segment Tree persistente.

Una estructura de datos persistente es una estructura que nunca destruye datos, solo aumenta la información, de forma de que es posible restaurar versiones anteriores. Programado eficientemente, la restauración toma $O(1)$, mientras que la memoria por query pasa de $O(N)$ a $O(N+rep\cdot logN)$.

Es la solución más directa, pero ocupa mucho código y memoria, no elegí esta.

### Opción 2: Guarda el Segment Tree original y restauralo.

La idea es sencilla, es cambiar de:
* construye segment tree
* modifica segment tree para T=0
* reconstruye segment tree 
* modifica segment tree para T=1
* reconstruye segment tree
* modifica segment tree para T=2
* $etc \ldots$

Y en vez de eso, utilizar:
* construye segment tree para T=0
* **ORIGINAL** = segment tree 
* modifica segment tree para T=0 O
* segment tree = **ORIGINAL**
* modifica segment tree para T=1 
* segment tree = **ORIGINAL**
* modifica segment tree para T=2
* $etc \ldots$

Es decir, guardar el ST en un temporal y cuando sea necesario restaurarlo desde allí.

Puede que no parezca mejoría porque el ST usa memoria $O(N)$ y copiar memoria de tamaño lineal toma $O(N)$ tiempo, lo mismo que la construcción. Sin embargo, podemos hacer un truco para mejorar esto.

Usaremos [Lazy Propagation][2] para hacer [Lazy initialization][3]. ¡Lo cuál nos reduce la complejidad de la igualación a $O(1)$!.

Es decir, para un vértice del árbol, no hacemos ST[i] = original[i] hasta que requiramos conocer este valor. Y como solo lo modificamos cuando requerimos conocer este valor, la asignación nos sale "gratis".

También aplicamos Lazy Copy a la parte de copiar `bestFound = solution` para hacerlo $O(1)$.

# Nueva complejidad
Aplicando este truco nuestra complejidad final es:

$$O(N(\text{rep}\cdot \text{log}N))$$
$$= O(N\text{logN}\cdot rep)$$

# Eligiendo reps

Reps lo establecemos como $\lfloor\frac{10^6}{N}\rfloor$, igual que teníamos antes, esto con el afán de mantener un tiempo de ejecución por caso de unos cuantos segundos.

# Cotejando
Cotejando este algoritmo, produce las mismas respuestas para K<=50 y K = 3.

Así que confío que este programado correctamente.

# Resultados

A continuación mostramos resultados.

## Comparando resultados
La mejor métrica que conozco para medir la efectividad de búsquedas son los bits:

No tengo mucha experiencia con Teoría de información, pero definiría una métrica como:


$bit(solucion) = log_2(1+\text{\# de soluciones mejores que solucion} )$.

Cuanto menor mejor. Y esto pq es más fácil eliminar 100 soluciones de 1000, que 100 de 101.

En base a eso  y a que hay $2^N$ soluciones, yo aproximo un bit con la formula:

$bit(solucion) = log_2((2-\frac{solucion}{optimo})*2^N ) = N\text{log}_2(2-\frac{solucion}{optimo})$.

Pero esta fórmula esta muy sacada de mi intuición en un tema que no me siento cómodo. Además, asume que las soluciones están distribuidas uniformemente en el rango $[0, optimo]$, pero esto no es el caso. La mayoría de soluciones son inválidas, (es decir con peso 0), por lo que en realidad nuestro bit es mucho menor a un bit real. 

En cualquier caso he aquí la tabla:

![img](src/tabla.png)

De 20 casos, 7 ya exploraba todo.

De 13 casos más explorados, 4 mejoraron y 9 quedaron iguales.


# Gráficas de cada caso
A continuación mostramos dos gráficas de cada caso.

La primera es dispersión costo (horizontal) y peso (vertical).

La segunda es T (horizontal) vs mejorSolución (vertical)

## ks_4_0
![](src/d_ks_4_0.png)

![](src/t_ks_4_0.png)

## ks_19_0

![](src/d_ks_19_0.png)


![](src/t_ks_19_0.png)
## ks_30_0

![](src/d_ks_30_0.png)


![](src/t_ks_30_0.png)
## ks_40_0

![](src/d40.0.png)

![](src/t40.0.png)
## ks_45_0
![](src/d45.0.png)

![](src/t45.0.png)

## ks_50_0
![](src/d50.0.png)

![](src/t50.0.png)

## ks_50_1
![](src/d50.1.png)

![](src/t50.1.png)

## ks_60_0
![](src/d60.0.png)

![](src/t60.0.png)

## ks_82_0
![](src/d82.0.png)

![](src/t82.0.png)

## ks_1000_0
![](src/d_ks_1000_0.png)


![](src/t_ks_1000_0.png)


# Correr el código

El archivo buildrun.bash compila y corre el código.

Imprime a la carpeta output dos archivos por caso, un .out que es la salida especificada en el formato del archivo y un .csv donde imprime una tabla de K contra mejor soluciónEncontrada.


# Lectura Adicional
https://cp-algorithms.com/data_structures/segment_tree.html

https://en.wikipedia.org/wiki/Lazy_initialization

[1]: https://cp-algorithms.com/data_structures/segment_tree.html

[2]: https://cp-algorithms.com/data_structures/segment_tree.html#range-updates-lazy-propagation

[3]: https://en.wikipedia.org/wiki/Lazy_initialization
