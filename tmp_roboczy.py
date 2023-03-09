x = "2e"
try:
    if x == int(x):
        print(True)
    else:
        print(False)
except Exception as e:
    print(f"Wpisano stringa\n{e}")