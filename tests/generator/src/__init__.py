from .parsing import parse
from .generation import Generator
from .generation import DepthFirstSearchStrategy

__version__ = "1.0.0"
__all__ = ['parse', 'Generator', 'DepthFirstSearchStrategy', 'generate', '__version__']


def generate(machine, max_tests=1000, max_actions=None, to_state=None, output=None,
             strategy=DepthFirstSearchStrategy):
    """Generate tests for a machine (convenience function)."""
    generator = Generator()
    return generator.generate(machine, max_tests, max_actions, to_state, output, strategy)
