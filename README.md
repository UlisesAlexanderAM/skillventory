# Personal inventory

## Description

Web app to use a personal inventory to manage the skills needed for a job position or to keep track of the desired skills.

## Motivation

After watching/taking some courses about how to land a job and personal development I got to a format for a personal inventory that I like, the format was a simple spreadsheet that I modified a little to fit my needs. And ended up with the following columns:

- Habilidades, conocimientos, competencias encontradas en puestos que me interesan (Skills, knowledge, competences found in positions that interest me)
- Grado de confianza (Level of confidence)
- Lugares con mayor interés (Places with greater interest)

But I stumbled upon a problem, I wanted to know which skills appeared in more places with greater interest, I also wanted the skills related to a specific place with greater interest to be color-coded, so I could differentiate them from skills needed for other jobs. Another problem was that there were skills (i.e. Python) that were highly demanded in many places with greater interest so I had to add more columns to keep track of the places with greater interest where the skill was needed.

So I decided to create a web app to solve those problems and change a little the purpose and implementation of the personal inventory. Below I'll write the user stories that I want to implement, diagrams and mockups.

## User Stories

- [ ] 1 - Register a new skill/knowledge/competence

  As a person interested in keeping track of my skills/knowledge/competences in a personal inventory, User, I want to register a new skill/knowledge/competence, so I can keep track of it.

  Acceptance criteria:
  - [ ] I can register a new skill/knowledge/competence
  - [ ] The skill/knowledge/competence has a name
  - [ ] The skill/knowledge/competence has a level of confidence
    - [ ] The level of confidence is one of the following:
      - "Debo empezar a aprender o desarrollar (I needed to start learning or developing it)"
      - "Estoy aprendiendo o desarrollando (I'm learning or developing it"
      - "Tengo confianza (I'm confident)"
  - [ ] The skill/knowledge/competence has a list of places with greater interest

- [ ] 2 - Retrieve a skill/knowledge/competence

  As a user, I want to retrieve a skill/knowledge/competence, so I can show or update it.

  Acceptance criteria:
  - [ ] I can retrieve a skill/knowledge/competence

- [ ] 3 - Retrieve all skills/knowledge/competences

  As a user, I want to retrieve all skills/knowledge/competences, so I can show them.

  Acceptance criteria:
  - [ ] I can retrieve all skills/knowledge/competences

- [ ] 4 - Update a skill/knowledge/competence

  As a user, I want to update a skill/knowledge/competence, to keep it updated.

  Acceptance criteria:
  - [ ] I can update a skill/knowledge/competence name
  - [ ] I can update a skill/knowledge/competence level of confidence
  - [ ] I can update a skill/knowledge/competence places with greater interest
    - [ ] I can add a place with greater interest to a skill/knowledge/competence
    - [ ] I can remove a place with greater interest from a skill/knowledge/competence

- [ ] 5 - Register a new place with greater interest

  As a user, I want to register a new place with greater interest, so I can keep track of it.

  Acceptance criteria:
  - [ ] I can register a new place with greater interest
  - [ ] The place with greater interest has a name
  - [ ] The place with greater interest has a link to their website
  - [ ] The place with greater interest has a link to their job positions page (Optional)
  - [ ] The place with greater interest has a link to their LinkedIn page (Optional)

- [ ] 6 - Retrieve a place with greater interest
  
  As a user, I want to retrieve a place with greater interest, so I can show or update it.
  
  Acceptance criteria:
  - [ ] I can retrieve a place with greater interest

- [ ] 7 - Retrieve all places with greater interest

  As a user, I want to retrieve all places with greater interest, so I can show them.

  Acceptance criteria:
  - [ ] I can retrieve all places with greater interest

- [ ] 8 - Update a place with greater interest
  
  As a user, I want to update a place with greater interest, so I can keep it updated.
  
  Acceptance criteria:
  - [ ] I can update a place with greater interest name
  - [ ] I can update a place with greater interest link to their website
  - [ ] I can update a place with greater interest link to their job positions page
  - [ ] I can update a place with greater interest link to their LinkedIn page
