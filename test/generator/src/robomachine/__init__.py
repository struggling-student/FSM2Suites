try:
    from StringIO import StringIO
except:
    from io import StringIO

from .parsing import parse

from .generator import Generator, DepthFirstSearchStrategy

def generate(machine, max_tests=1000, max_actions=None, to_state=None, output=None,
    strategy=DepthFirstSearchStrategy):
    generator = Generator()
    return generator.generate(machine, max_tests, max_actions, to_state, output, strategy)

def transform(text):
    output = StringIO()
    generate(parse(text), output=output)
    return output.getvalue()
