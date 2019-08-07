# TermProject

A bare bones clone of the GBA game Metroid Fusion, that I  wrote for a term project for CMU's 15-112 course.

Locally, I have been working on an updated version. Project has been on hiatus since 2016.
1. refactored version built using pygame.py 
    * levels composed from tilesets built using the Tiled Map Editor
          - layers: forground (tiles), object_layer (character animation), midground (tiles), background (image) 
          - parallax scrolling 
    * abstract player class 
          - movement of rectangular player bounding box around map
          - player physics, input control, etc
          - independent from the animation of the players character
    * per character animation (i.e., samus[player], mecha-ridley[boss], metroid[enemy], horn-toad[enemy], ..., etc) 
          - determinisitc finite autonim (dfa) used for handling transition between animated states
          - sprite animation as "sub-sprite-level"
              - instead of drawing a single sprite for each animated state, draw each body part sprite seperately
                   - for example, when changing from lazer-beam to missle, dont redraw samus's body, instead only redraw the weapon
                   - previously the weapon was backed into the sprite for samus's body, now we use a sprite-sheet of body parts, and glue them together on the fly
                
  
2. javascript version built using phaser.js
