import json, urllib.request, sys, os.path

result_total_count = False
result_total_cidade = False
result_cidade_list_nomes = False
no_cache = False

def print_help_and_exit():
    print ("Donates do cellbit, script by tcklpl.")
    print ("Opções:")
    print ("    -t  --total      Total de donates geral.")
    print ("    -c  --city       Total por cidade, uso: -c <CIDADE> <ESTADO>.")
    print ("                     Se a cidade possuir mais de 1 palavra usar aspas: \"São Paulo\", estados são com 2 letras: SP.")
    print ("    -ln --list-names Lista os nomes. É necessário usar -c.")
    print ("    -nc --no-cache   Pega os dados da net e não do cache.")
    exit()

if len(sys.argv) == 1:
    print_help_and_exit()
else:
    i = 1
    while i < len(sys.argv):
        arg = sys.argv[i]
        if arg == "-t" or arg == "--total":
            result_total_count = True
        elif arg == "-c" or arg == "--city":
            if (i + 2) > len(sys.argv) or "-" in sys.argv[i + 1] or "-" in sys.argv[i + 2]:
                print("Por favor, use -c <CIDADE> <ESTADO>")
                exit()
            cidade = sys.argv[i + 1]
            estado = sys.argv[i + 2]
            result_total_cidade = True
            i += 2
        elif arg == "-ln" or arg == "--list-names":
            result_cidade_list_nomes = True
        elif arg == "-nc" or arg == "--no-cache":
            no_cache = True
        else:
            print ("[!!] ERRO DE SINTAXE EM: " + arg)
            print_help_and_exit()
        i += 1

if result_cidade_list_nomes and not result_total_cidade:
    print("[!!] Para listar os nomes por favor selecionar uma cidade.")
    exit()

output = None
if not no_cache:
    if os.path.exists(".cellbit_donations_cache"):
        print ("[...] Lendo os donates do cache, isso deve ser rápido...")
        with open(".cellbit_donations_cache") as f:
            output = json.load(f)
    else:
        no_cache = False

if output is None:
    print ("[...] Lendo os donates atualizados, isso pode demorar uns minutos, a lista é grande pra caralho...")
    url = "https://api.catarse.me/contributors?project_id=eq.122021"
    data = urllib.request.urlopen(url).read()
    output = json.loads(data)

if result_total_count:
    print ("[OK] Atualmente existem " + str(len(output)) + " donates.")

if result_total_cidade:
    contador_total_cidade = 0
    nomes = []
    for donate in output:
        if donate['data']['city'] == cidade and donate['data']['state'] == estado:
            contador_total_cidade += 1
            nomes.append(donate['data']['name'])

    if result_cidade_list_nomes:
        nomes_srt = sorted(nomes, key=str.casefold)
        for nome in nomes_srt:
            print ("[  ] Doador: " + nome)

    print ("[OK] Atualmente existem " + str(contador_total_cidade) + " de donates da cidade " + cidade + " " + estado)

if no_cache:
    with open(".cellbit_donations_cache", "w") as f:
        json.dump(output, f)