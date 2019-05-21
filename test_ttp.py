from pegpy.peg import Grammar, nez
from pegpy.ttp.typeinferance import inference

def main():
    g = Grammar('prod')
    g.load('prod.tpeg')
    parser = nez(g)
    ast = parser('1*2*3')
    print(ast)

    env = inference(g)
    print(env)

    g2 = Grammar('json')
    g2.load('json.tpeg')
    env2 = inference(g2)
    print(env2)

if __name__ == "__main__":
    main()