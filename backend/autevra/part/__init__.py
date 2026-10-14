"""Part Design: user-authored parts as an ordered feature tree, domain-neutral.

A part is a list of features applied in order. Each solid-making feature adds to, cuts
from or intersects the result so far; modifiers (shell, fillet, mirror) change the result
so far, and patterns repeat the solid feature before them. Parts live in a project next to
the parametric model and are shown, exported and undone like it.
"""
