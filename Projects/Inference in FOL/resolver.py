def resolve(clause1, clause2):
    for literal1 in clause1:
        if literal1.startswith("¬"):
            negation = literal1[1:]
        else:
            negation = "¬" + literal1

        if negation in clause2:
            new_clause = [l for l in clause1 if l != literal1] + \
                         [l for l in clause2 if l != negation]
            return sorted(list(set(new_clause)))

    return None

print("--- Resolution Proof for Class Activity ---")

clause1 = ["Cat(Tom)"]
clause2 = ["¬Cat(Tom)", "Mammal(Tom)"]
clause3 = ["¬Mammal(Tom)", "Animal(Tom)"]
clause4 = ["¬Animal(Tom)"]

print(f"Initial clauses:")
print(f"1: {clause1}")
print(f"2: {clause2}")
print(f"3: {clause3}")
print(f"4: {clause4} (Negated Goal)")
print("-" * 20)

resolvent1 = resolve(clause3, clause4)
print(f"Step 1: Resolving {clause3} and {clause4}  ->  {resolvent1}")

if resolvent1 is not None:
    resolvent2 = resolve(clause2, resolvent1)
    print(f"Step 2: Resolving {clause2} and {resolvent1}  ->  {resolvent2}")

    if resolvent2 is not None:
        final_resolvent = resolve(clause1, resolvent2)
        print(f"Step 3: Resolving {clause1} and {resolvent2}  ->  {final_resolvent}")

        if final_resolvent == []:
            print("\nConclusion: Empty clause [] derived. The goal Animal(Tom) is proven to be true.")