# wad_8D_group_project: Flash Card Master

## Description

A website for creating and sharing sets of flash cards on various subjects. The website has the following features:
  - Registration and signing in/out
  - Creating and editing your own sets of flash cards
  - Viewing other's flash card sets
  - Commenting and leaving likes on flash card sets
  - Automatically generated tests for each flash card set for testing your knowledge of topics

## Getting started
(assuming the use of Anaconda Prompt)

1. Clone the repository to a suitable location on your PC
2. Create an environment:

```
conda create -n <env_name> python=3.9
```

3. Activate the environment

```
conda activate <env_name>
```

4. Install required packages to the environment

```
pip install -r requirements.txt
```

5. Navigate into the project folder, i.e. `cd wad_8d_group_project`
6. Create the database using migrations and population script:

```
python manage.py migrate
python populate_script.py
```

7. (optional) Create a super user to access the admin features

```
python manage.py createsuperuser
```

8. Run the server

```
python manage.py runserver
```
