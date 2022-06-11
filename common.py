import sys
import subprocess


def shell(cmd, cwd=None):
    """Run a shell cmd, return stdout+stderr, or raise, no need 2>&1."""
    proc = subprocess.run(cmd, shell=True, cwd=cwd,
                          stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    if proc.returncode != 0:
        raise ChildProcessError(proc.stdout.decode())
    return proc.stdout.decode()


def cprint(*objects, sep=' ', end='\n', file=sys.stdout,
           flush=False, fg=None, bg=None, style='default'):
    """colorful print.
    Color and style the string and background, then call the print function,
    Eg: cprint('pynote.net', fg='red', bg='green', style='blink')
    The other parameters are the same with stand print!
    """
    def _ct(code='0'):
        return '\033[%sm'%code

    # text color
    c = 37
    if fg in ('red','r'): c = 31
    elif fg in ('green','g'): c = 32
    elif fg in ('yellow','y'): c = 33
    elif fg in ('blue','b'): c = 34
    elif fg in ('magenta','m'): c = 35
    elif fg in ('cyan','c'): c = 36
    elif fg in ('white','w'): c = 37
    elif fg in ('black','k'): c = 30
    # background color
    b = 40
    if bg in ('red','r'): b = 41
    elif bg in ('green','g'): b = 42
    elif bg in ('yellow','y'): b = 43
    elif bg in ('blue','b'): b = 44
    elif bg in ('magenta','m'): b = 45
    elif bg in ('cyan','c'): b = 46
    elif bg in ('white','w'): b = 47
    elif bg in ('black','k'): b = 40
    # style
    a = 0
    if style == 'underline': a = 4
    elif style == 'blink': a = 5
    elif style == 'inverse': a = 7

    string = sep.join(map(str, objects))
    color = '%d;%d;%d' % (a,c,b)
    print(_ct(color)+string+_ct(), sep=sep, end=end, file=file, flush=flush)
