from django.shortcuts import render, HttpResponseRedirect
from django.http import HttpResponse
from pessoas.models import Pessoa
from django.db.models import Q #Queries complexas
from django.views.generic import ListView
from django.core import serializers


def index(request):
    return render(request, 'index.html')

def pessoaListar(request):
    pessoas = Pessoa.objects.all().order_by('-nome')[0:12]
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

def pessoaBuscarAjax(request):
        pessoas = Pessoa.objects.all()

        if request.method == 'GET':
            id_pessoa = request.GET['id']
            pessoas = Pessoa.objects.filter(Q(id__contains=id_pessoa))
            data = serializers.serialize('json', pessoas, fields=('nome', 'email', 'telefone','logradouro'))
            return HttpResponse(data, mimetype='application/json')


        return render(request, 'pessoas/buscaAjax.html', {'pessoas':pessoas})




def pessoaBuscar(request):
    
    if request.method == 'POST':
        consultando = request.POST.get('consultando', 'TUDO')
        try:
            if consultando == 'TUDO':
                pessoas = Pessoa.objects.all().order_by('-nome')
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
        '''
        pessoas = []
        consultar = Pessoa.POST['contulta']
        pessoas = '''

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
     
    