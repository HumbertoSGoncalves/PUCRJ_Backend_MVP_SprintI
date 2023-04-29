# MVP Backend - Adega Virtual

Este projeto contempla os requisitos para a entrega do MVP da **Sprint I: Desenvolvimento Full Stack Básico** do curso de Pós Graduação em Engenharia de Software da PUC RIO.

O objetivo é utilizar do conteúdo ensinado durante as aulas para a criação de uma single page application, contando com front e backend. Para que isso fosse possível, foi criada uma Adega virtual, onde os vinhos podem ser adicionados, consultados, ou excluídos.

Mais especificamente, para os códigos aqui encaminhados, será explorado o **backend do MVP**.

---
## Como executar 

- Atualizar todas as libs python listadas conforme o arquivo `requirements.txt`. Ou seja, execute, no ambiente escolhido, a instalação através do comando: 
```
pip install -r requirements.txt;
```
- Para executar a API: 
```
flask run --host 0.0.0.0 --port 5000
```

- Recomendá-se utilizar o comando abaixo, quando em modo de desenvolvimento:
```
flask run --host 0.0.0.0 --port 5000 --reload
```
Desta forma o servidor é reinicia automaticamente após mudanças no código fonte.


Acesse o [http://localhost:5000/#/](http://localhost:5000/#/) no navegador de preferência para verificar a API em execução.

Posteriormente, basta testar quaisquer rotas da API que desejar para gerenciar a sua adega virtual. Cada rota tem sua devida descrição na documentação acessada.
