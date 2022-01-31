# TODO for gradebook

+ Improve bash completion. I need to add flag awareness for sub-commands.
+ There's one flake8 criticism left: 'main' in gradebook_new.py is too complex.
  (This is C901[^1].) I should break the main function down into smaller
  pieces, but I also want to keep the use of `ValueError` in the validation
  functions. I'm not sure how the result should look, so I will think it over
  before making any further changes.

[^1]: https://www.flake8rules.com/rules/C901.html
