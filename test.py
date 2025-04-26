import time
import random
import secrets
import string
import matplotlib.pyplot as plt
from main import generate_password_with_details, fitness_types, fitness_series, fitness_unique_chars


def generate_passwords(n, password_length):
    # Character set
    characters = string.ascii_letters + string.digits + string.punctuation

    passwords_GA = [generate_password_with_details(int(password_length * 4))[0] for _ in range(n)]
    passwords_random = [''.join(random.choice(characters) for _ in range(password_length)) for _ in range(n)]
    passwords_secrets = [''.join(secrets.choice(characters) for _ in range(password_length)) for _ in range(n)]
    return passwords_GA, passwords_random, passwords_secrets

def get_time_generate_passwords(n, password_length):
    # Character set
    characters = string.ascii_letters + string.digits + string.punctuation

    start_fit = time.time()
    passwords_GA = [generate_password_with_details(int(password_length * 4))[0] for _ in range(n)]
    generate_GA = time.time() - start_fit

    start_fit = time.time()
    passwords_random = [''.join(random.choice(characters) for _ in range(password_length)) for _ in range(n)]
    generate_random = time.time() - start_fit

    start_fit = time.time()
    passwords_secrets = [''.join(secrets.choice(characters) for _ in range(password_length)) for _ in range(n)]
    generate_secrets = time.time() - start_fit

    return generate_GA/n, generate_random/n, generate_secrets/n

def passwords_strength(password_list, func):
    strengths = []
    for password in password_list:
        strengths.append(func(password))
    return strengths

def plot_passwords_hist(passwords_GA, passwords_random, passwords_secrets, func, title):
    plt.hist([passwords_strength(passwords_GA, func),
              passwords_strength(passwords_random, func),
              passwords_strength(passwords_secrets, func)],
             label=['GA', 'random', 'secrets'], alpha=0.7)
    plt.legend()

    plt.xlabel('Value')
    plt.ylabel('Frequency')
    plt.title(title)

    plt.show()


def plot_passwords_generation_time_mean(n=100, password_length_list=[4, 6, 8, 10, 12, 14]):
    times_GA = []
    times_random = []
    times_secrets = []

    for i in password_length_list:
        time_GA, time_random, time_secrets_value = get_time_generate_passwords(n, i)
        times_GA.append(time_GA)
        times_random.append(time_random)
        times_secrets.append(time_secrets_value)

    plt.figure(figsize=(8, 5))
    plt.plot(password_length_list, times_GA, marker='o', label='GA')
    plt.plot(password_length_list, times_random, marker='s', label='random')
    plt.plot(password_length_list, times_secrets, marker='^', label='secrets')
    plt.title("Mean time to generate password")
    plt.xlabel("Password length")
    plt.ylabel("Time (seconds)")
    plt.legend()
    plt.grid(True)
    plt.show()


# plot tests
def tests(passwords_GA, passwords_random, passwords_secrets):
    plot_passwords_hist(passwords_GA, passwords_random, passwords_secrets, fitness_types, "Different characters types")
    plot_passwords_hist(passwords_GA, passwords_random, passwords_secrets, fitness_series, "Different series")
    plot_passwords_hist(passwords_GA, passwords_random, passwords_secrets, fitness_unique_chars, "Unique characters")
    plot_passwords_generation_time_mean()

if __name__ == "__main__":
    n = 100
    password_length = 8
    tests(*generate_passwords(n, password_length))
