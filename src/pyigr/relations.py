from kanren import eq, lany, lall, var
from kanren.core import Zzz

def reflexive_relation(eq=eq):
    #https://github.com/pythological/kanren/issues/33#issuecomment-801492044
    def inner(rel):
        def goal(a, b):
            return lany(
                eq(a, b),
                rel(a, b)
            )
        return goal
    return inner

def symmetric_relation(rel):
    def goal(a, b):
        return lany(
            rel(a, b),
            rel(b, a)
        )
    return goal

def transitive_relation(rel):
    def goal(a, c):
        def transitive_step(a, c):
            b = var()
            return lall(
                rel(a, b), rel(b, c)
            )

        return lany(
            rel(a, c),
            Zzz(transitive_step, a, c)
        )
    return goal

def equivalence_relation(rel,
        reflexive=True,
        symmetric=True,
        transitive=True,
        equivalence=eq):
    if transitive:
        rel = transitive_relation(rel)
    if symmetric:
        rel = symmetric_relation(rel)
    if reflexive:
        rel = reflexive_relation(equivalence)(rel)
    return rel
