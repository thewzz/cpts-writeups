# CPTS Writeups

Writeups e anotações do curso preparatório **CPTS** (Certified Penetration Testing Specialist), documentando a resolução de máquinas e os estudos de enumeração/exploração.

🔗 **Site:** https://thewzz.github.io/cpts-writeups

## Sobre

Este repositório reúne meus writeups de máquinas (HTB / laboratórios) e anotações de estudo, publicados como um site estático com [MkDocs](https://www.mkdocs.org/) e o tema [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/).

## Conteúdo

### Máquinas

**Concluídos**

- **Easy:** Getting Started, Robot, CAP, Dancing, Redeemer, Footprinting Tests - Easy
- **Medium:** Footprinting Tests - Medium
- **Hard:** Footprinting Tests - Hard

**Em andamento**

- **Easy:** Silentium, Facts

### Anotações

- **Estudos de Footprinting:** DNS, SMB Client, SMTP, Oracle TNS, IPMI

## Estrutura do projeto

```
cpts-writeups/
├── docs/
│   ├── index.md              # Página inicial (Home)
│   ├── machines/             # Writeups das máquinas + imagens
│   ├── notes/                # Anotações de estudo
│   ├── overrides/            # Customizações do tema
│   ├── stylesheets/          # CSS extra (extra.css, home.css)
│   └── img/                  # Imagens compartilhadas
├── .github/workflows/
│   └── deploy.yml            # Deploy automático no GitHub Pages
└── mkdocs.yml                # Configuração do MkDocs
```

## Rodando localmente

Requer Python 3.12+.

```bash
# Instalar dependências
pip install mkdocs-material

# Servir localmente (http://127.0.0.1:8000)
mkdocs serve

# Gerar o site estático
mkdocs build
```

## Deploy

O deploy é automático: cada `push` na branch `main` dispara o workflow do GitHub Actions
([`deploy.yml`](.github/workflows/deploy.yml)), que executa `mkdocs gh-deploy --force --strict`
e publica o site no GitHub Pages.

## Autor

**Matheus Navarro de França**

---

> ⚠️ Conteúdo com fins educacionais. Os writeups documentam técnicas de teste de intrusão
> em ambientes autorizados de laboratório.
