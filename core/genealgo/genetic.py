"""
Created: Dec. 24 2018
The base package containing the genetic algorithm packages.
"""
import numpy as np
from typing import Dict, List, Union, Callable, Tuple


class GenericGeneticOptimizer:
    """
    The baseline optimizer using genetic algorithm.
    """

    def __init__(
        self,
        gene_pool: Dict[str, Union[object, List[object]]],
        pop_size: int,
        eval_func: Callable[Tuple[object], float],
        mode: Union["min", "max"],
        verbose: bool=False
    ) -> None:
        """
        #TODO: Docstring
        """
        assert isinstance(
            pop_size, int) and pop_size > 0, "Population size should be a positive integer."

        if verbose:
            print(f"Creating initial population: {pop_size} entities.")

        # Create initial population.
        self.population = list()
        for _ in range(pop_size):
            new_entity = dict()
            # Construct a random new entity from the gene pool.
            for (key, val) in gene_pool.items():
                # Suppose each value faces the same probability of being selected.
                val_lst = val if isinstance(val, list) else [val]
                new_entity[key] = np.random.choice(val_lst)
            self.population.append(new_entity)
        if verbose:
            print("Done.")
            unique_chromosome = self.count_unique()
            print(f"Unique entity chromosome created: {unique_chromosome}")

        # Admit fitness/evaluating function.
        self.eval_func = eval_func

        # The mode determines the correlation between fitness
        # and probability of being admitted the next generation
        # during the selection phase.
        assert mode in ["max", "min"], "Invalid optimization mode."
        self.mode = mode

        if verbose:
            print("Initial population created.")
        
    def count_unique(
        self
    ) -> int:
        """
        Count the unique chromosome in current poplation.
        This measures the varity of population gene pool.
        """
        count = np.unique(
            np.array(
                [np.array(list(entity.values())) for entity in self.population]
            ),
            axis=0
        )
        return len(count)
        
    def evaluation(
        self
    ) -> None:
        """
        Sort the current population so that the more competitive
        entities will be placed at the beginning of the sorted
        list.
        See comments below.
        """
        if self.mode == "min":
            # If this is a minimization problem, entities with 
            # lowest SCORE will be placed at the beginning of the
            # sorted population.
            self.population.sort(key=self.eval_func)
        elif self.mode == "max":
            # If this is a maximization probblem, entities with
            # highest SCORE will be placed at the beginning.
            self.population.sort(key=self.eval_func, reverse=True)

# Test
src = {
    "a": [1, 2],
    "b": [3, 4],
    "c": [1]
}

pop1 = GenericGeneticOptimizer(gene_pool=src, pop_size=10, verbose=True)



class GeneticHyperParameterTuner(GenericGeneticOptimizer):
    raise NotImplementedError