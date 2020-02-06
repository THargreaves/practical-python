# -*- coding: utf-8 -*-
"""
Model solution for session one of the AZ Practical Python Course.

This script implements the ROT cipher, supplying functions both for encryption
and decryption. The solution is compatible with messages containing alphabetic
characters and spaces only, and any integer choice of rotation is valid.
Validation is performed to ensure that inputs are appropriate. Furthermore,
a selection of tests are included to verify the workings of the script. This
section can generally be ignored; it is included simply to show what best
practice looks like for developing Python scripts.

@author: Tim Hargreaves
"""


import unittest


def rot_encrypt(msg, rot=13):
    """
    Encrypt a message using the ROT cipher.

    Accepts a message and rotation and applies the ROT cipher to encrypt it.
    The message is first converted to all upper case before encrypting.

    Args:
        msg (str): The message to be encrypted.
            Must only contain alphabetic characters and spaces.
        rot (int): The number of clockwise rotations to perform for encryption.
            Defaults to 13.

    Returns:
        enc (str): The encrypted message.
            Will only contain upper case letters and spaces.

    Raises:
        TypeError: If `msg` is not a string or `rot` is not an integer.
        ValueError: If `msg` contains characters other than alphabetic
            characters and spaces.
    """
    # validate inputs
    if not isinstance(msg, str):
        raise TypeError("msg must be a string")
    if not isinstance(rot, int):
        raise TypeError("rot must be an integer")

    # handle spaces by calling the function recursively
    if ' ' in msg:
        return ' '.join(rot_encrypt(m, rot) for m in msg.split(' '))
    elif not msg.isalpha():
        raise ValueError("msg can only contain alphabet characters and spaces")

    # convert to all upper case
    msg = msg.upper()

    # convert to numeric representation (A = 0, B = 1, ...)
    num_rep = [ord(c) - 65 for c in msg]

    # encrypt
    enc_num_rep = [(n + rot) % 26 for n in num_rep]

    # convert to text
    enc = ''.join(chr(n + 65) for n in enc_num_rep)

    return enc


def rot_decrypt(msg, rot=13):
    """
    Decrypt a message using the ROT cipher.

    Accepts a message and rotation and applies the ROT cipher to decrypt it.
    This function is simply a wrapper for the `rot_encrypt` function due to
    the symmetric nature of encryption/decryption with the ROT cipher. See
    the docs for `rot_encrypt` for help with this function.
    """
    return rot_encrypt(msg, -rot)


class TestROTCipher(unittest.TestCase):
    """A class for testing the ROT cipher."""

    def test_default_rot(self):
        msg = 'SPAM'
        enc = rot_encrypt(msg)
        self.assertEqual(enc, 'FCNZ')
        self.assertEqual(msg, rot_decrypt(enc))

    def test_custom_rot(self):
        msg = 'SPAM'
        rot = 17
        enc = rot_encrypt(msg, rot)
        self.assertEqual(enc, 'JGRD')
        self.assertEqual(msg, rot_decrypt(enc, rot))

    def test_with_spaces(self):
        msg = 'SPAM EGGS SPAM'
        enc = rot_encrypt(msg)
        self.assertEqual(enc, 'FCNZ RTTF FCNZ')
        self.assertEqual(msg, rot_decrypt(enc))

    def test_lower_case(self):
        msg = 'SpAm'
        enc = rot_encrypt(msg)
        self.assertEqual(enc, 'FCNZ')
        self.assertEqual(msg.upper(), rot_decrypt(enc))

    def test_invalid_message(self):
        with self.assertRaises(TypeError):
            rot_encrypt(123)
        with self.assertRaises(ValueError):
            rot_encrypt('5PAM')

    def test_invalid_rot(self):
        with self.assertRaises(TypeError):
            rot_encrypt('SPAM', 1.23)


if __name__ == '__main__':
    unittest.main()
