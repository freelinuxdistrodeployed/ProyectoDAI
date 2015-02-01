from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm#,UserCreationForm
from django.contrib.auth import login, authenticate, logout
from django.core.context_processors import csrf
from django.template import RequestContext
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
import paramiko

usoDisco = './LDT/scripts/usoDisco.sh'
hardwareHosts = './LDT/scripts/hardwareHosts.sh'

ssh = 0
conectado = False


def login(request):
	print 'Entro en login'

	if request.method == 'GET':
		if request.user.is_authenticated():
			return render(request,'index.html',{'usuario': request.user.username,
			"consulta1": consultaSSH(usoDisco),"consulta2": consultaSSH(hardwareHosts)})

	if request.method == 'POST':
		print 'Entro en post'
		formulario = AuthenticationForm(request.POST)
		if formulario.is_valid :
			usuario = request.POST['username']
			contrasenia = request.POST['password']
			user = authenticate(username=usuario, password=contrasenia)
			if user is not None:
				if user.is_active:
					auth_login(request, user)
					return render(request,'index.html',{'usuario': request.user.username,
					"consulta1": consultaSSH(usoDisco),"consulta2": consultaSSH(hardwareHosts)})

	return render(request,'login.html')

def logout(request):
	global ssh
	print 'Entro en logout'
	auth_logout(request)
	ssh.close()
	return HttpResponseRedirect('/LDT/login')


def index(request):
	if request.user.is_authenticated():
		print 'Entro en index'
		global usoDisco
		if request.method == 'GET':
			print 'metodo GET'
			if request.user.is_authenticated():
				print 'El usuario esta autenticado, devuelvo index'
				return render(request,'index.html',{'usuario': request.user.username,
				"consulta1": consultaSSH(usoDisco),"consulta2": consultaSSH(hardwareHosts)})
	else:
		print 'El usuario no esta autenticado, devuelvo login'
		return render(request,'login.html')

def conectarSSH():
	global ssh,conectado
	ssh = paramiko.SSHClient()
	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	ssh.connect('137.135.177.253', username='ansibleServer', password='Azure2015')
	conectado = True

def consultaSSH(comando):
	global ssh
	if not conectado:
		conectarSSH()
	else:
		if not ssh.get_transport().is_active():
			ssh.close()
			conectarSSH()

	(sshin, sshout, ssherr) = ssh.exec_command(comando)
	print 'Realizo consulta ssh, comando:'
	print comando
	salida = sshout.read()
	print salida
	return salida
