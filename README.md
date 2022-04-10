
![Logo](https://pole-bfcare.com/wp-content/uploads/2022/01/3eme-datathon.jpg)


# Groupe 1 Datahon 2022
## \#Genetic VOUS IA
Défi n°1
Développer un outil de classification des variations génomiques de signification inconnue ou VOUS

Lors d'une analyse chromosomique, il y a la mise en évidence d'anomalies chromosomiques. Cela peut être une supression d'un morceau on appelle cela délétion ou alors l'ajout d'un morceau, on appelle cela gain
Pour pouvoir définir si cette énomalie peut comporter un risque pour la personne, on utilise le diagramme ci-dessous
![classification](https://i.imgur.com/yE1E1JS.png)
## Installation

Installez votre projet sur votre machine locale puis télécharger les bases de données suivantes (clic droit puis enregistrer le lien sous) 

- [DGV](http://dgv.tcag.ca/dgv/docs/DGV.GS.March2016.50percent.GainLossSep.Final.hg19.gff3)
- [RefGene](http://hgdownload.cse.ucsc.edu/goldenPath/hg19/database/refGene.txt.gz)
- [OMIM]()
Placez les dans un dossier "data" à la racine de votre projet 

## Lancement

Pour lancer le projet il faut lui indiquer les paramètres
```
chromosome:start-stop:CNV
```
Par exemple une recherche sur le chromosome 1 entre 1 et 100000 avec une délétion
```
chr1:1-100000:LOSS
```
Par exemple une recherche sur le chromosome 1 entre 1 et 100000 avec un gain
```
chr1:1-100000:GAIN
```
## Auteurs

- [@Teuira](https://github.com/Teuira/)
- [@SimonLrch](https://github.com/SimonLrch)

