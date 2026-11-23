from pathlib import Path
from io import BytesIO
import json
from colorsys import hsv_to_rgb
import streamlit as st
from PIL import Image, ImageOps, UnidentifiedImageError
from algoritmos.color import extraer_colores, paleta_armonica, bfs, tono, hexadecimal

ROOT = Path(__file__).parent
st.set_page_config(page_title='ColorLab | Asistente cromático', page_icon='🎨', layout='wide')
# Los estilos visuales se editan en styles/style.css.
# No necesitas tocar los algoritmos para cambiar colores o tipografía.
def cargar_estilos():
    css_path = ROOT / "styles" / "style.css"
    st.markdown(f"<style>{css_path.read_text(encoding='utf-8')}</style>", unsafe_allow_html=True)

cargar_estilos()

def seccion(num, titulo):
    st.markdown(f'<div class="section-title"><span class="num">{num}</span><span class="txt">{titulo}</span></div>', unsafe_allow_html=True)

def chips(colors, show_percent=True):
    cols=st.columns(len(colors))
    for col,c in zip(cols,colors):
        h=hexadecimal(c['rgb'])
        with col:
            meta=f"{c['porcentaje']:.2f}% · {c['frecuencia']} píxeles" if show_percent else f"RGB {c['rgb']}"
            st.markdown(f'<div class="color-card"><div class="color-chip" style="background:{h}"></div><div class="color-code">{h}</div><div class="color-meta">{meta}</div></div>',unsafe_allow_html=True)
            st.code(h,language=None)

def wheel(step, visit):
    import math
    from PIL import ImageDraw
    scale=2; size=440
    img=Image.new('RGB',(size*scale,size*scale),'#faf7ff')
    draw=ImageDraw.Draw(img)
    cx=cy=size*scale//2; rad=160*scale
    pts=[]
    for i in range(12):
        angle=math.radians(i*30-90)
        pts.append((cx+rad*math.cos(angle),cy+rad*math.sin(angle)))
    for i in range(12):
        a=pts[i];b=pts[(i+1)%12]
        draw.line((a,b),fill='#bdb0ce',width=4*scale)
    visited=set(visit[:step])
    for i,(x,y) in enumerate(pts):
        rgb=tuple(round(v*255) for v in hsv_to_rgb(i/12,.73,.94))
        r=(24 if i in visited else 17)*scale
        draw.ellipse((x-r,y-r,x+r,y+r),fill=rgb,outline='#342542' if i in visited else '#ffffff',width=5*scale)
    return img.resize((size,size),Image.Resampling.LANCZOS)

st.markdown('<div class="hero"><p class="eyebrow">Laboratorio de color · Proyecto final</p><h1>ColorLab</h1><p class="subtitle">De una imagen a una paleta con sentido. Explora los colores dominantes, descubre combinaciones armónicas y observa los algoritmos en acción.</p><div class="badges"><span class="badge">Bubble Sort</span><span class="badge">Programación dinámica</span><span class="badge">BFS</span></div></div>',unsafe_allow_html=True)
with st.sidebar:
    st.header('⚙️ Tu proyecto')
    st.write('Algoritmos: **Bubble Sort**, **programación dinámica** y **BFS**.')
    educational=st.toggle('Modo de explicación',value=False)
    st.info('La puntuación de armonía es una métrica educativa, no una medida universal de belleza.')
    st.caption('Proyecto realizado por alunmas de quinto semestre  de ingenieria en softwarea')
    st.caption('Elaboracion: **Agundez Castillo Dariana** | 2026')
    st.caption('Elaboracion: **Martinez Lopez  Yamileth** | 2026')

seccion('01','Elige tu imagen')
st.markdown('<div class="section-intro">Carga una fotografía o utiliza uno de los ejemplos. Después, pulsa <strong>Generar mi paleta</strong> para comenzar el análisis.</div>', unsafe_allow_html=True)
origin=st.radio('Origen de la imagen', ['Subir imagen','Imagen de ejemplo 1','Imagen de ejemplo 2'],horizontal=True)
if origin=='Subir imagen':
    file=st.file_uploader('Carga un archivo PNG, JPG o JPEG',type=['png','jpg','jpeg'])
else:
    file=ROOT/'assets'/('ejemplo.png' if origin.endswith('1') else 'ejemplo2.jpg')
if file is None:
    st.markdown('<div class="empty-state">📷 <strong>Aún no hay imagen.</strong><br>Sube una foto PNG o JPG, o prueba con cualquiera de las dos imágenes de ejemplo.</div>', unsafe_allow_html=True)
    st.stop()
try:
    img=Image.open(file)
    img=ImageOps.exif_transpose(img)
    img.load()
    if img.width*img.height>35_000_000:
        st.error('La imagen es demasiado grande. Usa una imagen de menos de 35 megapíxeles.')
        st.stop()
except (OSError,ValueError,UnidentifiedImageError,Image.DecompressionBombError):
    st.error('No se pudo abrir la imagen. Comprueba que sea un PNG, JPG o JPEG válido.')
    st.stop()
left,right=st.columns([1.2,1])
with left:
    st.image(img,caption='Imagen original',width='stretch')
with right:
    st.markdown('#### Información de entrada')
    st.metric('Dimensiones',f'{img.width} × {img.height}')
    st.write('El análisis reduce una copia a un máximo de **160 × 160 píxeles**, agrupa colores RGB en intervalos de 32 y conserva los cinco grupos más frecuentes.')
    generate=st.button('✨ Generar mi paleta',type='primary',width='stretch')
source_id=origin+(getattr(file,'name','') if origin=='Subir imagen' else '')
if generate:
    st.session_state['ready_source']=source_id
if st.session_state.get('ready_source')!=source_id:
    st.stop()
colors=extraer_colores(img.copy())
palette,score=paleta_armonica(colors)
start=int((tono(colors[0]['rgb'])+15)//30)%12
visit=bfs(start)
st.divider()
seccion('02','Los cinco colores dominantes')
st.caption('Ordenados de mayor a menor frecuencia mediante Bubble Sort. Cada tarjeta muestra el código HEX, porcentaje y número de píxeles.')
chips(colors)
if len(colors)<5:
    st.warning(f'Esta imagen solo contiene {len(colors)} grupos de color. No se inventan colores adicionales.')
if educational:
    st.info('**Bubble Sort:** compara dos grupos vecinos y los intercambia si el de la derecha aparece más veces. Así se ordenan de mayor a menor frecuencia. Complejidad O(g²), donde g es la cantidad de grupos.')
    st.dataframe([{'Posición':i+1,'HEX':hexadecimal(c['rgb']),'RGB':str(c['rgb']),'Píxeles':c['frecuencia'],'Porcentaje':round(c['porcentaje'],2)} for i,c in enumerate(colors)],hide_index=True,width='stretch')
seccion('03','Tu paleta armónica')
st.caption('Hasta tres colores elegidos mediante programación dinámica. La puntuación combina presencia en la imagen y cercanía de tonos.')
chips(palette,False)
a,b=st.columns(2)
a.metric('Puntuación de armonía',f'{score:.2f}')
b.metric('Colores seleccionados',len(palette))
if educational:
    st.info('**Programación dinámica:** evalúa subsecuencias de los colores dominantes, suma porcentajes y bonificaciones por cercanía de tono, y reutiliza los mejores resultados parciales. Selecciona hasta tres colores sin repetir. No examina todas las permutaciones.')
seccion('04','Grafo cromático y recorrido BFS')
st.caption('Los 12 nodos representan tonos separados por 30°. El recorrido muestra proximidad entre tonos, no posiciones de píxeles.')
step=st.slider('Explora el recorrido paso a paso',min_value=1,max_value=12,value=12)
w1,w2=st.columns([1,1])
with w1:
    st.image(wheel(step,visit),caption=f'Nodos visitados: {step} de 12',width='stretch')
with w2:
    st.write('**Nodo inicial:**',f'{start*30}°')
    st.write('**Orden de visita:**')
    st.code(' → '.join(f'{n*30}°' for n in visit[:step]),language=None)
    st.write('**Nodo actual:**',f'{visit[step-1]*30}°')
    if educational:
        st.info('**BFS (búsqueda en anchura):** utiliza una cola FIFO y un conjunto de visitados. Explora primero los vecinos del nodo actual. Cada nodo tiene dos conexiones, por lo que el recorrido cuesta O(V + E).')
seccion('05','Guarda y utiliza tu paleta')
st.caption('Copia los códigos o descarga los resultados para utilizarlos en tus diseños y documentar el proyecto.')
hexes=[hexadecimal(c['rgb']) for c in palette]
css=':root {\n'+''.join(f'  --color-{i}: {h};\n' for i,h in enumerate(hexes,1))+'}\n'
json_data={'origen':origin,'dominantes':[{'hex':hexadecimal(c['rgb']),'rgb':list(c['rgb']),'frecuencia':c['frecuencia'],'porcentaje':round(c['porcentaje'],4)} for c in colors], 'paleta_armonica':hexes,'puntuacion':round(score,4),'bfs_grados':[n*30 for n in visit]}
t1,t2=st.tabs(['Copiar códigos','Descargar archivos'])
with t1:
    st.code(' · '.join(hexes),language=None)
    st.caption('Usa el icono de copiar en el recuadro para llevar los códigos al portapapeles.')
with t2:
    c1,c2=st.columns(2)
    c1.download_button('⬇️ Descargar CSS',css,'paleta.css','text/css',width='stretch')
    c2.download_button('⬇️ Descargar JSON',json.dumps(json_data,indent=2,ensure_ascii=False),'resultados.json','application/json',width='stretch')
st.caption('ColorLab · Los colores dominantes se calculan con la misma lógica del proyecto original.')
