# Video promo LAVALEX: fin de semana (vertical 9:16)

Video de motion graphics de 41 s (1080×1920, 30 fps) para anunciar la promo de fin de semana en alquiler de lavadoras. Es reutilizable porque no lleva fechas ni condiciones.

- Video final: `out/LAVALEX-promo-fin-de-semana.mp4`
- Storyboard con frames clave: `storyboard/index.html`
- Animación (fuente editable): `index.html`. Todo sale de la función `render(t)`, con una escena por bloque (`S1`…`S6`).
- Música y efectos (sintetizados, originales): `audio.py`

## Volver a renderizar

```bash
pip install imageio-ffmpeg numpy scipy
npm i playwright            # o usar una instalación global
export FFMPEG=$(python3 -c "import imageio_ffmpeg;print(imageio_ffmpeg.get_ffmpeg_exe())")
python3 audio.py                         # -> out/musica.wav
node render.mjs video                    # -> out/video-mudo.mp4
$FFMPEG -i out/video-mudo.mp4 -i out/musica.wav -c:v copy -c:a aac -b:a 192k -shortest out/LAVALEX-promo-fin-de-semana.mp4
node render.mjs shots 4.4 15.8 34.8      # capturas sueltas en shots/
```
