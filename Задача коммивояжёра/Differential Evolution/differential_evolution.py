from math import sqrt
import numpy as np

from random import choices, sample

from math import sqrt
import numpy as np
import matplotlib.pyplot as plt

from random import random, shuffle, choice, choices, sample

from math import sqrt
import numpy as np

from random import choices, sample

class Base:
    def euclidean_dist(self, a, b):
        return sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)

    def calculate_dist(self, dm, indx):
        dist = 0
        for i in range(len(indx) - 1):
            dist += dm[indx[i]][indx[i + 1]]
        return dist

    def distance_matrix(self, points):
        return [[self.euclidean_dist(a, b) for b in points] for a in points]

class differential_evolution(Base):
        def __init__(self, population_count, iter, c, F):
            self.population_count = population_count
            self.iter = iter
            self.c = c
            self.F = F

        def nearest_neighbor_initialization(self, n):
            populations = []
            sd = True
            for i in (sample(range(n), k=self.population_count)):
                T = []
                current_city = i
                if sd:
                    current_city = 21
                    sd = False
                visited = set([current_city])
                while len(visited) < n + 1:
                    T.append(current_city)
                    min_dist = float('inf')
                    min_city = None
                    for j in range(n):
                        if j not in visited and self.dm[current_city][j] < min_dist:
                            min_dist = self.dm[current_city][j]
                            min_city = j
                    current_city = min_city
                    visited.add(current_city)
                T.append(T[0])
                populations.append(T)
            return np.array(populations)

        def mutation(self, population, i, N):
            mas = list(range(N))
            mas.pop(i)
            r_1, r_2, r_3, r_4, r_5 = sample(mas, k=5)
            mas = np.array(mas)
            v = population[r_1] + self.F * (population[r_2] - population[r_3] + population[r_4] - population[r_5])
            return np.clip(np.round(v), 1, len(v) - 2)

        def crossing(self, n, population, v):
            u = np.full(n + 1, n)
            J_h = np.random.randint(n)

            prob = np.random.random(size=n)
            mask = np.logical_or(prob < self.c, np.arange(n) == J_h)

            index = 0
            for j in range(n):
                if mask[j] and v[j] not in u:
                    u[j] = v[j]
                else:
                    for popul in population[index:]:
                        if popul not in u:
                            u[j] = popul
                            index += 1
                            break
                        index += 1
            u[-1] = u[0]
            return u

        def get_best_road(self, population):
            best_road = population[0]
            best_score = self.calculate_dist(self.dm, population[0])
            for i in range(1, len(population)):
                if self.calculate_dist(self.dm, population[i]) < best_score:
                    best_score = self.calculate_dist(self.dm, population[i])
                    best_road = population[i]
            return best_road, best_score

        def run(self, entry):
            if len(entry[0]) == 2:
                self.dm = self.distance_matrix(entry)
                n = len(entry)
            else:
                self.dm = entry
                n = len(self.dm[0])
            if self.population_count > n:
                self.population_count = n
            population = self.nearest_neighbor_initialization(n)
            N = self.population_count
            for _ in range(self.iter):
                v = np.array([self.mutation(population, i, N) for i in range(N)])
                u = np.array([self.crossing(n, population[i], v[i]) for i in range(N)])
                distances_u = np.array([self.calculate_dist(self.dm, u[i]) for i in range(N)])
                distances_population = np.array([self.calculate_dist(self.dm, population[i]) for i in range(N)])
                mask = distances_u < distances_population
                for i in range(N):
                    if mask[i]:
                        population[i] = u[i]
            return self.get_best_road(population)