# EXP-014 — H-013 : part de l'erreur due aux bords des labels

- **Date** : 2026-11-23 · aucune inférence ; prédictions et masques d'EXP-012 (0841 × 3, 0009B, 0500P2).
- **Méthode** : bande de largeur r = dilatation(ink, r) ∖ érosion(ink, r) (carré 3×3 itéré r fois, soit 2r px de large),
  retirée de la région supervision ; r = 1, 2, 3. Contrôle : retrait aléatoire du même nombre de pixels.
  AUC protocole et AP de reader-v2, Hecate, fusion brute.
- **Code** : `analyze.py` → `results.json`. **Critère fixé avant** (EXP-010) : H-013 réfutée si ΔAUC à r = 2 < 0,03 pour
  reader-v2 ou Hecate (moyenne des 3 objets).

## Résultats (moyenne des objets, 0841 moyenné sur 3 segments)
| r | px sup. retirés | positifs retirés | ΔAUC reader-v2 | ΔAUC Hecate | ΔAUC fusion | ΔAP fusion | ΔAUC contrôle aléatoire |
|---|---|---|---|---|---|---|---|
| 1 | 1,5–2,4 % | 3,5–3,7 % | +0,005 | +0,005 | +0,005 | +0,007–0,010 | |≤ 0,0014| |
| 2 | 3,0–4,8 % | 6,9–7,4 % | **+0,010** | **+0,010** | +0,010 | +0,013–0,020 | |≤ 0,0011| |
| 3 | 4,5–7,1 % | 10,3–11,1 % | +0,015 | +0,015 | +0,014 | +0,018–0,030 | |≤ 0,0012| |

Effet très homogène entre segments, objets et modèles (ΔAUC r = 2 : 0,009–0,012 partout).

## Conclusions
- **H-013 réfutée** : exclure 2 px autour des frontières n'élève l'AUC que de 0,010 (seuil 0,03), pour les deux modèles.
  L'effet est réel (contrôle aléatoire ≈ 0) mais croît linéairement avec r (≈ 0,005 par px) au lieu de saturer : les
  erreurs ne sont pas concentrées sur le flou de bord 2,4→9 µm.
- L'erreur résiduelle (AUC 0,82–0,93) vient donc surtout de l'**intérieur** des zones encre/fond : encre manquée ou
  fausses détections franches, pas d'un désaccord de contour. Les métriques actuelles ne sont pas biaisées de façon
  notable par la résolution des labels.
- Même ampleur pour tous les modèles → la comparaison inter-modèles (EXP-002…013) n'est pas affectée par les bords.
