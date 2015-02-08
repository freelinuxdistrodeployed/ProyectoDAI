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
			usoDisco = consultaSSH('./usoDiscoHosts.sh')
			usoDisco = usoDisco.split( )
			usoDisco[1] = int(usoDisco[1]) - int(usoDisco[0])
			usoDisco[0] = int(usoDisco[0])/1024
			usoDisco[1] = int(usoDisco[1])/1024
			usoRam = consultaSSH('./usoRamHosts.sh')
			usoRam = usoRam.split( )
			usoRam[1] = int(usoRam[1]) - int(usoRam[0])
			usoRam[0] = int(usoRam[0])/1024
			usoRam[1] = int(usoRam[1])/1024
			hardware = consultaSSH('./consultaHardware.sh')
			hardware = hardware.split('\n')
			return render(request,'index.html',{'usuario': request.user.username,
			'discoUsado': usoDisco[0],'discoLibre': usoDisco[1] ,
			'ramLibre': usoRam[0],'ramUsada': usoRam[1],
			'modelName': hardware[0],'MHz': hardware[1],'cache': hardware[2]})

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
						usoDisco = consultaSSH('./usoDiscoHosts.sh')
						usoDisco = usoDisco.split( )
						usoDisco[1] = int(usoDisco[1]) - int(usoDisco[0])
						usoDisco[0] = int(usoDisco[0])/1024
						usoDisco[1] = int(usoDisco[1])/1024
						usoRam = consultaSSH('./usoRamHosts.sh')
						usoRam = usoRam.split( )
						usoRam[1] = int(usoRam[1]) - int(usoRam[0])
						usoRam[0] = int(usoRam[0])/1024
						usoRam[1] = int(usoRam[1])/1024
						hardware = consultaSSH('./consultaHardware.sh')
						hardware = hardware.split('\n')
						return render(request,'index.html',{'usuario': request.user.username,
						'discoUsado': usoDisco[0],'discoLibre': usoDisco[1] ,
						'ramLibre': usoRam[0],'ramUsada': usoRam[1],
						'modelName': hardware[0],'MHz': hardware[1],'cache': hardware[2]})

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
