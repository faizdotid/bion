# Optimasi Fungsi Sphere dengan Genetic Algorithm

import numpy as np
import matplotlib.pyplot as plt
import random
from typing import List, Tuple
import warnings
warnings.filterwarnings('ignore')

# Set random seed
np.random.seed(42)
random.seed(42)

# Fungsi Sphere
def sphere_function(x: List[float]) -> float:
    """
    Fungsi Sphere: f(x) = sum(xi^2) untuk i=1 to n
    Global minimum: f(0,0,...,0) = 0
    
    Args:
        x: List of float values representing coordinates
    Returns:
        float: Function value
    """
    return sum(xi**2 for xi in x)

print("Fungsi Sphere:")
print("   f(x) = Σ(xi²) untuk i=1 to n")
print("   Global minimum: f(0,0,0,0,0) = 0")
print("   Domain: [-5.0, 5.0]^5")

# Test fungsi dengan beberapa contoh
test_points = [
    [0, 0, 0, 0, 0],
    [1, 1, 1, 1, 1], 
    [-2, 3, -1, 4, -5]
]

print("\nContoh evaluasi fungsi:")
for i, point in enumerate(test_points):
    value = sphere_function(point)
    print(f"   f({point}) = {value:.4f}")

# Implementasi Genetic Algorithm
class SimpleGeneticAlgorithm:
    """
    Implementasi Genetic Algorithm sederhana untuk optimasi fungsi
    """
    
    def __init__(self, func, dimensions: int, bounds: Tuple[float, float], 
                 population_size: int = 50, mutation_rate: float = 0.1, 
                 crossover_rate: float = 0.8):
        self.func = func
        self.dimensions = dimensions
        self.bounds = bounds
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.crossover_rate = crossover_rate
        
        # Tracking history
        self.best_fitness_history = []
        self.avg_fitness_history = []
        self.best_individual_history = []
        
    def create_individual(self) -> List[float]:
        """Membuat individu random dalam bounds yang ditentukan"""
        return [random.uniform(self.bounds[0], self.bounds[1]) 
                for _ in range(self.dimensions)]
    
    def create_population(self) -> List[List[float]]:
        """Membuat populasi awal secara random"""
        return [self.create_individual() for _ in range(self.population_size)]
    
    def evaluate_fitness(self, individual: List[float]) -> float:
        """
        Evaluasi fitness individu
        Untuk minimisasi, gunakan negative value
        """
        return -self.func(individual)
    
    def tournament_selection(self, population: List[List[float]], 
                           fitnesses: List[float], tournament_size: int = 3) -> List[float]:
        """Tournament selection untuk memilih parent"""
        tournament_indices = random.sample(range(len(population)), tournament_size)
        winner_idx = max(tournament_indices, key=lambda i: fitnesses[i])
        return population[winner_idx][:]  # Return copy
    
    def crossover(self, parent1: List[float], parent2: List[float]) -> Tuple[List[float], List[float]]:
        """Single point crossover"""
        if random.random() > self.crossover_rate:
            return parent1[:], parent2[:]
        
        crossover_point = random.randint(1, self.dimensions - 1)
        child1 = parent1[:crossover_point] + parent2[crossover_point:]
        child2 = parent2[:crossover_point] + parent1[crossover_point:]
        return child1, child2
    
    def mutate(self, individual: List[float]) -> List[float]:
        """Gaussian mutation dengan boundary handling"""
        mutated = individual[:]
        for i in range(len(mutated)):
            if random.random() < self.mutation_rate:
                # Gaussian mutation
                mutation_strength = 0.5
                mutation = random.gauss(0, mutation_strength)
                mutated[i] += mutation
                
                # Clamp ke bounds
                mutated[i] = max(self.bounds[0], min(self.bounds[1], mutated[i]))
        return mutated
    
    def evolve(self, generations: int, verbose: bool = True) -> Tuple[List[float], float]:
        """
        Main evolution loop
        
        Args:
            generations: Number of generations to evolve
            verbose: Whether to print progress
            
        Returns:
            Tuple of (best_solution, best_fitness_value)
        """
        # Initialize population
        population = self.create_population()
        
        if verbose:
            print("\nMemulai Evolusi:")
            print(f"   Population size: {self.population_size}")
            print(f"   Mutation rate: {self.mutation_rate}")
            print(f"   Crossover rate: {self.crossover_rate}")
            print(f"   Generations: {generations}")
            print("\n" + "="*60)
        
        for generation in range(generations):
            # Evaluate fitness untuk semua individu
            fitnesses = [self.evaluate_fitness(ind) for ind in population]
            
            # Track statistics
            best_fitness = max(fitnesses)
            avg_fitness = sum(fitnesses) / len(fitnesses)
            best_idx = fitnesses.index(best_fitness)
            best_individual = population[best_idx][:]
            
            # Convert back to positive untuk tracking (karena kita minimize)
            self.best_fitness_history.append(-best_fitness)
            self.avg_fitness_history.append(-avg_fitness)
            self.best_individual_history.append(best_individual)
            
            # Print progress
            if verbose and (generation % 10 == 0 or generation == generations - 1):
                print(f"Gen {generation:3d}: Best = {-best_fitness:.8f}, "
                      f"Avg = {-avg_fitness:.8f}")
            
            # Create new population
            new_population = []
            
            # Keep best individual (elitism)
            new_population.append(best_individual)
            
            # Generate rest of population
            while len(new_population) < self.population_size:
                # Selection
                parent1 = self.tournament_selection(population, fitnesses)
                parent2 = self.tournament_selection(population, fitnesses)
                
                # Crossover
                child1, child2 = self.crossover(parent1, parent2)
                
                # Mutation
                child1 = self.mutate(child1)
                child2 = self.mutate(child2)
                
                new_population.extend([child1, child2])
            
            # Trim to exact population size
            population = new_population[:self.population_size]
        
        # Return best solution
        final_fitnesses = [self.evaluate_fitness(ind) for ind in population]
        best_idx = max(range(len(final_fitnesses)), key=lambda i: final_fitnesses[i])
        return population[best_idx], -final_fitnesses[best_idx]

# Jalankan optimasi
print("\nParameter Optimasi:")
print("   Fungsi: Sphere Function")
print("   Dimensi: 5")
print("   Range: [-5.0, 5.0]")
print("   Generasi: 40")

# Inisialisasi GA
ga = SimpleGeneticAlgorithm(
    func=sphere_function,
    dimensions=5,
    bounds=(-5.0, 5.0),
    population_size=50,
    mutation_rate=0.15,
    crossover_rate=0.8
)

# Jalankan optimasi
best_solution, best_value = ga.evolve(generations=40, verbose=True)

# Hasil dan analisis
print("\n" + "="*60)
print("Hasil Optimasi:")
print("="*60)
print(f"Best solution: {[f'{x:.6f}' for x in best_solution]}")
print(f"Best value: {best_value:.10f}")
print("Global optimum: 0.0 (theoretical minimum)")
print(f"Error from global optimum: {abs(best_value - 0.0):.10f}")

# Hitung distance dari origin
distance_from_origin = np.sqrt(sum(x**2 for x in best_solution))
print(f"Distance from origin: {distance_from_origin:.8f}")

# Visualisasi konvergensi
fig, axes = plt.subplots(2, 2, figsize=(15, 10))
fig.suptitle('Genetic Algorithm - Optimasi Fungsi Sphere', fontsize=16, fontweight='bold')

# Plot 1: Best and Average Fitness
axes[0,0].plot(ga.best_fitness_history, 'b-', linewidth=2, label='Best Fitness', marker='o', markersize=3)
axes[0,0].plot(ga.avg_fitness_history, 'r--', linewidth=2, label='Average Fitness', marker='s', markersize=3)
axes[0,0].set_xlabel('Generation')
axes[0,0].set_ylabel('Fitness Value')
axes[0,0].set_title('Fitness Evolution', fontweight='bold')
axes[0,0].legend()
axes[0,0].grid(True, alpha=0.3)
axes[0,0].set_yscale('log')

# Plot 2: Best Fitness Only (Linear Scale)
axes[0,1].plot(ga.best_fitness_history, 'g-', linewidth=2, marker='o', markersize=4)
axes[0,1].set_xlabel('Generation')
axes[0,1].set_ylabel('Best Fitness Value')
axes[0,1].set_title('Best Fitness Convergence', fontweight='bold')
axes[0,1].grid(True, alpha=0.3)

# Plot 3: Konvergensi setiap dimensi
generations = range(len(ga.best_individual_history))
for dim in range(5):
    values = [ind[dim] for ind in ga.best_individual_history]
    axes[1,0].plot(generations, values, linewidth=2, label=f'Dim {dim+1}', marker='o', markersize=2)

axes[1,0].axhline(y=0, color='black', linestyle='--', alpha=0.5)
axes[1,0].set_xlabel('Generation')
axes[1,0].set_ylabel('Value')
axes[1,0].set_title('Convergence per Dimension', fontweight='bold')
axes[1,0].legend()
axes[1,0].grid(True, alpha=0.3)

# Plot 4: Improvement rate
improvements = []
for i in range(1, len(ga.best_fitness_history)):
    if ga.best_fitness_history[i] < ga.best_fitness_history[i-1]:
        improvement = ga.best_fitness_history[i-1] - ga.best_fitness_history[i]
        improvements.append(improvement)
    else:
        improvements.append(0)

axes[1,1].plot(range(1, len(ga.best_fitness_history)), improvements, 'purple', linewidth=2, marker='o', markersize=3)
axes[1,1].set_xlabel('Generation')
axes[1,1].set_ylabel('Improvement')
axes[1,1].set_title('Fitness Improvement per Generation', fontweight='bold')
axes[1,1].grid(True, alpha=0.3)

plt.tight_layout()
plt.show()
