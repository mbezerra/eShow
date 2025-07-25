#!/usr/bin/env python3
"""
Script para gerenciar versionamento automático do projeto eShow
Uso:
    python version.py patch    # Incrementa versão patch (0.1.0 -> 0.1.1)
    python version.py minor    # Incrementa versão minor (0.1.0 -> 0.2.0)
    python version.py major    # Incrementa versão major (0.1.0 -> 1.0.0)
    python version.py show     # Mostra versão atual
"""

import subprocess
import sys
import re
from typing import Tuple

# Versão atual do projeto
VERSION = "0.22.0"

def get_current_version() -> str:
    """Obtém a versão atual baseada na tag mais recente"""
    try:
        result = subprocess.run(
            ["git", "describe", "--tags", "--abbrev=0"],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            version = result.stdout.strip()
            if version.startswith('v'):
                version = version[1:]
            return version
    except (subprocess.SubprocessError, FileNotFoundError):
        pass
    return "0.1.0"

def parse_version(version: str) -> Tuple[int, int, int]:
    """Converte string de versão em tupla (major, minor, patch)"""
    parts = version.split('.')
    major = int(parts[0]) if len(parts) > 0 else 0
    minor = int(parts[1]) if len(parts) > 1 else 0
    patch = int(parts[2]) if len(parts) > 2 else 0
    return major, minor, patch

def format_version(major: int, minor: int, patch: int) -> str:
    """Converte tupla de versão em string"""
    return f"{major}.{minor}.{patch}"

def increment_version(version: str, increment_type: str) -> str:
    """Incrementa a versão baseada no tipo especificado"""
    major, minor, patch = parse_version(version)
    
    if increment_type == "major":
        major += 1
        minor = 0
        patch = 0
    elif increment_type == "minor":
        minor += 1
        patch = 0
    elif increment_type == "patch":
        patch += 1
    else:
        raise ValueError(f"Tipo de incremento inválido: {increment_type}")
    
    return format_version(major, minor, patch)

def create_git_tag(version: str, message: str = None):
    """Cria uma tag Git com a versão especificada"""
    tag_name = f"v{version}"
    tag_message = message or f"Release version {version}"
    
    # Cria a tag
    subprocess.run(["git", "tag", "-a", tag_name, "-m", tag_message], check=True)
    print(f"Tag criada: {tag_name}")
    
    # Push da tag para o repositório remoto
    try:
        subprocess.run(["git", "push", "origin", tag_name], check=True)
        print(f"Tag enviada para o repositório remoto: {tag_name}")
    except subprocess.CalledProcessError:
        print("Aviso: Não foi possível enviar a tag para o repositório remoto")

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    
    command = sys.argv[1].lower()
    
    if command == "show":
        current_version = get_current_version()
        print(f"Versão atual: {current_version}")
        return
    
    if command not in ["major", "minor", "patch"]:
        print("Comando inválido. Use: major, minor, patch ou show")
        sys.exit(1)
    
    # Verifica se há mudanças não commitadas
    try:
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            capture_output=True,
            text=True
        )
        if result.stdout.strip():
            print("Erro: Há mudanças não commitadas. Faça commit antes de criar uma nova versão.")
            sys.exit(1)
    except subprocess.CalledProcessError:
        print("Erro: Não foi possível verificar o status do Git")
        sys.exit(1)
    
    # Obtém versão atual e calcula nova versão
    current_version = get_current_version()
    new_version = increment_version(current_version, command)
    
    print(f"Versão atual: {current_version}")
    print(f"Nova versão: {new_version}")
    
    # Confirma com o usuário
    response = input("Deseja criar a tag e fazer push? (y/N): ")
    if response.lower() not in ['y', 'yes', 's', 'sim']:
        print("Operação cancelada.")
        return
    
    try:
        create_git_tag(new_version)
        print(f"✅ Versão {new_version} criada com sucesso!")
        print(f"📦 A API agora usará automaticamente a versão {new_version}")
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao criar tag: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 