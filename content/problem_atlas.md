Title: An Atlas of Applied Math Problems
date: 2014-06-27
comments: true
slug: problem-atlas


The basic follow of problems in applied mathematics is as follows:

1. Find an interesting question (e.g., will this bridge collapse?, does this person have cancer?);
2. Choose a mathematical model for your question (e.g., a finite element model, use a mixture model to detect cell clusters);
3. Build an algorithm to solve your model (e.g., GMRES for large sparse FEM models, the expectation maximization algorithm for mixture models);
4. Demonstrate your model did what you expected by answering your question.

The core of Applied Mathematics is step three: building an algorithm to solve your model problem.  
Once given an objective function to maximize, it becomes a game.
Whose algorithm is fastest? 
Which provides the best solution?
How well does it preform for specific kinds of data?


A classic example of this development is that of solving linear least squares.
This is a critical step in most problems of mathematical physics.
The problems there have grown truly large.
Although general, good solutions are hard, there is a whole cottage industry devoted to building preconditioners for specific problems.


The problems are in fields where there is no clear objective function: e.g., clustering.
We all know what a cluster of points looks like, but building an algorithm to pick those out is a tricky task.
The issue generally is not so much building the algorithm, but picking the right model (better to say tweaking the model) for the task at hand.


What often motivates work in applied mathematics is a mixture of beauty and utility.
Powerful, beautiful results like the convergence of GMRES or the interlacing of eigenvalues inform vast swaths of theory.






