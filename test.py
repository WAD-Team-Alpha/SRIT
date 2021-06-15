def name(s):

    # split the string into a list
    l = s.split()
    new = ""

    # traverse in the list
    for i in range(len(l)):
        s = l[i]

        # adds the capital first character
        new += (s[0].upper()+'.')

    # l[-1] gives last item of list l. We
    # use title to print first character in
    # capital.

    return new


print(name("discrete mathematics"))
