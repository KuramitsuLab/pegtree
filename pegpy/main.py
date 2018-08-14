#!/usr/local/bin/python
import sys
from pegpy.peg import PEG

def read_inputs(a):
  try:
    f = open(a, 'rb')
    data = f.read() + b'\0'  # Zero Termination
    f.close()
    return data
  except:
    return a.encode() + b'\0' # Zero Termination

def parse(opt):
    peg = PEG()
    peg.load(opt['grammar'])
    peg.pegp()

def parse_opt(argv):
    def parse_each(a, d):
        if a[0] == '-g' and len(a) > 1:
            d['grammar'] = a[1]
            return a[2:]
        inputs = []
        for f in a:
            if not f.startswith('-'): inputs.append(f)
        d['inputs'] = inputs
        return []
    d  = {}
    while len(argv) > 0:
        argv = parse_each(argv, d)
    return d

def usage(opt):
    print("Usage: nez <command> options inputs");
    print("  -g | --grammar <file>      " + 'specify_a_grammar_file');
    print("  -s | --start <NAME>        " + 'specify_a_starting_rule');
    print("  -X                         " + 'specify_an_extension_class');
    print("  -D                         " + 'specify_an_optional_value');
    print()

    print("Example:");
    print("  nez parse -g math.tpeg <inputs>");
    print("  nez tojson -g math.tpeg <inputs>");
    print();

    print("The most commonly used nez commands are:");
    print(" parse      " + 'MainFmt.run_an_interactive_parser');
    print(" nezcc      " + 'MainFmt.generate_nez_parser');

if __name__ == "__main__":
    cmd = sys.argv[1]
    d = parse_opt(sys.argv[2:])
    names = globals()
    if cmd in names:
        names[cmd](d)
    else:
        usage(d)

'''
  st = time.time()
  t = parse(s, len(s)-1, newAST, subAST)
  et = time.time()
  sys.stderr.write(a + " " + str((et-st) * 1000.0) + "[ms]: ")
  sys.stderr.flush()
  sys.stdout.write(str(t))
  sys.stdout.flush()
  sys.stderr.write('\n')
'''