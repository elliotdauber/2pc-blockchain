from systemconfig import SYSCONFIGX
import sys

def test(pk, n):
    d = SYSCONFIGX.directory
    for i in range(n):
        print("\n\n")
        pki = int(pk, 16)
        print("PK BEFORE:", pki)
        print(d.search(pki))

if __name__ == "__main__":
    test(sys.argv[1], 10)