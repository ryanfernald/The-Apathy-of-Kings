# The Apathy of Kings
 Card Game for CS122 Final Project



TO-DO:

[Done]integration: separate game state variables to make tracking them easier.

[Done]bug: card in deck will auto move to the last touched card location, should be only move to card hand area if there is empty spot. [fixed]

functionality: support card isn't functional yet.

[Done]functionality: write instance or dictionary for tracking game grid if that is a card in the spot.[fixed] by modify GameControl.get_allowed_move_area() to restrict it.

[Done]bug: game grid can have more than one card in it. [fixed] by modify GameControl.get_allowed_move_area() to restrict it.

[Done]functionality: get dragon in field

[Done]functionality: get end turn button in field

[Done]functionality: find a way to switch player's action to establish final game rule

[Done]bug: card in deck should auto move to current player's hand not opponent's hand, last touched card's belonging cause logic error. [fixed] by add condition to see if that's a card in deck, then move card to allowed empty hand spot.
