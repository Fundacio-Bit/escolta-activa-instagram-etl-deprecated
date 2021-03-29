### *Escolta Activa*'s *instagram_etl* repository ###

It contains code of the Instagram ETL scripts required in the Escolta Activa project

It is shared with you under the MIT license.

### Installation and execution ###

<a name="prerequisites"></a>
* Prerequisites:

- Miniconda
- An environment variable INSTAGRAM_API_KEY containing the API key value.
    

* Create the Conda environment from the cloned repository (delete previously created environments to ensure that you
have the most updated version):

```console
conda remove --name escolta_activa_instagram_etl --all
conda env create -f setup_env.yml
```
You can check if the environment was deployed correctly using:

```console
conda list
```

You can find useful conda environment management instructions at its documentation:

https://conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html


* Execute the extractor via command line with:

```console 
python get_posts.py
```

### Contact info and support ###

We cannot provide support to users of this repository. Feel free to use it at you own risk and under the license
conditions. In any case, we will be glad to receive your questions and comments at
[turisme@fundaciobit.org](mailto:turisme@fundaciobit.org) and will do our best to answer them whenever possible.

