## 0.2.0 (2024-02-15)

### Feat

- **routers**: use api versioning
- **routers**: add pagination to "/skills"
- **crud**: `get_skills` return the count of skills in db
- return a message in root route
- add ability to update skill's level
- **routers.skills**: add capability to update skill's name
- **crud**: implement pagination for 'get_skills'
- add `/skills/name/skill_name` `get` path operation function
- replace `warns` and `raise` with logging messages
- add a table for domains and intermediate table for skill_domain
- add `/skills/id/{skill_id}` `get`path operation function
- add /skills post path operation function
- add funcionality for the HTTP method get of the route /skills
- add stacklevel=2 to warnings
- add function to use as dependencie in fastapi
- add a function that updates the skill's level of confidence
- add warnings
- add a function that updates the skill's name
- add a function that retrives an skill by its id
- add a function that deletes a skill from the database
- add a function that retrives an skill by its name
- raises an exeption when trying to create an existing skill
- add a function that retrieves the skills from the database
- add a function that create a skill in the database
- add sqlalchemy and pydantic models
- add settings to access the sqlite database
- add pydantic models

### Fix

- **crud**: delete test logger
- remove contextmanager decorator
- add more logging messages
- fix type hint in the function `update_skill_level_of_confidence`
- fix typo in warning
- fix the sqlalchemy models

### Refactor

- delete unused file
- modify models
- **router.skills**: remove code related to test previously removed
- **skills**: change import statements
- **data**: modify the session dependency
- **crud**: use get and first methods
- **models**: refactor the models to be more sqlmodel-like
- remove use of type aliases
- **data,database,models**: use sqlmodel
- use sqlmodel instead of pure sqlalchemy and pydantic
- use constants or variables instead of magic number 2
- create type aliases
- reorganize tests
- use type aliases
- use function `get_skill_name`where necessary
- use the `staticmethod`decorator
