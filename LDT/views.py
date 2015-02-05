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

def logout(request):
	#global ssh
	auth_logout(request)
	#ssh.close()
	print "Entra en logout"
	return HttpResponseRedirect('/')

def index(request):
	if request.method == 'GET':
		if request.user.is_authenticated():
			print "!!!!!"
			return render(request,'index.html',{'usuario': request.user.username})

	if request.method == 'POST':
		print "Llamada a POST"
		if request.user.is_authenticated():
			auth_logout(request)
			return render(request,'index.html')

		else:
			formulario = AuthenticationForm(request.POST)
			if formulario.is_valid:
				usuario = request.POST['username']
				passw = request.POST['password']
				user = authenticate(username=usuario, password=passw)
				if user is not None:
					if user.is_active:
						auth_login(request, user)
						return render(request,'index.html',{'usuario': request.user.username})

	return render(request,'index.html')

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
	salida = sshout.read()
	return salida
