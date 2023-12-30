import random


# Definición del problema
estudiantes = ["Estudiante1", "Estudiante2", "Estudiante3", "Estudiante4"]
aulas = ["Aula1", "Aula2", "Aula3"]
horarios = ["Lunes 8:00-10:00", "Martes 10:00-12:00", "Miércoles 14:00-16:00"]


# Representación genética: cromosoma = [estudiante, aula, horario]
def generar_individuo():
    return [(estudiante, random.choice(aulas), random.choice(horarios)) for estudiante in estudiantes]


# Función de evaluación: calcular la calidad del horario (menos cruces)
def evaluar_horario(horario):
    cruces = sum(horario.count((estudiante, aula, hora)) for estudiante, aula, hora in horario) - len(estudiantes)
    return max(-cruces, 1)  # Usamos max para asegurar que la puntuación sea al menos 1


# Función de selección: seleccionar individuos para cruzamiento
def seleccionar_padres(poblacion):
    pesos = [evaluar_horario(individuo) for individuo in poblacion]
   
    # Asegurarse de que al menos un individuo tenga una puntuación diferente de cero
    while all(peso == 0 for peso in pesos):
        pesos = [evaluar_horario(individuo) for individuo in poblacion]


    return random.choices(poblacion, k=2, weights=pesos)


# Función de cruzamiento: combinar los genes de dos padres
def cruzar(padre1, padre2):
    punto_corte = random.randint(1, len(padre1) - 1)
    hijo = padre1[:punto_corte] + padre2[punto_corte:]
    return hijo


# Función de mutación: introducir pequeñas modificaciones en el genoma
def mutar(individuo):
    indice = random.randint(0, len(individuo) - 1)
    individuo[indice] = (estudiantes[random.randint(0, len(estudiantes) - 1)], aulas[random.randint(0, len(aulas) - 1)], horarios[random.randint(0, len(horarios) - 1)])
    return individuo


# Algoritmo genético
def algoritmo_genetico(num_generaciones, tamano_poblacion):
    poblacion = [generar_individuo() for _ in range(tamano_poblacion)]


    for generacion in range(num_generaciones):
        poblacion = sorted(poblacion, key=evaluar_horario, reverse=True)


        nueva_poblacion = []
        for _ in range(tamano_poblacion // 2):
            padre1, padre2 = seleccionar_padres(poblacion)
            hijo1 = cruzar(padre1, padre2)
            hijo2 = cruzar(padre2, padre1)


            if random.random() < 0.1:  # Probabilidad de mutación
                hijo1 = mutar(hijo1)
            if random.random() < 0.1:
                hijo2 = mutar(hijo2)


            nueva_poblacion.extend([hijo1, hijo2])


        poblacion = nueva_poblacion


    mejor_horario = max(poblacion, key=evaluar_horario)
    return mejor_horario


# Uso del algoritmo genético
mejor_horario_encontrado = algoritmo_genetico(num_generaciones=100, tamano_poblacion=50)
print("Mejor horario encontrado:", mejor_horario_encontrado)
