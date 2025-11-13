# Script para configurar Git no projeto
$ErrorActionPreference = "Stop"

# Definir encoding UTF-8
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8

# Caminho do projeto
$projectPath = "C:\Users\italo.lucena\OneDrive\1. IE Consultoria\9. IBMEC\Turma - Inovação_IA_DS_BD_Negócios - Nov25_Live_6x\Cursor_PreAgentAI_RAG_Atividade"

# Verificar se o diretório existe
if (-not (Test-Path $projectPath)) {
    Write-Host "Diretório não encontrado: $projectPath"
    exit 1
}

# Navegar para o diretório do projeto
Set-Location -LiteralPath $projectPath

# Inicializar repositório Git (se não existir)
if (-not (Test-Path ".git")) {
    git init
}

# Adicionar remote
git remote remove origin 2>$null
git remote add origin git@github.com:InStudium/PreAgentAI_RAG.git

# Adicionar todos os arquivos
git add .

# Fazer commit
git commit -m "Initial commit: PreAgentAI RAG project"

# Fazer push
git push -u origin master

Write-Host "Projeto commitado e enviado para o GitHub com sucesso!"

