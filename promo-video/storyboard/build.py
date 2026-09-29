import html
scenes=[
 ("01","0:00 – 0:07","Entrada de logo","Una gota cae sobre fondo azul noche, salpica y las ondas se convierten en la escotilla de una lavadora que gira como un remolino. El remolino implota con un destello y el logo se arma: el contorno se dibuja, el tambor entra girando, la ola se revela, las burbujas saltan y las letras LAVALEX caen con rebote. Brillo final y aparece “Alquiler de lavadoras”.",
  "(Solo música y efectos: gota, remolino, impacto)",[("00.50","Gota"),("01.80","Remolino / escotilla"),("02.80","Estallido y dibujo del logo"),("04.40","Letras con rebote"),("05.80","Logo + tagline")]),
 ("02","0:07 – 0:13","Gancho","Ola de transición a azul marca. Titulares con golpe: “¿Montañas de ropa sucia?” mientras cae un montón de ropa. Entra la lavadora LAVALEX, la ropa vuela a la escotilla, el tambor acelera y vibra: “¡Tenemos algo para ti!”",
  "“¿Montañas de ropa sucia? Tranquilo… ¡tenemos algo para ti!”",[("08.60","Pregunta gancho"),("10.60","Entra la lavadora"),("12.20","Teaser")]),
 ("03","0:13 – 0:22","Revelación de la promo","Zoom a través de la escotilla con destello. “PROMO” golpea en amarillo con extrusión 3D y temblor de cámara, se despliega la cinta “FIN DE SEMANA”, el sello “¡No te la pierdas!” entra girando y explota confeti con “en alquiler de LAVADORAS”. Después, calendarios SÁB / DOM con sellos de check: “¡Válida solo este fin de semana!”",
  "“¡Llegó la promo de fin de semana en alquiler de lavadoras! Válida solo este fin de semana.”",[("13.60","Golpe PROMO"),("15.80","Cinta, sello y confeti"),("20.60","SÁB / DOM")]),
 ("04","0:22 – 0:29","Beneficio","Transición de burbujas a escena clara. “Tú descansas, la lavadora trabaja”: la lavadora gira con espuma y entran tres chips: ropa siempre limpia, más tiempo para ti, cero complicaciones.",
  "“Tú descansas, la lavadora trabaja.”",[("23.60","Titular"),("26.50","Chips de beneficio")]),
 ("05","0:29 – 0:36","Llamado a la acción","Barrido diagonal a azul noche. “¡Escríbenos cuanto antes!” golpea en pantalla, sube un celular con un chat: se escribe “¡Hola! Quiero la promo del fin de semana”, se envía y LAVALEX responde. Aparece el botón verde con el número y ondas de pulso.",
  "“Escríbenos cuanto antes por WhatsApp y aparta la tuya.”",[("31.50","Mensaje escribiéndose"),("34.80","Respuesta + número")]),
 ("06","0:36 – 0:41","Cierre","Destello y el logo se vuelve a armar en versión rápida, tagline, botón de WhatsApp con pulso y “¡Te esperamos!”. Segundo brillo sobre el logo y fundido.",
  "“LAVALEX, alquiler de lavadoras. ¡Te esperamos!”",[("38.50","Tarjeta final")]),
]
cards=[]
for n,tc,name,desc,vo,frames in scenes:
    fr="".join(f'<figure><img src="f_{t}.jpg" alt="{html.escape(c)} ({t} s)" loading="lazy" width="540" height="960"><figcaption><span class="tc">{t.lstrip("0") or "0"} s</span>{html.escape(c)}</figcaption></figure>' for t,c in frames)
    cards.append(f'''<section class="scene"><header><span class="num">Escena {n}</span><span class="time">{tc}</span></header>
<h2>{html.escape(name)}</h2><p class="desc">{html.escape(desc)}</p><p class="vo"><b>Locución opcional</b>{html.escape(vo)}</p>
<div class="frames">{fr}</div></section>''')
page=open('template.html').read().replace('<!--SCENES-->',"\n".join(cards))
open('index.html','w').write(page)
