### Reading RLE Files

Here is a general outlines of the strategy I used to read RLE files:
- Create a 2D list of the desired size with elements defaulting to `False`
- Skip comment lines and read the header
- Check the pattern can fit of the grid
- Read through the pattern keeping track of your x/y position. When you encounter a number keep track of this as a multiplier. When you encounter a letter, act on it a number of times equal to the multiplier and reset to one.
- When you encounter a `$`, the correct action is to increment y and reset x to 0
- When you encounter a `b` or `o` you should fill the corrsponding cell, increment x

### Updating the Grid

It is easiest to create a new grid using 

``` python
new_grid = [[None for j in range(height)]
            for i in range(width)]
```

and then fill these values as you go rather than updating the current grid in-place.

You can handle wrapping around the grid by using modular arithmetic.

``` python
valid = False
print("Will it rain today? (y/n)")
while not valid:
	res = input()
	if res in ('y', 'n'):
		valid = True
	else:
		print("Please enter one of 'y' or 'n'")
if res = 'y':
	print("Don't forget your umbrella!")
```

### Drawing the Grid

There are many ways to print the grid. If you wanted to convert to Boolean values in the grid to characters, you could use something like this:

``` python
char_grid = [['#' if cell else '.' for cell in row]
             for row in grid]
```
