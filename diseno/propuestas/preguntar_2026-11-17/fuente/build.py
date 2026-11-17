import sys,re
src=open('/Users/felipe/Documents/Ciclo K576/ciclo/app/index.html',encoding='utf8').read()
src=src.replace("const ltAncho=()=>Math.min(680,","const ltAncho=()=>Math.min(1e4,")
assert 'Math.min(1e4,' in src
# tras cada asPintar, la propuesta engancha lo suyo
src=src.replace("function asPintar(nuevo){","function asPintar(nuevo){setTimeout(()=>window.propPost&&!as.hist.length&&propPost(),0);",1)
src=src.replace('function moviPanel(L,titulo,signo){\n  const W=520,','function moviPanel(L,titulo,signo,Wx){\n  const W=Wx||520,');assert 'Wx||520' in src
comun=open('comun.css').read()
for p in 'abc':
  css=(comun+open(p+'.css').read()).replace('§',':not(#q):not(#qq)')
  js=open(p+'.js').read()
  inj=f"<style>{css}</style><script>{js}\nif(typeof asPintar==='function'&&$('#v-lectura')&&!$('#v-lectura').hidden)asPintar();</script>"
  i=src.rindex('</body>') if '</body>' in src else len(src)
  open(f'../prop/prop_{p}.html','w',encoding='utf8').write(src[:i]+inj+src[i:])
print('ok')
