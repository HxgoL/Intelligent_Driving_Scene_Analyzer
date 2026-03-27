""" Message a supprimer

En entrée tu prends une image

En sortie renvoie des objets du type: 
- BoundingBox
- DetectedObject
- SceneDetections

C'est pour faciliter les echanges entre les parties, l'agent et le llm prendront en entrée tes sorties
Si tu penses que je me suis trompé dis moi
Si tu veux rajouter des champs, des infos ou autre dis moi, j'ai juste mis le minimum vitale tu peux le faire seule aussi stv

Les infos des objets sont dans pipeline/schema.py
Il faudra faire un import (je te le fais)
"""

from pipeline.schema import BoundingBox, DetectedObject, SceneDetections
