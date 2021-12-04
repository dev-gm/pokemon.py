# pokemon
An open-source pokemon game framework, written with pygame. The base functionality for a pokemon game is there, but users can download or create stories, stored in .json files, and play it. NOT FINISHED AND NO PLANS TO FINISH. NEW PROJECT AT github.com/dev-gm/pokemon

TODO:
- Add features to json parsing (4/6)
  - reusable sprites and doors DONE
  - reusable int[2] (pos or size) DONE
  - referencing them inside of the definition dict DONE
  - being able to reference reusable objects inside the "reusable" dict DONE
  - indexing them ("pos.0")
  - adding them ("pos.0+5")
- Make sure that sprites (boxes, buildings) properly show up DONE
- Add functionality for
  - pokemon battles
  - dialog
  - encounters with
    - wild pokemon
    - trainers
  - cutscenes (?)
- Create a pokemon-edit application for this version of the game, written in rust or typescript
