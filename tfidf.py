from gensim.models import TfidfModel
import datasource as ds
import sys

MC = ds.MahaCorpus(sys.argv[1:])
MC.BuildCorpus()
D = MC.DICTIONARY()

C = MC.CORPUS()
F = MC.FILES()
model = TfidfModel(C)

print('idfs :')
print('------')
IDFSR = sorted(model.idfs.items(), key=lambda x: x[1], reverse=True)
print(IDFSR)


for ix, _ in enumerate(C) :
    V = model[C[ix]]
    V = sorted(V, key=lambda x: x[1], reverse=True)[:20]

    print('\n\n')
    print(F[ix])
    print('------------------------------------------')
    for v in V :
        tokfreq = 0
        for tok in C[ix] :
            if tok[0] == v[0] :
                tokfreq = tok[1]
                break

        print('{:16} ({:02d}/{:02d}/{})  {}'.format(D[v[0]], tokfreq, D.dfs[v[0]], D.num_docs, v[1]))

