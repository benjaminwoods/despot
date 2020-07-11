######
despot
######

.. image:: https://readthedocs.org/projects/despot/badge/?version=latest
   :target: https://despot.readthedocs.io/en/latest/?badge=latest
   :alt: Documentation Status

**Currently in pre-alpha!**

Codify programming standards and regulations as well... code!

`despot` is a framework/tool written (primarily) in Python that allows one to
write and run metatests on packages/libraries. **Use it to get a team all on
the same page, and prevent bad code practices.**

Each metatest allows one to perform analysis on the code _itself_, rather than
the results of the code. To do this, despot leverages Radon and Pydantic. All
of which, Some typical uses include:

- Require all functions to not exceed a threshold for cyclomatic complexity
	- **Prevent accruing technical debt!**
- Require unit tests for every function
	- **Prevent cascading failures!**
- Check that your code has all of the correct dependencies, and no more
	- **Prevent overencumbered binaries!**
- Check that your code meets standards for nomenclature
	- **Hate snake case? Banish it from your code!**

*Quick example coming soon...*

## Basic principles
This is metaprogramming, through and through, but without all of the
unnecessary fluff. `despot` is designed with the following in mind:

- Code standards should be code
- Out-of-the-box, easy-to-use functionality
- Lightweight
- Extensibility and integrability, **not** disposability and conformity 

With `despot`, you can enforce code standards by writing pieces of code. Each
set of standards (or rules) is enforced by a function known as a **ruler**.
Use a `Despot` instance to organise your rulers, and deal with the results.