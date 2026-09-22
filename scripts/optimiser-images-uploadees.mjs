// Compresse automatiquement, à chaque build, les images uploadées par
// Emmanuelle via Decap CMS — sans limite de poids côté formulaire, sans
// rien changer à son geste : elle dépose un PNG ou un JPG comme toujours.
//
// La cause du poids (mesurée sur les fichiers réels du 22 sept. 2026) n'est
// pas la taille des uploads mais le fait que public/images/uploads/
// échappe totalement au pipeline d'Astro : ce dossier est copié tel quel
// dans dist/, sans aucun traitement. Deux profils différents s'y côtoient :
//   - des PNG (souvent des illustrations) : format sans perte sur du
//     contenu photographique, 65-94 % de gras à perdre selon le fichier ;
//   - des photos JPEG déjà bien compressées mais aux dimensions natives de
//     l'appareil (jusqu'à 4128 px de large) pour un affichage qui ne
//     dépasse jamais ~900 px.
//
// Cette intégration tourne en fin de build (astro:build:done), donc sur
// dist/ déjà généré — jamais sur public/. Les fichiers de Decap dans git,
// et donc ce qu'Emmanuelle voit dans sa médiathèque, ne sont JAMAIS
// modifiés : seul ce qui est effectivement servi aux visiteurs change.
//
// Pour chaque image de dist/images/uploads/ :
//   1. Un jumeau .webp est généré (redimensionné si besoin, qualité 84) —
//      c'est lui que <picture> sert en priorité (UploadImage.astro et
//      rehype-webp-uploads.mjs).
//   2. L'original est recompressé À LA MÊME URL, même extension — c'est le
//      repli pour un lien direct, un partage sur les réseaux, ou un
//      lecteur qui ignore <picture>. Lui aussi profite du build, à
//      hauteur de ce qu'un même format permet sans y perdre en fidélité.
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import sharp from 'sharp';

const DOSSIER_UPLOADS = 'images/uploads';
// Aucune image du site ne s'affiche au-delà de cette largeur — la
// redescendre est donc sans perte perceptible, quel que soit l'appareil
// photo ou le générateur d'image qui a produit le fichier d'origine.
const LARGEUR_MAX = 2000;
const QUALITE_WEBP = 84;
const EXTENSIONS_TRAITEES = new Set(['.png', '.jpg', '.jpeg']);

export default function optimiserImagesUploadees() {
  return {
    name: 'optimiser-images-uploadees',
    hooks: {
      'astro:build:done': async ({ dir, logger }) => {
        // fileURLToPath decode a la fois les % (espaces, accents) et les
        // differences Windows/POSIX — new URL(dir).pathname laisse les
        // caracteres encodes tels quels et fait echouer fs.existsSync des
        // qu'un chemin de projet contient un espace ou un accent.
        const dossier = path.join(fileURLToPath(dir), DOSSIER_UPLOADS);
        if (!fs.existsSync(dossier)) return;

        const fichiers = fs.readdirSync(dossier)
          .filter((nom) => EXTENSIONS_TRAITEES.has(path.extname(nom).toLowerCase()));
        if (!fichiers.length) return;

        let poidsAvant = 0;
        let poidsApres = 0;

        for (const nom of fichiers) {
          const chemin = path.join(dossier, nom);
          const original = fs.readFileSync(chemin);
          poidsAvant += original.length;

          // .rotate() sans argument applique la rotation dictée par le tag
          // EXIF orientation puis l'efface — indispensable pour les photos de
          // téléphone (une photo verticale y est souvent stockée en pixels
          // paysage avec l'instruction de pivoter à l'affichage). Sans lui,
          // sharp ignore le tag, l'écrit rarement dans le buffer de sortie,
          // et l'image ressort couchée sur le côté. Trouvé à la relecture,
          // sur un fichier absent de l'échantillon vérifié dans ce commit.
          const base = () => sharp(original).rotate().resize({ width: LARGEUR_MAX, withoutEnlargement: true });

          const webp = await base().webp({ quality: QUALITE_WEBP }).toBuffer();
          fs.writeFileSync(chemin.replace(/\.(png|jpe?g)$/i, '.webp'), webp);

          const extension = path.extname(nom).toLowerCase();
          const repli = extension === '.png'
            ? await base().png({ palette: true, quality: 85, effort: 8 }).toBuffer()
            : await base().jpeg({ quality: 85, mozjpeg: true }).toBuffer();
          // Ne jamais écrire un repli plus lourd que l'original (arrive sur
          // les fichiers déjà bien compressés en amont).
          fs.writeFileSync(chemin, repli.length < original.length ? repli : original);

          poidsApres += Math.min(webp.length, repli.length < original.length ? repli.length : original.length);
        }

        const gain = poidsAvant ? Math.round(100 - (100 * poidsApres) / poidsAvant) : 0;
        logger.info(
          `${fichiers.length} image(s) uploadée(s) optimisée(s) : ` +
          `${(poidsAvant / 1024 / 1024).toFixed(1)} Mo -> ${(poidsApres / 1024 / 1024).toFixed(1)} Mo (-${gain} %)`
        );
      },
    },
  };
}
