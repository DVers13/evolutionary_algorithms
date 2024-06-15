from ant import Ant
import numpy as np
import random
import time

class GA():
        __slots__ = ("population_count", "count_state", "best_solution_count", "iter", "coef_m", "coef_c", "ant")
        def __init__(self, population_count, count_state ,best_solution_count, iter, coef_m, coef_c, field):
            self.population_count = population_count
            self.count_state = count_state
            self.best_solution_count = best_solution_count
            self.iter = iter
            self.coef_m = coef_m
            self.coef_c = coef_c
            self.ant =  Ant(field)

        def initialization(self):
            automat = np.empty((self.count_state, 3), dtype=int)
            states = np.arange(self.count_state)
            for i in range(self.count_state):
                automat[i] = [np.random.choice(states), np.random.choice([0, 1, 2]), np.random.choice(states)]
            return automat

        def mutation(self, crossing):
            state = [st for st in range(self.count_state)]
            for i in range(self.count_state):
                if random.random() < self.coef_m:
                    available_states = [st for st in state if st != crossing[i][0]]
                    crossing[i][0] = random.choice(available_states)
                if random.random() < self.coef_m:
                    crossing[i][1] = random.choice([0, 1, 2])
                if random.random() < self.coef_m:
                    available_states = [st for st in state if st != crossing[i][2]]
                    crossing[i][2] = random.choice(available_states)

            self.ant.reset()
            e, v = self.ant.run_automat(crossing)
            if e:
                for i in v:
                    available_states = [st for st in state if st != i]
                    crossing[i][0] = random.choice(available_states)
                    crossing[i][2] = random.choice(available_states)
            return crossing

        def crossing(self, first, second, th):
            for i in range(self.count_state):
                if random.random() < self.coef_c:
                    first[i][0] = second[i][0]
                elif random.random() < self.coef_c:
                    first[i][0] = th[i][0]
                if random.random() < self.coef_c:
                    first[i][1] = second[i][1]
                elif random.random() < self.coef_c:
                    first[i][1] = th[i][1]
                if random.random() < self.coef_c:
                    first[i][2] = second[i][2]
                elif random.random() < self.coef_c:
                    first[i][2] = th[i][2]
            return first

        def get_new_population(self, population):
            new_population = [0] * self.population_count
            for i in range(self.population_count):
                first, second, th = random.choices(list(population), k=3)
                crossing = self.crossing(first, second, th)
                mutation = self.mutation(crossing)
                new_population[i] = mutation
            return np.array(new_population)
        
        def get_best_solution(self, population):
            score_automats = np.zeros(self.population_count)
            for i in range(self.population_count):
                score, _ = self.get_score(population[i])
                score_automats[i] = score

            sorted_indices = np.argsort(score_automats)
            population_sorted = population[sorted_indices]
            return population_sorted[-self.best_solution_count:]
        
        def get_score(self, automat):
            self.ant.reset()
            self.ant.run_automat(automat)
            score = self.ant.info()['score']
            step = self.ant.info()['step']
            return score, step
        
        def otbor(self, population):
            score_automats = np.zeros(len(population))
            for i in range(len(population)):
                score, _ = self.get_score(population[i])
                score_automats[i] = score

            sorted_indices = np.argsort(score_automats)
            population_sorted = population[sorted_indices]
            return population_sorted[-self.population_count:]

        def run(self):
            pre_score = 0
            current_population = np.array([self.initialization() for _ in range(self.population_count * 20)])
            current_population = self.otbor(current_population)
            best_automat = None
            best_step = 9999
            с = 0
            for e in range(self.iter):
                start_time = time.time()
                best_solution = self.get_best_solution(current_population)
                new_population = self.get_new_population(best_solution)
                new_population_score_list = []
                current_population_score_list = []
                for i in range(self.population_count):
                    new_population_score, new_population_step = self.get_score(new_population[i])
                    current_population_score, current_population_step = self.get_score(current_population[i])
                    new_population_score_list.append((new_population_score, new_population_step + (89 - new_population_score), new_population[i]))
                    current_population_score_list.append((current_population_score, current_population_step + (89 - current_population_score), current_population[i]))
                combined_scores = new_population_score_list + current_population_score_list
                combined_scores.sort(key=lambda x: (-x[0], x[1]))

                selected_population = [individual for _, _, individual in combined_scores[:self.population_count]]

                current_population = np.array(selected_population)
                
                best_score = combined_scores[0][0]
                
                current_step = combined_scores[0][1] - (89 - best_score)
                
                if best_score >= pre_score and current_step <= best_step:
                    best_step = current_step
                    pre_score = best_score
                    best_automat = combined_scores[0][2]
                    print(f"Epoch: {e + 1}, best_score: {pre_score}, best_step: {best_step}, time: {time.time() - start_time}")
            print("END")
            return pre_score, best_automat