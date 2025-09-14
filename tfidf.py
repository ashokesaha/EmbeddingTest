from gensim.models import TfidfModel
import datasource as ds
import sys

print(sys.argv[1:])
print('')

#MC = ds.MahaCorpus(['Food/cake.txt', 'Food/dosa.txt', 'Food/pizza.txt'])
MC = ds.MahaCorpus(sys.argv[1:])
MC.BuildCorpus()
D = MC.DICTIONARY()

C = MC.CORPUS()
F = MC.FILES()
model = TfidfModel(C)

for ix, _ in enumerate(C) :
    V = model[C[ix]]
    V = sorted(V, key=lambda x: x[1], reverse=True)[:20]

    print('\n\n')
    print(F[ix])
    print('------------------------------------------')
    for v in V :
        print('{:16} {}'.format(D[v[0]], v[1]))

sys.exit(0)

