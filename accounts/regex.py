from re import compile, VERBOSE

# Username regex
usernameRegex = compile(r"^(\w|\.){4,50}$") # Username between 4 and 50 characters with only letters, digits, underscore, dot

# First and Last name regex
flNameRegex = compile(r"^[A-Z][a-z]{1,24}$") #Name with a capital letter and 24 other lowercase letters  

# Email regex
emailRegex = compile(r'''
    ^(\w|\.|-)+     # Local part (letters, digits, underscore, dot, hyphen)
    (@)             # @ character
    (\w|\.|-)+      # Website domain (same characters as local part)
    (\.)            # . character
    ([a-zA-Z])+$    # Top-level domain
''', VERBOSE)

# Password regex
passwordRegex = compile(r'''
    ^(?=.*[0-9])    # Must contain at least one digit
    (?=.*[a-z])     # Must contain at least one lowercase digit
    (?=.*[A-Z])     # Must contain at least one uppercase digit
    .{8,32}$        # Must be between 8 and 32 characters long
''', VERBOSE)

# Phone number regex
mkdPhoneRegex = compile(r'''
    ^(\d){3}        # First three digits
    (/)             # / separator
    (\d){3}         # Second three digits
    (-)             # - separator
    (\d){3}$        # Last three digits
''', VERBOSE)