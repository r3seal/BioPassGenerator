import random
from Bio.Seq import Seq
import string

# Stałe
POPULATION_SIZE = 10
STOP_LIMIT = 200
MUTATIONS_PER_INDIVIDUAL = 5

# Generowanie startowej sekwencji DNA
def generate_dna_sequence(length):
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

# Zapewnienie poprawnej długości sekwencji DNA
def normalize_sequence(seq, dna_length):
    if len(seq) > dna_length:
        return seq[:dna_length]
    elif len(seq) < dna_length:
        return seq + ''.join(random.choices("ATCG", k=dna_length - len(seq)))
    return seq

# Konwersja ciągu DNA do ASCII
def dna_to_ascii(seq, desired_length):
    mapping = {'A': '00', 'C': '01', 'T': '10', 'G': '11'}
    binary_str = ''.join(mapping[nt] for nt in seq if nt in mapping)

    total_bits = desired_length*2
    #print(desired_length)
    binary_str = binary_str[:total_bits].ljust(total_bits, '0')

    ascii_chars = []
    for i in range(0, total_bits, 8):
        byte = binary_str[i:i+8]
        value = int(byte, 2)
        value = 33 + (value % 94)
        ascii_chars.append(chr(value))

    return ''.join(ascii_chars)

# Funkcja oceny hasła
def fitness(dna, desired_length):
    ascii_pass = dna_to_ascii(dna, desired_length)
    if not ascii_pass:
        return 0
    return (fitness_unique_chars(ascii_pass) +
            fitness_valid(ascii_pass) +
            2 * fitness_types(ascii_pass) +
            fitness_series(ascii_pass))

# Funkcje oceny haseł
def fitness_unique_chars(password):
    return len(set(password))

def fitness_valid(password):
    valid = all(33 <= ord(c) <= 126 for c in password)
    return (10 if valid else 0)

def fitness_types(password):
    has_digit = any(c.isdigit() for c in password)
    has_lower = any(c.islower() for c in password)
    has_upper = any(c.isupper() for c in password)
    has_special = any(c in string.punctuation for c in password)

    strength = sum([has_digit, has_lower, has_upper, has_special])

    return strength

def fitness_series(passwd):
    pass_len = len(passwd)
    preferred_series_count = 5
    pref_series_len = pass_len / preferred_series_count

    series = []
    current_series = passwd[0]

    for char in passwd[1:]:
        if char.isalpha() == current_series[-1].isalpha() and char.isdigit() == current_series[-1].isdigit():
            current_series += char
        else:
            series.append(current_series)
            current_series = char
    series.append(current_series)

    sum_err = sum(abs(len(s) - pref_series_len) for s in series)

    strength = pass_len ** 2 - sum_err
    if strength < 0:
        strength = 0

    return strength/10

# GA Functions
def init_population(dna_length):
    return [generate_dna_sequence(dna_length) for _ in range(POPULATION_SIZE)]

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

def generate_password_from_dna(dna, desired_length):
    dna_length = desired_length * 4
    dna = normalize_sequence(dna, dna_length)
    return dna_to_ascii(dna, desired_length)

def genetic_algorithm(desired_length):
    dna_length = desired_length * 4
    population = init_population(dna_length)
    best = ''
    best_fitness = 0
    no_improvement = 0

    while no_improvement < STOP_LIMIT:
        population = mutate_population(population)
        population = crossover_population(population)
        fitnesses = [fitness(dna, dna_length) for dna in population]

        current_best = max(fitnesses)
        if current_best > best_fitness:
            best_fitness = current_best
            best = population[fitnesses.index(current_best)]
            no_improvement = 0
        else:
            no_improvement += 1

        population = selection(population, fitnesses)

    return generate_password_from_dna(best, dna_length)

# Globalna historia
history = ""

def generate_password_with_details(desired_length):
    global history
    dna_length = desired_length
    population = init_population(dna_length)
    best = ''
    best_fitness = 0
    no_improvement = 0
    history = ""
    generation = 0

    while no_improvement < STOP_LIMIT:
        generation += 1
        history += f"\n📈 Generation {generation}:\n"
        history += "🔄 Population before mutation:\n"
        history += "\n".join(population) + "\n\n"

        population = mutate_population(population)
        history += "🔁 Population after mutation:\n"
        history += "\n".join(population) + "\n\n"

        population = crossover_population(population)
        history += "🔀 Population after crossover:\n"
        history += "\n".join(population) + "\n\n"

        fitnesses = [fitness(dna, desired_length) for dna in population]

        current_best = max(fitnesses)
        if current_best > best_fitness:
            best_fitness = current_best
            best = population[fitnesses.index(current_best)]
            no_improvement = 0
        else:
            no_improvement += 1

        population = selection(population, fitnesses)

    original_dna = best
    mutated_dna = normalize_sequence(best, dna_length)
    password = dna_to_ascii(mutated_dna, desired_length)
    print(password)

    history += "🔬 Oryginalna sekwencja DNA:\n" + original_dna + "\n\n"
    history += "🧬 Znormalizowana / zmodyfikowana sekwencja DNA:\n" + mutated_dna + "\n\n"
    history += "🔐 Wygenerowane hasło:\n" + password

    return password, history

# URUCHOMIENIE
if __name__ == "__main__":
    desired_length = 16
    password = genetic_algorithm(desired_length)
    print("Wygenerowane hasło:", password)
