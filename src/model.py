from pymoc.modules import Module

class Model(object):
  def __init__(self):
    self.south_module = None
    self.north_module = None

  def keys(self):
    keys = []
    module = south_module
    while module:
      keys.append(module.key)
      module = module.north
    return keys

  def modules(self):
    modules = []
    module = south_module
    while module:
      modules.append(module)
      module = module.north
    return modules

  def get_module(self, key):
    if not key:
      return None

    module = south_module
    while module and module.key != key:
      module = module.north
    if module.key == key:
      return module
    return None

  def add_module(self, module, name, north_key=None, south_key=None):
    module = Module(
      module,
      name,
      north=self.get_module(north_key),
      south=self.get_module(south_key),
    )

    if module.north == self.south_module:
      self.south_module = module
    if module.south == self.north_module:
      self.north_module = module

  def run(self):