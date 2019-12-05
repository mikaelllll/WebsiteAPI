<h1>WebsiteAPI</h1> 

Aplicativo para teste da empresa nave.rs

Autor: Mikael Poetsch

Email: mikaelpoe@gmail.com

<h2>Utilização</h2>

Tenha o python 3 e o django instalado 

Abra o prompt de comando

Navegue até a pasta api que possui o arquivo manage.py

execute o comando

```
python manage.py runserver
```
Abra um browser

Vá para o endereço 127.0.0.1:8000 para acessar a homepage da API




<h2> Explicação da API </h2>

A api é uma ferramenta para cadastros de empregos e de aplicação para estas vagas por parte de usuários

Primeiramente para se cadastrar os empregos é preciso ser criado um usuário administrador

Para criar um usuário administrador é preciso estar logado no sistema como um administrador



<h2> Cadastro do administrador </h2>

Para isso, é preciso criar uma conta

Utilizando o prompt de comandos vá até a pasta api que possui o arquivo manage.py e execute o comando

```
python manage.py createsuperuser
```

Quando for solicitado, insira seu nome de usuário (letras minúsculas, sem espaços), e-mail e senha



<h2> Utilização da API por administradores </h2>

Após criar a conta do administrador poderá se logar no site

No canto superior direito da página se encontram os botões para acessar o login e o cadastro de novos usuários da API

Ao clicar no botão **"Log in"** você será redirecionado para uma página para inserir os dados do administrador cadastrado previamente

Após logar no site como administrador irá aparecer uma tabela e um botão

A tabela mostra uma lista de todos os usuários administradores cadastrados no site, o seu email e a última data em que aquela conta logou no sistema

O botão de registrar usuário administrador irá redirecionar para uma página onde é possivel cadastrar contas para os usuários administradores do sistema, basta preencher os campos com dados e clicar em enviar

<h2> Utilização da API por usuários administradores </h2>

Após criar a conta do usuário administrador poderá se logar no site com ela

Após logar no site como usuário administrador irá aparecer uma tabela e um botão

A tabela mostra a lista de todas as vagas de emprego já cadastradas pelo usuário administrador, porém não irá listar vagas de emprego cadastradas por outros usuários administradores

Na tabela consta o nome da empresa, a descrição do emprego e o salário. Um botão logo abaixo da tabela redireciona o usuário administrador à uma tela onde ele pode criar as vagas de emprego

Na tabela à direita também consta um botão de comentário

É possível que o usuário administrador adicione algum comentário à alguma aplicação para vaga de emprego de algum usuário comum. Múltiplos comentários podem ser criados



<h2> Utilização da API por usuários </h2>

Para se registrar como usuário comum basta clicar em cima à direita no botão **"Sign up"** e preencher os dados

Diferente dos outros tipos de usuários, o usuário comum deve preencher o seu nome, telefone, email e cpf

Após logar no site como usuário comum irá aparecer uma tabela

A tabela mostra uma lista de todas as vagas de emprego no site e à direita possui um botão **"Apply for the job"** que ao ser clicado cria a relação de interesse do usuário com a vaga de emprego, permitindo que o usuário administrador que cadastrou a vaga de emprego crie comentários sobre esta aplicação

Ao se candidatar para o emprego, o usuário comum pode clicar em **"Remove Application"** para remover a sua candidatura ao emprego

Em cima à direita existe o botão **"Profile"** que leva qualquer tipo de usuário para uma tela com uma tabela que mostra as informações da conta logada

Para o usuário comum também mostra uma tabela com uma lista de todas as candidaturas às vagas de emprego que ele se cadastrou, inclusive as que foram desistidas por ele 
