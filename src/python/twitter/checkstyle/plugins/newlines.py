import ast

from ..common import CheckstylePlugin


class Newlines(CheckstylePlugin):
  def iter_toplevel_defs(self):
    for node in self.python_file.tree.body:
      if isinstance(node, ast.FunctionDef) or isinstance(node, ast.ClassDef):
        yield node

  def previous_blank_lines(self, line_number):
    blanks = 0
    while line_number > 1:
      line_number -= 1
      line_value = self.python_file.lines[line_number].strip()
      if line_value.startswith('#'):
        continue
      if line_value:
        break
      blanks += 1
    return blanks

  def nits(self):
    for node in self.iter_toplevel_defs():
      previous_blank_lines = self.previous_blank_lines(node.lineno)
      if node.lineno > 2 and previous_blank_lines != 2:
        yield self.error('T302', 'Expected 2 blank lines, found %d' % previous_blank_lines,
            node)
    for node in self.iter_ast_types(ast.ClassDef):
      for subnode in node.body:
        if not isinstance(subnode, ast.FunctionDef):
          continue
        previous_blank_lines = self.previous_blank_lines(subnode.lineno)
        if subnode.lineno - node.lineno > 1 and previous_blank_lines != 1:
          yield self.error('T301', 'Expected 1 blank lines, found %d' % previous_blank_lines,
              subnode)