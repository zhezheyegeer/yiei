from itertools import combinations

# 定义交易记录
transactions = [
    [1, 3, 4],
    [2, 3, 5],
    [1, 2, 3, 5],
    [2, 5]
]

# 最小支持度和最小置信度
minSupport = 0.5
minConfidence = 0.7


def GetItemSetSupport(itemset, transactions):
    count = sum(set(transaction).issuperset(itemset) for transaction in transactions)
    return count / len(transactions)


def GenerateCandidates(frequentSets):
    candidates = set()
    k = len(next(iter(frequentSets)))
    if k == 1:
        for itemset1 in frequentSets:
            for itemset2 in frequentSets:
                if itemset1 != itemset2:
                    candidate = tuple(sorted(set(itemset1) | set(itemset2)))
                    if len(candidate) == k + 1:
                        candidates.add(candidate)
    else:
        for itemset1 in frequentSets:
            for itemset2 in frequentSets:
                if len(set(itemset1) & set(itemset2)) == k - 1:
                    candidate = tuple(sorted(set(itemset1) | set(itemset2)))
                    if all(tuple(sorted(subset)) in frequentSets for subset in combinations(candidate, k)):
                        candidates.add(candidate)
    return candidates


def apriori(transactions, minSupport):
    items = set(item for transaction in transactions for item in transaction)
    one_itemsets = [{item} for item in items]

    frequent_itemsets = []
    current_frequent_itemsets = [itemset for itemset in one_itemsets if
                                 GetItemSetSupport(itemset, transactions) >= minSupport]

    while current_frequent_itemsets:
        frequent_itemsets.extend(current_frequent_itemsets)
        candidates = GenerateCandidates(current_frequent_itemsets)
        current_frequent_itemsets = [candidate for candidate in candidates if
                                     GetItemSetSupport(set(candidate), transactions) >= minSupport]

    return frequent_itemsets


def GenerateAssociationRules(frequent_itemsets, transactions, minConfidence):
    associationRules = []
    for itemset in frequent_itemsets:
        subsets = [frozenset(q) for q in combinations(itemset, len(itemset) - 1)]
        for antecedent in subsets:
            consequent = itemset - antecedent
            confidence = GetItemSetSupport(itemset, transactions) / GetItemSetSupport(antecedent, transactions)
            if confidence >= minConfidence:
                associationRules.append((list(antecedent), list(consequent), confidence))
    return associationRules


# 执行Apriori算法
frequentItemSets = apriori(transactions, minSupport)
association_rules = GenerateAssociationRules([set(fi) for fi in frequentItemSets], transactions, minConfidence)

# 输出结果
print("Frequent ItemSets:")
for itemset in frequentItemSets:
    print(f"{list(itemset)} with support {GetItemSetSupport(set(itemset), transactions):.2f}")

print("\nAssociation Rules:")
for rule in association_rules:
    print(f"{rule[0]} -> {rule[1]} with confidence {rule[2]:.2f}")