import random
from Bio.Seq import Seq

# Paramtery stałe
POPULATION_SIZE = 10
DNA_LENGTH = 64  # 64 nukleotydy = 128 bitów = 16 znaków ASCII
STOP_LIMIT = 200
MUTATIONS_PER_INDIVIDUAL = 5

# Generowanie startowej sekwencji DNA
def generate_dna_sequence(length=64):
    return str(Seq("".join(random.choices("ATCG", k=length))))

# Funkcje mutacji
def insertion(seq):
    i = random.randint(0, len(seq))
    nt = random.choice("ATCG")
    return seq[:i] + nt + seq[i:]

def deletion(seq):
    if len(seq) <= 1:
        return seq
    i = random.randint(0, len(seq) - 1)
    return seq[:i] + seq[i + 1:]

def substitution(seq):
    if not seq:
        return seq
    i = random.randint(0, len(seq) - 1)
    new_nt = random.choice("ATCG")
    return seq[:i] + new_nt + seq[i + 1:]

def duplication(seq):
    if len(seq) < 2:
        return seq
    start = random.randint(0, len(seq) - 2)
    end = random.randint(start + 1, min(len(seq), start + 4))
    nt = seq[start:end]
    insert_at = random.randint(0, len(seq))
    return seq[:insert_at] + nt + seq[insert_at:]

def translocation(seq):
    if len(seq) < 2:
        return seq
    start = random.randint(0, len(seq) - 2)
    end = random.randint(start + 1, min(len(seq), start + 4))
    nt = seq[start:end]
    rest = seq[:start] + seq[end:]
    insert_at = random.randint(0, len(rest))
    return rest[:insert_at] + nt + rest[insert_at:]

# Losowanie i wykonywanie mutacji
def mutate_sequence(seq, mutation_count=MUTATIONS_PER_INDIVIDUAL):
    mutations = [insertion, deletion, substitution, duplication, translocation]
    for _ in range(mutation_count):
        mutation = random.choice(mutations)
        seq = mutation(seq)
    return seq

# Zapewnienie poprawnej długości hasła
def normalize_sequence(seq, length=DNA_LENGTH):
    if len(seq) > length:
        return seq[:length]
    elif len(seq) < length:
        return seq + ''.join(random.choices("ATCG", k=length - len(seq)))
    return seq

# Konwersja ciągu DNA do ASCII
def dna_to_ascii(seq):
    mapping = {'A': '00', 'C': '01', 'T': '10', 'G': '11'}
    binary_str = ''.join(mapping[nt] for nt in seq if nt in mapping)
    binary_str = binary_str[:128].ljust(128, '0')

    ascii_chars = []
    for i in range(0, 128, 8):
        byte = binary_str[i:i+8]
        value = int(byte, 2)
        value = 33 + (value % 94)  # zakres cztelnych znaków ASCII 33–126
        ascii_chars.append(chr(value))
    return ''.join(ascii_chars)

# Funkcja hasła
def fitness(dna):
    ascii_pass = dna_to_ascii(dna)
    if not ascii_pass:
        return 0
    unique_chars = len(set(ascii_pass))
    valid = all(33 <= ord(c) <= 126 for c in ascii_pass) # czy wszystkie znaki są czytelne
    return unique_chars + (10 if valid else 0) # punktacja/ocena hasła

# FUNKCJE ALGORYTMU GA
def init_population():
    return [generate_dna_sequence() for _ in range(POPULATION_SIZE)]

def mutate_population(population):
    return [mutate_sequence(ind) for ind in population]

def crossover_population(population):
    new_population = []
    for i in range(0, len(population), 2):
        if i + 1 < len(population):
            p1, p2 = population[i], population[i + 1]
            if random.random() < 0.8:
                child1, child2 = '', ''
                for a, b in zip(p1, p2):
                    if random.random() < 0.5:
                        child1 += a
                        child2 += b
                    else:
                        child1 += b
                        child2 += a
                new_population.extend([child1, child2])
            else:
                new_population.extend([p1, p2])
        else:
            new_population.append(population[i])
    return new_population

def selection(population, fitnesses):
    best = population[fitnesses.index(max(fitnesses))]
    total_fit = sum(fitnesses)
    probs = [f / total_fit for f in fitnesses]
    new_population = [best]
    for _ in range(len(population) - 1):
        pick = random.random()
        current = 0
        for ind, prob in zip(population, probs):
            current += prob
            if current > pick:
                new_population.append(ind)
                break
    return new_population

def generate_password_from_dna(dna):
    dna = normalize_sequence(dna)
    return dna_to_ascii(dna)

def genetic_algorithm():
    population = init_population()
    best = ''
    best_fitness = 0
    no_improvement = 0

    while no_improvement < STOP_LIMIT:
        population = mutate_population(population)
        population = crossover_population(population)
        fitnesses = [fitness(dna) for dna in population]

        current_best = max(fitnesses)
        if current_best > best_fitness:
            best_fitness = current_best
            best = population[fitnesses.index(current_best)]
            no_improvement = 0
        else:
            no_improvement += 1

        population = selection(population, fitnesses)

    return generate_password_from_dna(best)

# URUCHOMIENIE
if __name__ == "__main__":
    password = genetic_algorithm()
    print("Wygenerowane hasło:", password)
