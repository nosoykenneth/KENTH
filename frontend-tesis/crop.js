import sharp from 'sharp';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

async function crop() {
    const input = 'D:/ESPE/MIC/ACTIVITIES/LOGOS/KENTHacademyblack.png';
    const output = path.join(__dirname, 'src/assets/logo-main-black.png');
    try {
        await sharp(input)
            .trim()
            .toFile(output);
        console.log("Image cropped successfully!");
    } catch(e) {
        console.error(e);
    }
}
crop();
