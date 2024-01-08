# VazanDigital

## Descrição
VazanDigital é um script projetado para auxiliar no curso da plataforma Vazan Conteúdo Digital.

## Pré-requisitos

Antes de instalar o VazanDigital, você precisa instalar o Python 3.10.6 e o aria2c. Aqui estão as instruções para diferentes sistemas operacionais:

### Para usuários do Windows:

1. Instale o Chocolatey, um gerenciador de pacotes para Windows. Abra o PowerShell como administrador e execute:
   ```bash
   Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))
   ```
   Instale o Python 3.10.6 e o aria2c usando o Chocolatey:
   ```bash
   choco install python --version=3.10.6
   choco install aria2
   ```

### Para usuários do Ubuntu 22.04:

1. Abra o terminal e atualize a lista de pacotes:
   ```bash
   sudo apt update
   ```
   Instale o Python 3.10.6 e o aria2c:
   ```bash
   sudo apt install python3.10
   sudo apt install aria2
   ```

## Instalação

Para instalar o VazanDigital, siga os passos abaixo:

```bash
# Clone o repositório
git clone https://github.com/benedictus79/VazanDigital.git

# Navegue até o diretório do script
cd VazanDigital

# Instale os pacotes necessários (se aplicável)
pip install -r requirements.txt
```

## Uso

Para usar o VazanDigital, siga estes passos:

Execute o script

```bash
# Comando básico de uso
python main.py
```
Autentique com seu email e senha e escolha o conteúdo a baixar
