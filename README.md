# issues dataset generator

A finalidade desse repositório é armazenar os scripts que serão usados para gerar os datasets que iremos usar no nosso trabalho.

Esse dataset será criado com base nas issues de bug dos seguintes softwares open-source:
- [Angular](https://github.com/angular/angular)
- [Angular.js](https://github.com/angular/angular.js)
- [ASP.NET Core](https://github.com/dotnet/aspnetcore)
- [Spring](https://github.com/spring-projects/spring-framework)

## Requisitos para rodar o script
- [Instalar Python](https://www.python.org/downloads/)
- [Instalar PyGithub](https://pygithub.readthedocs.io/en/latest/introduction.html)
- [Instalar reliability](https://reliability.readthedocs.io/en/latest/)
- [Instalar matplotlib](https://matplotlib.org/3.3.2/users/installing.html)
- [Gere seu Personal Access Token](https://github.com/settings/tokens)

## Como rodar localmente

- Certifique-se possuir uma verção >= 3.8 do ptyhon

```bash
# Crie uma virtual env
virtualenv -p python3.8 env

# Entre na venv
source env/bin/activate

# Instale as dependências
pip install -r requirements.txt

# Crie um token no github. Não é necessário nenhuma autorização
# https://github.com/settings/tokens

Pesquise por um repositório https://github.com/explore, e copie a url do repositório.
Por exemplo: https://github.com/awesomeWM/awesome

Entenda as regras de identificação de bugs desse repositório.
Para o caso do exemplo, as issues de bug recebem a tag `bug`

Modifique o script de geração.
Exemplo de modificação:
```

```python
elif(SOFTWARE=='ANGULARJS'):
    filters_rules = {
        'labels': {
            'must_have': ['type: bug'],

            'blocklist_labels': [
                'resolution: invalid',
                "resolution: can't reproduce",
                'resolution: duplicate',
                'Known Issue'
            ]
        }
    }

    r = Repository('angular/angular.js', filters_rules)
```

```bash
# Rode o script
python local-script-app.py
```

## Referencias bibliograficas importantes

- Open source software reliability model: an empirical approach [[Original]](https://www.ics.uci.edu/~wscacchi/Papers/WOSSE-2005/ZhouDavis.pdf) [[Tradução]](https://durvalcarvalho.github.io/testesSoftware/#/artigos/open-source-software-reliability-model-an-empirical-approach)

- An empirical analysis of open source software defects data through software reliability growth models [[Original]](https://booksc.xyz/book/31986905/aec648) [[Tradução]](https://durvalcarvalho.github.io/testesSoftware/#/artigos/an-empirical-analysis-of-open-source-software-defects-data-through-software-reliability-growth-models)

- A Comparative Analysis of Software Reliability Growth Models using Defects Data of Closed and Open Source Software [[Original]](https://booksc.xyz/book/21572363/897a7b) [[Tradução]](https://durvalcarvalho.github.io/testesSoftware/#/artigos/a-comparative-analysis-of-software-reliability-growth-models-using-defects-data-of-closed-and-open-source-software)
