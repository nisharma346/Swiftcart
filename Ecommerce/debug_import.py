import sys, traceback, importlib, os
print('cwd:', os.getcwd())
print('sys.path[0]:', sys.path[0])
print('python exe:', sys.executable)
try:
    import swiftcart
    print('swiftcart file:', getattr(swiftcart, '__file__', None))
    print('swiftcart path:', getattr(swiftcart, '__path__', None))
    if hasattr(swiftcart, '__path__'):
        print('swiftcart dir listing:', os.listdir(swiftcart.__path__[0]))
    import pkgutil, inspect
    print('pkgutil iter_modules in swiftcart.path:')
    if hasattr(swiftcart, '__path__'):
        print(list(pkgutil.iter_modules(swiftcart.__path__)))

    m = importlib.import_module('swiftcart.context_processors')
    print('Imported module:', m)
    print('module file:', getattr(m, '__file__', None))
    print('\nSource:')
    print('\n'.join(inspect.getsource(m).splitlines()))
except Exception:
    traceback.print_exc()
    sys.exit(1)
print('OK')
