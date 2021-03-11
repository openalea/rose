
lpymodimported = {}

def mylpyimport(globals, modname, *funcnames):
  from openalea.lpy import Lsystem
  global lpymodimported 
  if lpymodimported.has_key(modname):
    l = lpymodimported[modname]
  else:
    l = Lsystem(modname+'.lpy')
    lpymodimported[modname] = l
  for fname in funcnames:
    globals[fname] = l.context()[fname]
