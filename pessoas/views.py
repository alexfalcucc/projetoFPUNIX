from django.shortcuts import render, HttpResponseRedirect
from pessoas.models import Pessoa
from django.db.models import Q #Queries complexas


def index(request):
    return render(request, 'index.html')

def pessoaListar(request):
    pessoas = Pessoa.objects.all().order_by('-nome')[2:12]
    # TESTE LOCAL PARA VERIFICAR SE A TABELA ESTA LISTANDO
    #pessoas = []
    #pessoas.append(Pessoa(nome='UNIFRAN', email='MAIL'))
    #pessoas.append(Pessoa(nome='CRUZEIRO'))
    return render(request, 'pessoas/listaPessoas.html', {'pessoas': pessoas})

def pessoaAdicionar(request):
    return render(request, 'pessoas/formPessoas.html')

def pessoaSalvar(request):
    if request.method == 'POST':
        codigo = request.POST.get('codigo', '0')

        try:
            pessoa = Pessoa.objects.get(pk=codigo)
        except:
            pessoa = Pessoa()

        pessoa.nome = request.POST.get('nome', '')
        pessoa.email = request.POST.get('email', '')
        pessoa.telefone = request.POST.get('telefone', '(00) 0-0000-0000')
        pessoa.logradouro = request.POST.get('logradouro', '')

        pessoa.save()

    return HttpResponseRedirect('/pessoas/')

def pessoaBuscar(request):
    if request.method == 'POST':
        consultando = request.POST.get('consultando', 'TUDO')
        try:
            if consultando == 'TUDO':
                pessoas = Pessoa.objects.all()
            else:
                pessoas = Pessoa.objects.filter(
                (Q(nome__contains=consultando) |
                Q(email__contains=consultando) |
                Q(telefone__contains=consultando)|
                Q(logradouro__contains=consultando))).order_by('-nome')#buscar tudo e ordena por nome
        except:
            pessoas = []

        #print cidadao

        return render(request, 'pessoas/listaPessoas.html', {'pessoas':pessoas, 'consultando':consultando})

        """pessoas = []
        consultar = Pessoa.POST['contulta']
        pessoas = """ 

def  pessoaEditar(request, pk=0):
    try:
        pessoa = Pessoa.objects.get(pk=pk)

    except:   
        return HttpResponseRedirect('/pessoas/')


    return render(request, 'pessoas/formPessoas.html', {'pessoa': pessoa})  

def pessoaExcluir(request, pk=0):
    try:
        pessoa = Pessoa.objects.get(pk=pk)
        pessoa.delete()
        return HttpResponseRedirect('/pessoas/')
    except:
        return HttpResponseRedirect('/pessoas/')
     
    