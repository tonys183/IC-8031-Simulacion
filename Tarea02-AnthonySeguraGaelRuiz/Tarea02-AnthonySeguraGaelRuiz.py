CUABITS = 4
CINBITS = 5

def probarGene(x0, k, fun, *para):
    for _ in range(k):
        x0 = fun(x0, *para)
        print(f'{x0}', end=" ")
    print()

# Ejercicio 1
def congruBin(n):
    ub = n&1
    b2 = (n>>2)&1
    xb = ub^b2
    return (n>>1) | (xb<<(CUABITS-1))

# Ejercicio 2
def congruBinCin(n):
    ub = n&1
    b2 = (n>>2)&1
    xb = ub^b2
    return (n>>1) | (xb<<(CINBITS-1))

# Ejercicio 3
def cantDig(n):
    return 1+cantDig(n//10) if n else 0

def cuadMedios(n):
    n *= n
    cd = cantDig(n) + cantDig(n)&1
    return (n//(10**((cd-CUABITS)>>1))) % 10**CUABITS

# Ejercicio 4 y 5
def congruMixMulti(n,a,c,m):
    return (n*a+c) % m

def gcd(a,b):
    while b:
        a, b = b, a%b
    return a

# Ejercicio 9
def congruAdi(x0, x1, m):
    while True:
        yield x0
        x0, x1 = x1, (x1+x0)%m

# Ejercicio 10
def genDigit(x0, a, c, m, ub):
    x0 = congruMixMulti(x0, a, c, m)
    return int((x0 / m) * ub), x0

def menuEjercicio1():
    # A)
    """
    No hace el recorrido completo
    """

    # B)
    """
    No hace el recorrido completo
    """

    while True:
        print("\n--- Ejercicio 1 ---")
        print("1. Semilla A (x0 = 6)")
        print("2. Semilla B (x0 = 15)")
        print("0. Volver")
        op = input("Opción: ")
        semi = {'1': 6, '2': 15}

        if op == '0':
            break

        if op in semi:
            probarGene(semi[op], 16, congruBin)

def menuEjercicio3():
    while True:
        print("\n--- Ejercicio 3 ---")
        print("1. Semilla A (x0 = 3567345)")
        print("2. Semilla B (x0 = 1234500012)")
        print("3. Semilla C (x0 = 4567234902)")
        print("0. Volver")
        op = input("Opción: ")
        semi = {'1': 3567345, '2': 1234500012, '3': 4567234902}

        if op == '0':
            break

        if op in semi:
            probarGene(semi[op], 50, cuadMedios)

def menuEjercicio4():
    # A)
    """
    x0=7, a=5, c=24, m=32
    1) Se da que gcd(24,32)=8 != 1, entonces el
    periodo completo no se cumple porque no son coprimos
    """

    # B)
    """
    x0=8, a=9, c=13, m=32
    1) Se da que gcd(13,32)=1
    2) a=9 -> a-1=8 = 2^3
       m=32 = 2^5
       Entonces cada primo que divde a "m" también divide a "a-1"
       
    3) 4|m ∧ 4|a-1
    Por las tres condiciones anteriores, el periodo completo se cumple
    """

    # C)
    """
    x0=13, a=50, c=17, m=64
    1) Se da que gcd(17,64)=1
    2) a=50 -> a-1=49 = 7^2
       m=64 = 2^6
    Ya que 2 no divide a 49, el periodo completo no se cumple      
    """

    # D)
    """
    x0=15, a=8, c=16, m=100
    1) Se da que gcd(16,100)=4 != 1, entonces el
    periodo completo no se cumple porque no son coprimos
    """

    # E)
    """
    x0=3, a=5, c=21, m=100
    1) Se da que gcd(21,100)=1
    2) a=5 -> a-1=4 = 2^2
       m=100 = 5^2 * 2^2
    Ya que 5 no divide a 4, el periodo completo no se cumple 
    """

    while True:
        print("\n--- Ejercicio 4 ---")
        print("1. Semilla A (x0 = 7)")
        print("2. Semilla B (x0 = 8)")
        print("3. Semilla C (x0 = 13)")
        print("4. Semilla D (x0 = 15)")
        print("5. Semilla E (x0 = 3)")
        print("0. Volver")
        op = input("Opción: ")
        semi = {'1': 7, '2': 8, '3': 13, '4': 15, '5': 3}
        a = {'1': 5, '2': 9, '3': 50, '4': 8, '5': 5}
        c = {'1': 24, '2': 13, '3': 17, '4': 16, '5': 21}
        mod = {'1': 32, '2': 32, '3': 64, '4': 100, '5': 100}

        if op == '0':
            break

        if op in semi:
            probarGene(semi[op], mod[op], congruMixMulti, a[op], c[op], mod[op])

def menuEjercicio5():
    # A)
    """
    x0=7, a=5, m=64
    Como m es una potencia de 2, se debe cumplir lo siguiente:
     1) x0 es impar
     2) a ≡ 3 mod 8 ∨ a ≡ 5 mod 8
    Dado que se cumplen ambas condiciones
    El generador tiene periodo máximo posible que es m/4 = 16
    """

    # B)
    """
    x0=9, a=11, m=128
    Como m es una potencia de 2, se debe cumplir lo siguiente:
     1) x0 es impar
     2) a ≡ 3 mod 8 ∨ a ≡ 5 mod 8
    Dado que se cumplen ambas condiciones
    El generador tiene periodo máximo posible que es m/4 = 32
    """

    # C)
    """
    x0=3, a=221, m=10^3
    Como m es una potencia de 10, se debe cumplir lo siguiente:
     1) x0 no debe ser divido por 2 ni por 5 -> 2∤3 ^ 5∤3
    Por lo tanto el generador tiene el periodo máximo posible 
    de 5*10^(3-2) = 50
    """

    # D)
    """
    x0=17, a=203, m=10^5
    Como m es una potencia de 10, se debe cumplir lo siguiente:
     1) x0 no debe ser divido por 2 ni por 5 -> 2∤17 ^ 5∤17
    Por lo tanto el generador tiene el periodo máximo posible
    de 5*10^(5-2) = 5000
    """

    # E)
    """
    x0=19, a=211, m=10^8
    Como m es una potencia de 10, se debe cumplir lo siguiente:
     1) x0 no debe ser divido por 2 ni por 5 -> 2∤19 ^ 5∤19
    Por lo tanto el generador tiene el periodo máximo posible
    de 5*10^(8-2) = 5000000
    """
    
    while True:
        print("\n--- Ejercicio 5 ---")
        print("1. Semilla A (x0 = 7)")
        print("2. Semilla B (x0 = 9)")
        print("3. Semilla C (x0 = 3)")
        print("4. Semilla D (x0 = 17)")
        print("5. Semilla E (x0 = 19)")
        print("0. Volver")
        op = input("Opción: ")
        semi = {'1': 7, '2': 9, '3': 3, '4': 17, '5': 19}
        a = {'1': 5, '2': 11, '3': 221, '4': 203, '5': 211}
        mod = {'1': 64, '2': 128, '3': 1000, '4': 100000, '5': 100000000}
        maxp = {'1': 16, '2': 32, '3': 50, '4': 5000, '5': 5000000}

        if op == '0':
            break

        if op in semi:
            i=0
            s = set()
            x0 = semi[op]
            for _ in range(mod[op]):
                x0 = congruMixMulti(x0, a[op], 0, mod[op])
                if x0 in s and i == maxp[op]:
                    print(f'Cumple el periodo máximo posible de {i}')
                    break
                if gcd(x0, mod[op]) != 1:
                    print(f'No cumple el periodo máximo posible, termina en {i}')
                    break
                s.add(x0)
                i+=1

def menuEjercicio9():
    # A)
    """
    Congruencial Mixto
    x0=1: La semilla como cualquier valor entero
    a=21: Se usa 21 para satisfacer las condiciones, como
          21 ≡ 1 mod 10, el generador se comporta de forma lineal
    c=3: Tanto para cumplir con gcd(c,m)=1, como para que la 
         secuencia generada no tenga un orden aparente
    m=10
    """

    # B)
    """
    Congruencial Multiplicativo
    No se puede tener un recorrido para el rango de [0,...,9],
    solo se generan los coprimos de m
    x0=1: La semilla debe ser impar y no múltiplo de 5 
    a=3: El a debe ser coprimo con m, gcd(3,10)=1
    m=10
    """

    # C)
    """
    Congruencial Aditivo
    En el periodo se repiten números
    x0=3, x1=7: Las semillas no deben ser pares seguidos, ni múltiplos de 5
    m=10
    """

    while True:
        print("\n--- Ejercicio 9 ---")
        print("1. Congruencial Mixto")
        print("2. Congruencial Multiplicativo")
        print("3. Congruencial Aditivo")
        print("0. Volver")
        op = input("Opción: ")
        semi = 1
        a = {'1': 21, '2': 3, '3': 1}
        c = {'1': 3, '2': 0}
        mod = 10
    
        if op == '0':
            break

        if op == '1' or op == '2':
            probarGene(semi, mod, congruMixMulti, a[op], c[op], mod)

        elif op == '3':
            x0, x1 = 3, 7
            x = congruAdi(x0, x1, mod)
            for _ in range(30):
                print(f'{next(x)}', end=" ")
            print()

def menuEjercicio10():
    x0 = 71635
    while True:
        print("\n--- Ejercicio 10 ---")
        print("1. Caso A")
        print("2. Caso B")
        print("3. Caso C")
        print("4. Caso D")
        print("0. Volver")
        op = input("Opción: ")
        a, c, m = 1589013525, 1, 4294967296

        if op == '0':
            break

        if op == '1':
            # A)
            """
            n ∈ {0,...,9}
            Si n ∈ {0,1,2,3,4} -> Escudo
            Si n ∈ {5,6,7,8,9} -> Corona
            Ambos con probabilidad 0.5
            """
            n, x0 = genDigit(x0, a, c, m, 10)
            print(f'n: {n} - Escudo') if n < 5 else print(f'n: {n} - Corona')
        
        elif op == '2':
            # B)
            """
            Como cada número tiene 0.1 de probabilidad, entonces 
            a=0.1 es 1 número, b=0.4 son 4 números, c=0.5 son 5 números
            n ∈ {0,...,9}
            Si n = 9 -> a
            Si n ∈ {0,1,2,3} -> b
            Si n ∈ {4,5,6,7,8} -> c
            """
            n, x0 = genDigit(x0, a, c, m, 10)
            r = "a" if n == 9 else ("b" if n < 4 else "c")
            print(f'n: {n} - {r}')

        elif op == '3' or op == '4':
            # C) y D)
            """
            Esta lógica aplica para ambos casos, con N=10 o N=100
            Para poder generar una probabilidad de 1/6 se necesita descartar un valor
            Pasos:
            1. Sacar un número n del generador en {0,...,N-1}
            2. Si n = 0 se vuelve a sacar otro (para que queden 9 o 99), 
               en caso contrario se definen tres grupos: 
                a : 0 ≡ n mod 3
                b : 1 ≡ n mod 3
                c : 2 ≡ n mod 3

               Cada grupo tiene dos posibles caras del dado:
                El grupo a las caras {1,2}
                El grupo b las caras {3,4}
                El grupo c las caras {5,6}
                
            3. Se saca otro número z, el número que tenga la misma paridad
            que z en el grupo definido anteriormente será el elegido.
            Ejemplo: si se está en el grupo "a" y z = 9 se elige el 1.

            En la primera, la probabilidad de estar en uno de los grupos es de 1/3.
            En la segunda, la probabilidad de ser par o impar es de 1/2.
            Por tanto la probabilidad de sacar cualquier cara del dado es de
            1/3 * 1/2 = 1/6

            - Para los poliedros regulares, se pueden simular todos, para algunos haciendo este
            mismo método de rechazo y para otros dividiendo el rango en partes iguales
            """
            N = 10 if op == '3' else 100
            while True:
                n, x0 = genDigit(x0, a, c, m, N)
                if n: break

            z, x0 = genDigit(x0, a, c, m, N)
            d = (n%3)*2 + (1 if z%2 else 2)
            print(f'n: {n}, z: {z} - Dado: {d}')

def menuEjercicio11():
    # A)
    """
    x0=619375842: La semilla como cualquier valor entero [1,...,m-1]
    a=5: Es una raiz primitiva de m
    c=0: Para usar el congruencial multiplicativo, aprovechando que m es primo
    m=10^9+7
    """

    # B)
    """
    x0=284619375: La semilla como cualquier valor entero [1,...,m-1]
    a=13: Es una raiz primitiva de m
    c=0: Para usar el congruencial multiplicativo, aprovechando que m es primo
    m=10^9+9
    """

    while True:
        print("\n--- Ejercicio 11 ---")
        print("1. Caso A (m = 10^9+7)")
        print("2. Caso B (m = 10^9+9)")
        print("0. Volver")
        op = input("Opción: ")
        semi = {'1': 619375842, '2': 284619375}
        a = {'1': 5, '2': 13}
        mod = {'1': 1000000007, '2': 1000000009}

        if op == '0':
            break

        if op in semi:
            probarGene(semi[op], 30, congruMixMulti, a[op], 0, mod[op])

def main():
    while True:
        print("\n=================")
        print("      MENÚ")
        print("=================")
        print("1. Ejercicio 1")
        print("2. Ejercicio 2")
        print("3. Ejercicio 3")
        print("4. Ejercicio 4")
        print("5. Ejercicio 5")
        print("6. Ejercicio 6")
        print("7. Ejercicio 7")
        print("8. Ejercicio 8")
        print("9. Ejercicio 9")
        print("10. Ejercicio 10")
        print("11. Ejercicio 11 (Extra)")
        print("0. Salir")
        op = input("Opción: ")

        if op == '1':
            menuEjercicio1()

        elif op == '2':
            print("\n--- Ejercicio 2 ---")
            """
            Semilla x0!=0, ya que el 0 se vuelve absorbente,
            cualquier otra semilla se puede usar
            Se hace un XOR entre los bits de las posiciones 0 y 2,
            de derecha a izquierda
            """
            print("Semilla (x0 = 1)")
            probarGene(1, 32, congruBinCin)

        elif op == '3':
            menuEjercicio3()

        elif op == '4':
            menuEjercicio4()

        elif op == '5':
            menuEjercicio5()

        elif op == '6':
            print("\n--- Ejercicio 6 ---")
            """
            Recorrido de [0,...,14]
            x0=1: La semilla como cualquier valor entero
            a=16: Se usa 16 para satisfacer las condiciones, como
                  16 ≡ 1 mod 15, el generador se comporta de forma lineal
            c=4: Tanto para cumplir con gcd(c,m)=1, como para que la 
                 secuencia generada no tenga un orden aparente
            m=15: Para tomar todos los valores del rango
            """
            probarGene(1, 15, congruMixMulti, 16, 4, 15)

        elif op == '7':
            print("\n--- Ejercicio 7 ---")
            """
            x0=1: La semilla como cualquier valor entero
            a=4: Se puede usar 1, pero estadísticamente no es tan bueno
                 Se usa 4 para satisfacer las condiciones y generar más amplitud
            c=5: Tanto para cumplir con gcd(c,m)=1, como para que la 
                 secuencia generada no tenga un orden aparente
            m=9
            """
            probarGene(1, 9, congruMixMulti, 4, 5, 9)

        elif op == '8':
            print("\n--- Ejercicio 8 ---")
            """
            x0=1: La semilla como cualquier valor entero
            a=20: Se usa 20 para satisfacer las condiciones, como
                  20 ≡ 1 mod 19, el generador se comporta de forma lineal
            c=7: Tanto para cumplir con gcd(c,m)=1, como para que la 
                 secuencia generada no tenga un orden aparente
            m=19
            """
            probarGene(1, 19, congruMixMulti, 20, 7, 19)

        elif op == '9':
            menuEjercicio9()

        elif op == '10':
            menuEjercicio10()

        elif op == '11':
            menuEjercicio11()

        elif op == '0':
            break
     
if __name__ == "__main__":
    main()