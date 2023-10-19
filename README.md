# Jogo Da Memória TCP

Este projeto foi realizado para a cadeira: **_CIC4004A - Programação Concorrente, Paralela e Distribuída_** do cursor de **_[Ciência da Computação, na UCS](https://www.ucs.br/ciencias-da-computacao)_**, semestre 2023/4

## ⚙ Orientação

**Objetivos do Trabalho**

Implementar o jogo da memória, onde os dois usuários se enfrentam utilizando computadores diferentes.
Deve ser desenvolvido de duas maneira, a primeira utilizando sockets TCP e a segunda RPC ou RMI.

**Descrição do Jogo da Memória**

O jogo da memória é um jogo formado por 40 peças (20 pares) que apresentam uma figura em um dos lados. Cada figura se repete em duas peças diferentes. Para começar o jogo, as peças são postas com as figuras voltadas para baixo, para que não possam ser vistas. Cada participante deve, na sua vez, virar duas peças e deixar que todos as vejam. Caso as figuras sejam iguais, o participante deve recolher o par e jogar novamente. Se forem peças diferentes, estas devem ser viradas novamente, e sendo passada a vez ao participante seguinte. Ganha o jogo quem tiver mais pares no final do jogo.

**Descrição da Implementação:**

A implementação deverá empregar o modelo de cliente-servido, sendo formada por 1 servidor e 2

1. _O lado servidor deverá:_

   - Iniciar o jogo e distribuir as peças para os clientes.
   - Controlar as jogadas e a pontuação dos participantes;
   - Receber as peças dos clientes e verificar se as peças são iguais ou não;
   - Enviar para os clientes as atualizações;
   - Ao final do jogo enviar a ambos participantes do jogo a mensagem indicando quem foi o vencedor e quem foi o perdedor da batalha;

2. _O lado cliente deverá:_
   - Receber as peças do servidor;
   - Mostrar a situação do jogo;
   - Enviar a jogada para o servidor;

## 💻 Tecnologias

<p align="left"> 
    <a href="https://www.python.org/" target="_blank" rel="noreferrer"> 
        <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/c/c3/Python-logo-notext.svg/1869px-Python-logo-notext.svg.png" alt="python" width="50" height="50"/> 
    </a>
    <a href="https://api.arcade.academy/en/latest/" target="_blank" rel="noreferrer"> 
        <img src="https://api.arcade.academy/en/2.6.1/_images/arcade-logo.svg" alt="Python Arcade" width="50" height="50"/> 
    </a>
</p>
