# ANNEF

>  Artificial Neural Networks in Economic Forecasting

### About this Project

ANNEF is a project about the intermixing of economics, computer science, and statistics.

This project aims to implement various time-series prediction models in python.

And then we apply those models to economic data and compare their efficiency and accuracy on real-world data.



### How to Run Models in this Project

All backbones of models are stored in `.py `  files under `/core`  directory.

To execute certain model, one can run Jupyter notebooks in `/notebook`  directory and specify parameters within the notebook.

Detailed explanation, instruction and result visualization for a certain neural net can all be found in the corresponding Jupyter notebook.



### Packages Used in this Project

This project is a learn-by-doing project, and we used various libraries to implement our models.

#### Python

* All python codes and Jupyter notebooks are written in python 3.

* Basic python packages including `numpy`,  `scipy` and `pandas` are required.
* Statistical packages including `sklearn` and `statsmodels` .
* Machine learning libraries including `tensorflow` and `keras`.

#### Matlab

* Matlab models were developed in `MATLAB_2018a` . Please note that certain machine learning packages might not be supported in earlier versions of Matlab.



### Repository Layout

#### Main Models

* `/core`  core files
*  `/data` dataset directory
* `/notebooks`  Jupyter notebooks
* `/saved_models`  this is the default directory for TensorFlow to store models after training.
* `/tensorboard`  this is the default directory for TensorFlow to store tensor board visualization files.

#### Archived Models

* `/keras_based`  models built on `keras`  packages
* `/matlab_based`  models built on `MatLab` 