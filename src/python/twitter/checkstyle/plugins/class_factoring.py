import ast

from ..common import CheckstylePlugin


class ClassFactoring(CheckstylePlugin):
  """Enforces recommendations for accessing class attributes.

  Within classes, if you see:
    class Distiller(object):
      CONSTANT = "Foo"
      def foo(self, value):
         return os.path.join(Distiller.CONSTANT, value)

  recommend using self.CONSTANT instead of Distiller.CONSTANT as otherwise
  it makes subclassing impossible."""

  def iter_class_accessors(self, class_node):
    for node in ast.walk(class_node):
      if isinstance(node, ast.Attribute) and isinstance(node.value, ast.Name) and (
          node.value.id == class_node.name):
        yield node

  def nits(self):
    for class_def in self.iter_ast_types(ast.ClassDef):
      for node in self.iter_class_accessors(class_def):
        yield self.warning('T800',
            'Instead of %s.%s use self.%s or cls.%s with instancemethods and classmethods '
            'respectively.' % (class_def.name, node.attr, node.attr, node.attr),
            node)