# pokemon
An open-source pokemon game framework, written with pygame. The base functionality for a pokemon game is there, but users can download or create stories, stored in .json files, and play it.

TODO:
- Add features to json parsing
  - reusable sprites and doors
  - reusable int[2] (pos or size)
    - indexing them ("pos.0")
    - adding them ("pos.0+5")
    - referencing them inside of the definition dict
  - being able to reference reusable objects inside the "reusable" dict
- Make sure that sprites (boxes, buildings) properly show up
- Add functionality for
  - pokemon battles
  - dialog
  - encounters with
    - wild pokemon
    - trainers
  - cutscenes (?)
- Create a pokemon-edit application for this version of the game, written in rust or typescript
