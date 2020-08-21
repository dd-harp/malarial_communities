Overview
========

There is an Overleaf document describing the work.
The computational steps here are:

 1. Find cities in input high-resolution settlement layer (HRSL) data.

 2. Create a settlement map with population and pfpr for every settlement.

 3. Apply a movement model to the full settlement map.

    a. Movement of people, ignoring malaria.

    b. Movement of hazard from mosquito bites, so
       that areas without malaria are included.

    c. Movement of PfPR-generated hazard of malaria.

 4. Reduce the movement model to movement among cities
    that retains equivalent rates of movement.

 5. Find communities within the cities.
