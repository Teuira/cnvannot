
![Logo](https://pole-bfcare.com/wp-content/uploads/2022/01/3eme-datathon.jpg)


# Groupe 1 Datahon 2022
## \#Genetic VOUS IA
Défi n°1
Développer un outil de classification des variations génomiques de signification inconnue ou VOUS

Lors d'une analyse chromosomique, il y a la mise en évidence d'anomalies chromosomiques. Cela peut être une supression d'un morceau on appelle cela délétion ou alors l'ajout d'un morceau, on appelle cela gain
Pour pouvoir définir si cette anomalie peut comporter un risque pour la personne, on utilise le diagramme ci-dessous
On propose aussi l'intégration de l'outil X-CNV (https://github.com/kbvstmd/XCNV)
![classification](https://i.imgur.com/yE1E1JS.png)

Pour plus de rapidité nous utilisons la librairie intervalTree sur Python nous permettant de trouver des résultats en moins de 5 secondes
## Installation

Installez votre projet sur votre machine locale puis télécharger les bases de données suivantes (clic droit puis enregistrer le lien sous) 

- [DGV](http://dgv.tcag.ca/dgv/docs/DGV.GS.March2016.50percent.GainLossSep.Final.hg19.gff3)
- [RefGene](http://hgdownload.cse.ucsc.edu/goldenPath/hg19/database/refGene.txt.gz)
- [OMIM]()


Placez les dans un dossier "data" à la racine de votre projet 

## Lancement

Pour lancer le projet il faut lui indiquer les paramètres
```
reference:chromosome:start-stop:CNV
```
Par exemple une recherche sur le chromosome 1 entre 1 et 100000 avec une délétion
```
hg19:chr1:1-100000:LOSS
```
Par exemple une recherche sur le chromosome 1 entre 1 et 100000 avec un gain
```
hg19:chr1:1-100000:GAIN
```

Exemple de retour sous format JSON de la requête "chr1:1-100000:LOSS"
```
Overlap found in DGV
< 1%: Interval(61724, 346583, {'chr': 'chr1', 'start': 61724, 'stop': 346583, 'var_type': 'LOSS', 'freq': 0.3})
< 1%: Interval(60905, 97505, {'chr': 'chr1', 'start': 60905, 'stop': 97505, 'var_type': 'LOSS', 'freq': 0.61})
>= 1%: Interval(87811, 89158, {'chr': 'chr1', 'start': 87811, 'stop': 89158, 'var_type': 'LOSS', 'freq': 3.13})
END
```
Nous pouvons voir que notre programme a trouvé dans DGV 3 itérations 

Exemple de retour sous format JSON de la requête "chr1:1-100000:GAIN"
```
Overlap found in DGV
>= 1%: Interval(87433, 91967, {'chr': 'chr1', 'start': 87433, 'stop': 91967, 'var_type': 'GAIN', 'freq': 16.88})
>= 1%: Interval(13514, 91174, {'chr': 'chr1', 'start': 13514, 'stop': 91174, 'var_type': 'GAIN', 'freq': 44.78})
>= 1%: Interval(10443, 80811, {'chr': 'chr1', 'start': 10443, 'stop': 80811, 'var_type': 'GAIN', 'freq': 19.4})
>= 1%: Interval(77166, 88027, {'chr': 'chr1', 'start': 77166, 'stop': 88027, 'var_type': 'GAIN', 'freq': 27.5})
>= 1%: Interval(91470, 124563, {'chr': 'chr1', 'start': 91470, 'stop': 124563, 'var_type': 'GAIN', 'freq': 100.0})
>= 1%: Interval(49911, 222421, {'chr': 'chr1', 'start': 49911, 'stop': 222421, 'var_type': 'GAIN', 'freq': 1.13})
< 1%: Interval(60905, 97505, {'chr': 'chr1', 'start': 60905, 'stop': 97505, 'var_type': 'GAIN', 'freq': 0.61})
>= 1%: Interval(46501, 71800, {'chr': 'chr1', 'start': 46501, 'stop': 71800, 'var_type': 'GAIN', 'freq': 6.45})
>= 1%: Interval(22022, 35107, {'chr': 'chr1', 'start': 22022, 'stop': 35107, 'var_type': 'GAIN', 'freq': 30.0})
END
```

Nous pouvons voir que notre programme a trouvé dans DGV 9 itérations 
## Roadmap

- Ajout vérification DGV

- Ajout vérification refGene

- Ajout vérification OMIM

## Contributeurs

- [@Teuira](https://github.com/Teuira/)
- [@SimonLrch](https://github.com/SimonLrch)

## XCNV

Zhang L, Shi J, Ouyang J, Zhang R, Tao Y, Yuan D, Lv C, Wang R, Ning B, Roberts R, Tong W, Liu Z, Shi T. X-CNV: genome-wide prediction of the pathogenicity of copy number variations. Genome Med. 2021 Aug 18;13(1):132. doi: 10.1186/s13073-021-00945-4. PMID: 34407882
https://github.com/kbvstmd/XCNV

## License

[MIT](https://choosealicense.com/licenses/mit/)
