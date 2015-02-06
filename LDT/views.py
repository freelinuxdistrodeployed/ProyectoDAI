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

ssh = 0
conectado = False

def index(request):
	if request.method == 'GET':
		if request.user.is_authenticated():
			usoDisco = [40,60] #consultaSSH('./usoDiscoHosts.sh')
			usoRam = [70,30] #consultaSSH('./usoRamHosts.sh')
			hardware = consultaSSH('./consultaHardware.sh')
			return render(request,'index.html',{'usuario': request.user.username,
			'discoLibre': usoDisco[0],'discoUsado': usoDisco[1] ,
			'ramLibre': usoRam[0],'ramUsada': usoRam[1],'hardwareInfo': hardware})

	if request.method == 'POST':
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
						usoDisco = [40,60] #consultaSSH('./usoDiscoHosts.sh')
						usoRam = [70,30] #consultaSSH('./usoRamHosts.sh')
						hardware = consultaSSH('./consultaHardware.sh')
						return render(request,'index.html',{'usuario': request.user.username,
						'discoLibre': usoDisco[0],'discoUsado': usoDisco[1] ,
						'ramLibre': usoRam[0],'ramUsada': usoRam[1],'hardwareInfo': hardware})

	return render(request,'index.html')

def conectarSSH():
	global ssh,conectado
	ssh = paramiko.SSHClient()
	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	ssh.connect('137.117.251.84',username='azureuser',password='Azureserver2015')
	conectado = True

def consultaSSH(comando):
	global ssh,conectado
	if not conectado:
		conectarSSH()
	else:
		if not ssh.get_transport().is_active():
			ssh.close()
			conectarSSH()

	(sshin, sshout, ssherr) = ssh.exec_command(comando)
	salida = sshout.read()
	return salida
