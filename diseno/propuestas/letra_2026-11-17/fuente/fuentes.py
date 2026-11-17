V={
 'bodoni':dict(link='',moda='"Bodoni Moda",Didot,serif',w='500',ls='-.01em',var='normal',adj='0.5'),
 'cormorant':dict(link='<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,500;0,600;1,500&display=swap">',moda='"Cormorant Garamond",Garamond,serif',w='600',ls='0',var='normal',adj='0.52'),
 'archivo':dict(link='<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@125,500;125,600;125,700&display=swap">',moda='"Archivo",sans-serif',w='600',ls='-.025em',var='"wdth" 125',adj='none'),
}
LOGO='<svg viewBox="0 0 20 20" aria-hidden="true">'+''.join(f'<circle cx="{10+7.5*__import__("math").cos(__import__("math").radians(-90+72*i)):.2f}" cy="{10+7.5*__import__("math").sin(__import__("math").radians(-90+72*i)):.2f}" r="{2.3 if i==4 else 1.7}" fill="{"currentColor" if i==4 else "none"}" stroke="currentColor" stroke-width="1.2"/>' for i in range(5))+'</svg>'
src=open('/Users/felipe/Documents/Ciclo K576/ciclo/app/index.html',encoding='utf8').read()
base=open('base.css',encoding='utf8').read().replace('§',':not(#q):not(#qq)')
papel='\n.app§,body§{background:#f6f2ea!important}.app .mast§{background:rgba(246,242,234,.86)!important}'.replace('§',':not(#q):not(#qq)')
for k,d in V.items():
  for pap in ([False,True] if k=='bodoni' else [False]):
    css=f':root{{--moda:{d["moda"]};--moda-w:{d["w"]};--moda-ls:{d["ls"]};--moda-var:{d["var"]};--moda-adj:{d["adj"]}}}'+base+(papel if pap else '')
    js="document.querySelectorAll('.mk').forEach(b=>b.innerHTML='"+LOGO+"<span>CICLO</span>');"
    inj=d['link']+f'<style>{css}</style><script>{js}</script>'
    i=src.rindex('</body>')
    open(f'../prop/letra_{k}{"_papel" if pap else ""}.html','w',encoding='utf8').write(src[:i]+inj+src[i:])
print('ok')
