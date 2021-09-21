<h1>P2 Project Refactor</h1>

Esse projeto é uma refatoração do código presente no seguinte link:
https://github.com/zadhart/P2-Project.git

<h3>Code Smells Identificados:</h3>
<li>Long Method no método undo da classe Change;</li>
<li>Código Duplicado na classe Change;</li>
<li>Large Class na classe Change;</li>
<li>Long Method no método Run;</li>

<h3>Padrões aplicados:</h3>
<li>Para o Long Method da classe Change utilizamos o padrão Replace Method with Method Object;</li>
<li>Para o Código Duplicado na classe Change utilizamos o padrão Extract Superclass;</li>
<li>Para a Large Class na classe Change utilizamos o padrão Extract Subclass</li>
<li>Para o Long Method no método Run utilizamos o padrão Extract Method;</li>

<h3>Refatorando:</h3>
<li>Replace Method with Method Object: Transformamos o método em várias classes separadas de modo que as variáveis locais se tornam campos dessa classe.</li>
<li>Extract Superclass: Criamos uma superclasse que possui todos os campos e métodos idênticos.</li>
<li>Extract Subclass: Criamos algumas subclasses para diminuir o código.</li>
<li>Extract Method: Movemos o código para um método novo, e trocamos o código antigo com uma chamada para o novo método.</li>