# Lazy FCA

A big homework to merge [Lazy Learning](https://en.wikipedia.org/wiki/Lazy_learning)
and [Formal Concept Analysis](https://en.wikipedia.org/wiki/Formal_concept_analysis).
Created for the course Ordered Sets in Data Analysis (GitHub [repo](https://github.com/EgorDudyrev/OSDA_course))
taught in Data Science Master programme in HSE University, Moscow. 

# Task description

## Intention of the homework
 
This homework serves as an entry point for students into the data science world.     
So it introduces students to three main topics: 
1. **Typical machine learning project**: \
   The pipeline of loading a dataset, feature engineering, designing a new predictive algorithm, results comparison;     
2. **Lazy learning**: \
   Predicting labels for small or rapidly changing data;
4. **Rule-learning** (on part with FCA): \
   Viewing data as binary descriptions of objects (instead of points in a space of real numbers). 

## To-do list

* Basic achievements (5-6 pts.)
  * [ ] Find a dataset for binary classification:\
  _Ideal dataset would be: openly available, with various datatypes (numbers, categories, graphs, etc),
  with hundreds of rows_;
  * [ ] Describe scaling (binarization) strategy for the dataset features,
  * [ ] Describe prediction quality measure best suited for the dataset\
  _(e.g. accuracy, f1 score, or any measure that you find reasonable)_,
  * [ ] Adapt the pipeline from lazyfca.ipynb to your task.
* (Very) good solution (7-8 pts.):
  * [ ] Improve the baseline algorithm:
    * [ ] Achieve better asymptotic time complexity;
    * [ ] Improve the runtime of examples comparison:
    * [ ] Rewrite the intersections of sets into the intersection of the corresponding bitmasks. Would it make the algorithm faster?\
    _(numpy, bitarray, and other python packages may be of help)_;
    * [ ] Modify the algorithm to achieve better quality of predictions.
  * [ ] Or simply design a new lazy algorithm to beat the baseline\
  _in terms of algorithmic time complexity, runtime, and prediction quality_;
  * [ ] Compare the proposed algorithm with at least 2  popular rule-based models\
  _i.e. decision tree, random forest, XGBoost, CatBoost in terms of runtime and prediction quality_.
* Perfect solution (9-10 pts.)
  * [ ] Incorporate pattern structures into the pipeline to avoid the scaling (binarization);
  * [ ] Test the proposed algorithm on more datasets (at least 3 others);
  * [ ] Compare the proposed algorithm with at least 3  popular rule-based models.

## How to submit

Students are expected to provide the working code and pdf report for their homework by the end of the semester. 

The code should be available on the students GitHub accounts.
Please, modify [lazy_pipeline.py](https://github.com/EgorDudyrev/OSDA_course/blob/Autumn_2022/lazy_fca/lazy_pipeline.py)
script to load and to scale your dataset and to keep your proposed predictive function.
Modify [lazyfca.ipynb](https://github.com/EgorDudyrev/OSDA_course/blob/Autumn_2022/lazy_fca/lazyfca.ipynb) notebook
to run your code and produce final [Classifier_comparison](https://github.com/EgorDudyrev/OSDA_course/blob/Autumn_2022/lazy_fca/Classifier_comparison.png).

A pdf report should describe the reasoning behind every step of your homework. For example,
it should contain a description of your dataset, what quality measure you have chosen (and why), 
how did you optimize the prediction function, etc.  

## Intro to baseline algorithm

### Binary classification setup

This homework focuses on the task of binary classification. 
That is, we are given the data $X = \\{x_1, x_2, x_3, ...\\}$
and the corresponding labels $Y$ where each label $y \in Y$ is either True of False.
The task is to make a "prediction" $\hat{y}$ of a label $y \in Y$ for each datum $x \in X$ as if $y$ is unknown.

To estimate the quality of predictions we split the data $X$ into two non-overlapping sets $X_{train}$ and $X_{test}$.
Then we make make a prediction $\hat{y}$ for each test datum $x \in X_{test}$
based on the information obtained from the training data $X_{train}$. 
Finally, we measure how well predictions $\hat{y}$ represent the true test labels $y$.  

The original data $X$ often comes in various forms: numbers, categories, texts, graphs, etc.
So to make all these kinds of data look the same we scale (binarize) the dataset. 
Now we can say that there are a set of attributes $M$ where each attribute $m \in M$ is either describes $x$ or not.
That is, we replace each $x \in X$ with its binary analogue $x_{bin} \subseteq M$.


### Baseline algorithm
The following algorithm is used in the homework as a baseline algorithm for lazy FCA-based classification.
And it is called "Generators framework".

Assume that we want to make a prediction for description $x \subseteq M$ given
the set of training examples $X_{train} \subseteq 2^M$ and the labels $y_x \in \\{False, True\\}$
corresponding to each $x \in X_{train}$.

First, we split all examples $X_{train}$ to positive $X_{pos}$ and negative $X_{neg}$ examples:
$$X_{pos} = \\{x \in X_{train} \mid y_x \textrm{ is True} \\}, \quad X_{neg} = X \setminus X_{pos}.$$

To classify the descriptions $x$ we follow the procedure:
1) Count the number of counterexamples for positive examples \
For each positive example $x_{pos} \in X_{pos}$ we compute the intersection $x \cap x_{pos}$.
Then, we count the counterexamples for this intersection,
that is the number of negative examples $x_{neg} \in X_{neg}$ containing intersection $x \cap x_{pos}$;
2) Dually, count the number of counterexamples for negative examples \
For each negative example $x_{neg} \in X_{neg}$ we compute the intersection $x \cap x_{neg}$.
Then, we count the counterexamples for obtained intersection,
that is the number of positive examples $x_{pos} \in X_{pos}$ containing intersection $x \cap x_{neg}$.

Finally, we compare the average number of counterexamples for positive and negative examples. 
We classify $x$ as being positive if the number of counterexamples 
for positive examples is smaller the one for negative examples. 
