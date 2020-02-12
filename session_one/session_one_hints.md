### Converting from characters to numeric representations

We can use `ord(c)` to convert a character to `c` to its numeric (ASCII) representation. This will map a capital 'A' to the value 65. We may therefore which to substract 65 from this value to have 'A' map to zero. This will make things easier since 'A' is the first character we care about and typically in programming we wish the first element of a group to have index zero.

### Encrypting

It is easiest to encrypt the message using its numeric representation. If we had the message 'CAT', the numeric representation would be [2, 0, 19]. Suppose we then used the default rotation of 13. For the 'C' and 'A' we can simply add 13 to get new numeric representations of 15 and 13 which correspond to 'R' and 'P' respectively. 'T' is more difficult. The value of 19 will become 32 after adding 13 but there isn't a 31st letter (remember 1st letter has index 0) of the alphabet. What we would like is for this addition to 'wrap round' so that any addition past 25 will roll back to 0. We can do this using modular arithmetic. Notice that that (19 + 13) % 26 = 8, giving us an 'I' as we would expect. Since taking the remainder modulo 26 has no effect on numbers in the range 0-25, we are safe to apply this in every case. Notice also that be taking the modulus rather than simply using an `if` statement to subtract 26 if we overflow, we make it so our code can accept any integer value of `rot` including those over 25 or negative.

### Converting from numeric representations to characters

Don't forget to add 65 before you try to convert back to characters.

### Decrypting

Remember that because we used modular arithmetic when encrypting, we are able to apply encryption using negative rotations. How does encryption with `rot=1` and `rot=-1` relate? Can we use this to define a decryption function in only one line by calling the encryption function?

### Handling spaces

After checking that `msg` is a string and `rot` is an integer you will want some logic as follows.

``` python
if ' ' in msg:
    # split the msg by spaces, apply encryption to each part, join with spaces, and return
elif not msg.isalpha():
    # raise error

# carry on in knowledge that there is no space in `msg`
```
