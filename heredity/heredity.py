import csv
import itertools
import sys
import math

PROBS = {

    # Unconditional probabilities for having gene
    "gene": {
        2: 0.01,
        1: 0.03,
        0: 0.96
    },

    "trait": {

        # Probability of trait given two copies of gene
        2: {
            True: 0.65,
            False: 0.35
        },

        # Probability of trait given one copy of gene
        1: {
            True: 0.56,
            False: 0.44
        },

        # Probability of trait given no gene
        0: {
            True: 0.01,
            False: 0.99
        }
    },

    # Mutation probability
    "mutation": 0.01
}


def main():

    # Check for proper usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python heredity.py data.csv")
    people = load_data(sys.argv[1])

    # Keep track of gene and trait probabilities for each person
    probabilities = {
        person: {
            "gene": {
                2: 0,
                1: 0,
                0: 0
            },
            "trait": {
                True: 0,
                False: 0
            }
        }
        for person in people
    }

    # Loop over all sets of people who might have the trait
    names = set(people)
    for have_trait in powerset(names):

        # Check if current set of people violates known information
        fails_evidence = any(
            (people[person]["trait"] is not None and
             people[person]["trait"] != (person in have_trait))
            for person in names
        )
        if fails_evidence:
            continue

        # Loop over all sets of people who might have the gene
        for one_gene in powerset(names):
            for two_genes in powerset(names - one_gene):

                # Update probabilities with new joint probability
                p = joint_probability(people, one_gene, two_genes, have_trait)
                update(probabilities, one_gene, two_genes, have_trait, p)

    # Ensure probabilities sum to 1
    normalize(probabilities)

    # Print results
    for person in people:
        print(f"{person}:")
        for field in probabilities[person]:
            print(f"  {field.capitalize()}:")
            for value in probabilities[person][field]:
                p = probabilities[person][field][value]
                print(f"    {value}: {p:.4f}")


def load_data(filename):
    """
    Load gene and trait data from a file into a dictionary.
    File assumed to be a CSV containing fields name, mother, father, trait.
    mother, father must both be blank, or both be valid names in the CSV.
    trait should be 0 or 1 if trait is known, blank otherwise.
    """
    data = dict()
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"]
            data[name] = {
                "name": name,
                "mother": row["mother"] or None,
                "father": row["father"] or None,
                "trait": (True if row["trait"] == "1" else
                          False if row["trait"] == "0" else None)
            }
    return data


def powerset(s):
    """
    Return a list of all possible subsets of set s.
    """
    s = list(s)
    return [
        set(s) for s in itertools.chain.from_iterable(
            itertools.combinations(s, r) for r in range(len(s) + 1)
        )
    ]

def get_geneprob(person, people, gene_amount, info): #checked
    '''
    gets the propability of a person having a certain amount of genes, 
    if parents are involved, it handles it accordingly.
    '''
    #if person has no parents
    if people[person]["mother"] == None:
        gene_prob = PROBS["gene"][gene_amount]

    #if the person does have parents
    else:
        #gets the amount of genes that mom and dad are supposed to have
        mother = people[person]["mother"]
        mom = get_stats(mother, info)[0]

        father = people[person]["father"]
        dad = get_stats(father,info)[0]

        #gets the probability that the parent DOES pass on the gene
        pass_probs = dict()
        for gene_parent in [mom, dad]:
            if gene_parent == 0:
                pass_probs[gene_parent] = PROBS["mutation"]
            if gene_parent == 1:
                pass_probs[gene_parent] = 0.5
            if gene_parent == 2:
                pass_probs[gene_parent] =  (1 - PROBS["mutation"])

        #calculates the prob that person has x amount of genes
        if gene_amount == 0:
            #only if mom gives none and dad gives none:
            gene_prob = (1 -pass_probs[mom]) * (1 -pass_probs[dad])
        elif gene_amount == 1:
            #if mom gives none and dad gives one or vice versa:
            gene_prob = (1 -pass_probs[mom]) * pass_probs[dad] + pass_probs[mom] * (1 - pass_probs[dad])
        elif gene_amount == 2:
            #only if mom gives one and dad gives one:
            gene_prob = pass_probs[mom] * pass_probs[dad]

    return gene_prob

def get_stats(person, info):
    '''
    infers the amount of genes and which trait we're looking for
    from the trait and gene sets that we're given.
    returns a tuple with that info
    '''
    #gets the gene amount
    gene_amount = (
            2 if person in info[1] else
            1 if person in info[0] else
            0
        )
    #gets the traitval
    trait_val = person in info[2]
    
    return (gene_amount, trait_val)

def joint_probability(people, one_gene, two_genes, have_trait): #checked
    """
    Compute and return a joint probability.

    The probability returned should be the probability that
        * everyone in set `one_gene` has one copy of the gene, and
        * everyone in set `two_genes` has two copies of the gene, and
        * everyone not in `one_gene` or `two_gene` does not have the gene, and
        * everyone in set `have_trait` has the trait, and
        * everyone not in set` have_trait` does not have the trait.
    """
    #collects the factors for the final product
    joint_values = list()
    info = [one_gene, two_genes, have_trait]

    #goes by each person in people
    for person in people:
        #gets the amount of genes and the value of trait based on info
        stats = get_stats(person, info)
        #gets the gene_prob
        gene_prob = get_geneprob(person, people, stats[0], info)

        #gets the trait_prob, based on the gene amount
        trait_prob = PROBS["trait"][stats[0]][stats[1]]
        joint_values.append(gene_prob * trait_prob)
    
    return math.prod(joint_values)


def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """
    info = [one_gene, two_genes, have_trait]
    for person in probabilities:
        stats = get_stats(person, info)

        #adds p to the appropriate gene distribution
        probabilities[person]["gene"][stats[0]] += p
        #adds p to the appropriate trait distribution
        probabilities[person]["trait"][stats[1]] += p

def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """
    for person in probabilities:
        trait_total = 0
        gene_total = 0

        #gets the normal for traits
        for val in [True, False]:
            trait_total += probabilities[person]["trait"][val]
        trait_normal = 1/trait_total
        #adjusts the traits distributions
        for val in [True, False]:
            probabilities[person]["trait"][val] *=trait_normal
        
        #gets the normal for genes
        for val in [0, 1, 2]:
            gene_total += probabilities[person]["gene"][val]
        gene_normal = 1/gene_total
        #adjusts the genes distributions
        for val in [0, 1, 2]:
            probabilities[person]["gene"][val] *= gene_normal


if __name__ == "__main__":
    main()
