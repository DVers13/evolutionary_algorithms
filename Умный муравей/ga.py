import time
import numpy as np
import random
from ant import Ant
class GA():
        def __init__(self, population_count, count_state ,best_solution_count, iter, coef_m, coef_c, field):
            self.population_count = population_count # [ [[[2, 0], [3, 2] ], [...]], []]
            self.count_state = count_state
            self.best_solution_count = best_solution_count
            self.iter = iter
            self.coef_m = coef_m
            self.coef_c = coef_c
            self.ant =  Ant(field)

        def initialization(self):
            automat = np.empty((self.count_state, 2, 2), dtype=int)
            states = np.arange(self.count_state)
            sample_state = np.random.permutation(states)
            for i in range(self.count_state):
                automat[i, 0] = [sample_state[i], np.random.choice([0, 1, 2])]
                automat[i, 1] = [np.random.choice(states), 2]
            return automat

        def mutation(self, crossing):
            state = [st for st in range(self.count_state)]
            for i in range(self.count_state):
                if random.random() < self.coef_m:
                    crossing[i][0][0] = random.sample(state, 1)[0]
                if random.random() < self.coef_m:
                    crossing[i][0][1] = random.sample([0, 1, 2], 1)[0]
                if random.random() < self.coef_m:
                    crossing[i][1][0] = random.sample(state, 1)[0]

            self.ant.reset()
            self.ant.run_automat(crossing)
            for state in range(self.count_state):
                if crossing[state][1][0] not in self.ant.useState:
                    crossing[state][1][0] = 0
                if crossing[state][0][0] not in self.ant.useState:
                    crossing[state][0][0] = 0
            return crossing

        def crossing(self, first, second):
            for i in range(self.count_state):
                if random.random() < self.coef_c:
                    first[i][0][0] = second[i][0][0]
                if random.random() < self.coef_c:
                    first[i][0][1] = second[i][0][1]
                if random.random() < self.coef_c:
                    first[i][1][0] = second[i][1][0]
            return first

        def get_new_population(self, population):
            new_population = [0] * self.population_count #Создается пустое новое поколение решение.
            for i in range(self.population_count):
                first, second = random.choices(list(population), k=2)#Из группы лучших решений случайным образом выбирается пара решений.
                crossing = self.crossing(first, second) # Формируется новое решение с помощью применения оператора скрещивания [4] к двум выбранным решениям.
                mutation = self.mutation(crossing) #К новому решению применяются операторы мутации [4].
                new_population[i] = mutation #Новое решение добавляется в новое поколение решений.
            return np.array(new_population)

        def get_best_solution(self, population):
            score_automats = []
            for i in range(self.population_count):
                score, _ = self.get_score(population[i])
                score_automats.append(score)
            score_automats = np.array(score_automats)
            sorted_indices = np.argsort(score_automats)
            population_sorted = [population[sort] for sort in sorted_indices]
            return population_sorted[:-self.best_solution_count]
        
        def get_best_individuals(self, population):
            score = 0
            best_automat = []
            for automat in population:
                self.ant.reset()
                self.ant.run_automat(automat)
                if self.ant.info()['score'] > score:
                    score = self.ant.info()['score']
                    best_automat = automat
            return score, best_automat
        
        def get_score(self, automat):
            self.ant.reset()
            self.ant.run_automat(automat)
            score = self.ant.info()['score']
            step = self.ant.info()['step']
            return score, step
        
        def run(self):
            pre_score = 0
            current_population = np.array([self.initialization() for _ in range(self.population_count)]) # 1. Текущее поколение решений заполняется случайными решениями.
            for e in range(self.iter):
                start_time = time.time()
                score = 0
                best_solution = self.get_best_solution(current_population)# 2. Из текущего поколения решений отбирается группа лучших решений.
                new_population = self.get_new_population(best_solution) #3. Формируется новое поколение решений
                for i in range(self.population_count):
                    new_population_score, new_population_step = self.get_score(new_population[i])
                    current_population_score, current_population_step = self.get_score(current_population[i])
                    if current_population_score < new_population_score:
                        current_population[i] = new_population[i]
                    elif (current_population_score == new_population_score) and (new_population_step < current_population_step):
                        current_population[i] = new_population[i]
                        print("es")
                    score = max(max(new_population_score, current_population_score), score)
                if score > pre_score:
                    pre_score = score
                    print(f"Epoch: {e + 1}, best_score: {score}, time: {time.time() - start_time}")
            return self.get_best_individuals(current_population)