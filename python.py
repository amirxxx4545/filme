import random
import math
import itertools

def init(pop_size):
  permutations = itertools.permutations([1, 2, 3, 4, 5, 6, 7, 8])
  start = random.randint(0, 40320 - pop_size)
  stop = start + pop_size
  return list(itertools.islice(permutations, start, stop))

def print_chrom(chrom):
  for i in range(8):
    print("|", end='')
    for j in range(8):
      if j + 1 == chrom[i]:
        print(" Q |", end='')
      else:
        print("   |", end='')
    print()
    print("-----------------------------------------------------------------------------")

def one_queen_penalty(index, chrom):
  col = index
  row = chrom[index]
  penalty = 0
  for i in range(len(chrom)):
    if i == col:
      continue
    if chrom[i] < row and chrom[i] + math.fabs(col - i) == row:
      penalty = penalty + 1
    elif chrom[i] > row and chrom[i] - math.fabs(col - i) == row:
      penalty = penalty + 1
  return penalty

def configuration_penalty(chrom):
  sum = 0
  for i in range(len(chrom)):
    sum = sum + one_queen_penalty(i, chrom)
  return sum

def chrom_fitness_calculator(chrom):
  penalty = configuration_penalty(chrom)
  if penalty > 0:
    return 1 / penalty
  else:
    return 2

def selection(population, number):
  randomlist = random.sample(range(0, len(population)), number)
  selected = []
  for i in randomlist:
    selected.append(population[i])
  return selected

def get_two_parents(population):
  population.sort(reverse=True, key=chrom_fitness_calculator)
  return population[0:2]

def cross_over(parent1, parent2):
  parent1 = list(parent1)
  parent2 = list(parent2)
  position = random.randint(1, 6)
  child1 = parent1[0:position]
  child2 = parent2[0:position]
  for i in range(len(parent1)):
    if parent1[i] not in child2:
      child2.append(parent1[i])
    if parent2[i] not in child1:
      child1.append(parent2[i])
  child1 = tuple(child1)
  child2 = tuple(child2)
  return [child1, child2]

def mutation(childs):
  mutated = []
  for child in childs:
    prob = random.randint(1, 100)
    if prob < mutation_prob:
      mutated.append(mutate(child))
    else:
      mutated.append(child)
  return mutated

def mutate(chrom):
  position1 = random.randint(0, len(chrom) - 1)
  position2 = random.randint(0, len(chrom) - 1)
  chrom = list(chrom)
  temp = chrom[position1]
  chrom[position1] = chrom[position2]
  chrom[position2] = temp
  chrom = tuple(chrom)
  return chrom

def survival_selection(population, childs):
  population.sort(reverse=True, key=chrom_fitness_calculator)
  population[-1] = childs[0]
  population[-2] = childs[1]
  if chrom_fitness_calculator(childs[0]) == 2:
    return (1, population)
  if chrom_fitness_calculator(childs[1]) == 2:
    return (2, population)
  return (0, population)

pop_size = 100
select_random = 5
mutation_prob = 80
pop = init(pop_size)
rounds = 10000
TOTAL_ROUNDS = rounds

while rounds > 0:
  selected = selection(pop, select_random)
  parents = get_two_parents(selected)
  childs = cross_over(parents[0], parents[1])
  childs = mutation(childs)
  done, pop = survival_selection(pop, childs)
  if done == 1:
    print("Best 10 answers after {0} iterations:".format(TOTAL_ROUNDS - rounds))
    pop.sort(reverse=True, key=chrom_fitness_calculator)
    print(pop[0:10])
    print("Best answer:")
    print(childs[0])
    print_chrom(childs[0])
    break
  if done == 2:
    print("Best 10 answers after {0} iterations:".format(TOTAL_ROUNDS - rounds))
    pop.sort(reverse=True, key=chrom_fitness_calculator)
    print(pop[0:10])
    print('--------------------------------------------------------')
    print("Best answer:")
    
    print(childs[1])
    print_chrom(childs[1])
    break
  rounds = rounds - 1

if rounds <= 0:
  pop.sort(reverse=True, key=chrom_fitness_calculator)
  print("Best answer at the end:")
  print(pop[0])
  print_chrom(pop[0])