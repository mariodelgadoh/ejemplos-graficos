# Hecho por Mario Delgado

import re

# Función que implementa el algoritmo de Floyd-Warshall para encontrar las distancias más cortas
def floyd_warshall(graph):
    n = len(graph)
    dist = [row[:] for row in graph]  # Copiar la matriz de adyacencia

    # Aplicar el algoritmo de Floyd-Warshall
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
    
    return dist

# Función para imprimir la matriz de distancias de manera legible
def print_matrix(matrix):
    for row in matrix:
        print(" ".join(map(lambda x: f"{x:.1f}" if isinstance(x, float) else str(x), row)))

def main():
    print("¡Bienvenido al programa de Floyd-Warshall simplificado!")
    
    # Solicitar al usuario el número de vértices
    n = int(input("Ingrese el número de vértices del grafo: "))
    
    # Inicializar la matriz de adyacencia con infinito (inf) y 0 en la diagonal
    graph = [[float('inf')] * n for _ in range(n)]
    for i in range(n):
        graph[i][i] = 0  # La distancia de un vértice a sí mismo es 0
    
    # Expresión regular para aceptar entradas en diferentes formatos:
    # Puede ser 'i,j,peso', 'i-j-peso', 'i j peso', o simplemente 'ijpeso' (sin separadores)
    edge_pattern = re.compile(r'^(\d+)[, -]?(\d+)[, -]?(\d+)$')
    
    print("\nIngrese las aristas y sus pesos (ingrese 'fin' para terminar):")
    print("Formato: 'i,j,peso', 'i-j-peso', 'ijpeso' o 'i j peso' (ejemplo: '0 1 5')")
    print("Puede usar '-' para indicar que no hay camino entre dos nodos.")

    while True:
        edge = input("> ")
        if edge.lower() == 'fin':
            break
        match = edge_pattern.match(edge)
        if match:
            i, j, weight = match.groups()
            i, j = int(i), int(j)
            
            if i >= n or j >= n:
                print(f"Error: Los vértices deben estar entre 0 y {n-1}. Intente de nuevo.")
                continue
            
            # Validar si el peso es '-' para indicar que no hay camino
            if weight == '-':
                graph[i][j] = float('inf')  # Sin camino se representa con infinito
            else:
                try:
                    weight = int(weight)  # Convertir el peso a entero
                    graph[i][j] = weight
                except ValueError:
                    print("Error: El peso debe ser un número entero o '-'. Intente de nuevo.")
        else:
            print("Error: Formato incorrecto. Use 'i,j,peso', 'i-j-peso', 'ijpeso'. Intente de nuevo.")
    
    # Calcular las distancias más cortas usando Floyd-Warshall
    shortest_distances = floyd_warshall(graph)
    
    print("\nMatriz de distancias más cortas:")
    
    # Imprimir la matriz resultante
    print_matrix(shortest_distances)

if __name__ == "__main__":
    main()
