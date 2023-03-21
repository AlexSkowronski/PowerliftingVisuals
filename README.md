# PowerliftingVisuals

Would like to take in powerlifting data and create a dashboard

Need to do:

- Add gitignore and ignore **pycache**
- Perhaps use bs4 to parse through html tags and find link that way
- perhaps more elegant way of getting the zip file name
- begin cleaning the data

## Cleaning:

- For now, dropped lift event information
- Assign a unique ID to each lifter (later)
- If no entry for particular lift i.e. null value, just replaced with 0
- Calculated best 3 lifts correctly, with failing all three lifted counting for zero total
- Now check for Place, if does not count, returns False in new row, converse gives True
- Correctly assign weights to weight classes

### Bodyweight and Classes:

- Simplify weight classes for now: follow typical IPF weight classes
- If no bodyweight and class -> give average for that persons age class (harder)
- If bodyweight but no class -> Assign to correct class
- If no bodyweight but class -> Make a decision call on what class they should belong to if an overlap
- If both, bodyweight takes priority

### Division and Ages:

- Similar to above:
- AgeClass, BirthYearClass, Age, Age takes priority

###
