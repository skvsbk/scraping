def repl(st):
    #res = st
    for s in ["<p>", "</p>"]:
        # if s in st:
        #     st = st.replace(s, "")
        # else:
        #     st = st
        st = st.replace(s, "") if s in st else st
    return st

print(repl("<p>jhdecjkhekjdc</p>"))