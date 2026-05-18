#ex1
"""A Análise de Componentes Principais (PCA) é uma técnica de redução de dimensionalidade que transforma os dados em novos eixos, chamados componentes principais, que concentram a maior parte da variância. Os eixos originais nem sempre são os mais informativos porque a maior variação dos dados pode ocorrer em outras direções, como em uma diagonal."""

#ex2
"""Dados distribuídos em diagonal são ideais para PCA porque a maior parte da variância está concentrada em uma única direção. Assim, o primeiro componente principal captura quase toda a informação. Se os dados já estivessem alinhados com os eixos x e y, o PCA encontraria componentes semelhantes aos eixos originais."""

#ex3
"""Variância direcional mede o espalhamento dos dados em uma direção específica. Ela é calculada projetando os pontos sobre um vetor w e medindo a variância dessas projeções. O vetor w deve ter magnitude 1 para que apenas a direção influencie o resultado, e não o tamanho do vetor."""

#ex4
"""
A:
A maior variância ocorre na direção diagonal crescente, da esquerda inferior para a direita superior, que corresponde ao eixo maior da elipse.

B:
O outlier está aproximadamente em (-11, -27). Ele pode alterar a direção do primeiro componente principal, puxando-o em sua direção.

C:
O padrão diagonal indica forte correlação entre x e y. O PCA encontra essa direção e permite representar os dados com menos dimensões e pouca perda de informação.
"""

#ex5
"""A função de_mean_matrix(A) centraliza os dados.

Na linha nr, nc = shape(A), obtém-se o número de linhas e colunas da matriz.

Na linha column_means, _ = scale(A), calcula-se a média de cada coluna.

Na linha return make_matrix(...), cria-se uma nova matriz em que cada valor é substituído por valor original menos a média da coluna.

Após a centralização, os dados mantêm o mesmo formato, mas passam a ter média zero em cada coluna e ficam centrados na origem.

Na Figura 10-6, a nuvem de pontos tem a mesma forma da Figura 10-5, mas está deslocada para o centro do plano.
"""

#ex6
"""Ao subtrair a média de cada coluna, a média de cada variável passa a ser zero, fazendo com que os dados fiquem centrados na origem.

A centralização não altera a correlação porque apenas desloca os pontos, sem mudar suas posições relativas.

Após centralizar, o PCA busca a direção em que os dados apresentam a maior variância, ou seja, o primeiro componente principal."""

#ex7
"""a) O vetor [0.924, 0.383] representa a direção do primeiro componente principal, alinhada com o alongamento do conjunto de dados.

b) Usa-se descida de gradiente para encontrar o vetor que maximiza a variância dos dados projetados.

c) A função direction() normaliza o vetor para que ele tenha magnitude 1 e represente apenas uma direção."""

#ex8
"""A direção para o quadrante superior direito é consistente com a correlação positiva, pois x e y aumentam juntos.

Se o vetor fosse [0.383, 0.924], a componente y teria maior peso.

Como o primeiro componente captura a maior parte da variância, a projeção nessa direção perde pouca informação."""

#ex9
"""A função remove_projection(X, w) remove de cada ponto a parte que está na direção do componente principal w.

Isso permite que o próximo componente capture apenas a variância restante.

Se essa remoção não fosse feita, o algoritmo encontraria novamente o mesmo componente."""

#ex10
"""Após remover o primeiro componente, resta apenas a variância residual, fazendo os pontos se alinharem em uma única linha.

A inclinação negativa indica a direção do segundo componente principal.

O primeiro e o segundo componentes são ortogonais, formando um ângulo de 90 graus."""

#ex11
"""Os componentes principais são ortogonais porque cada novo componente é calculado após remover a variância explicada pelos anteriores.

O segundo componente captura a variância residual.

Em 10 dimensões, podem existir até 10 componentes principais, mas geralmente apenas os primeiros são relevantes."""

#ex12
"""A função transform_vector projeta um vetor nos componentes principais. A função transform aplica isso a todo o conjunto de dados.

Transformar os dados significa representá-los pelos componentes principais, em vez das variáveis originais.

O custo de interpretabilidade supera os benefícios quando é essencial entender o significado de cada variável, como em medicina e finanças."""

#ex13
"""Na detecção de spam, usa-se um classificador supervisionado. As features podem ser palavras, links e anexos. O rótulo é spam ou não spam.

A detecção de fraude é supervisionada porque utiliza transações históricas rotuladas como fraude ou legítima.

Sistemas de recomendação podem ser supervisionados quando utilizam avaliações dos usuários como rótulos."""

#ex14
"""No aprendizado supervisionado, um exemplo é prever o preço de imóveis com base em suas características.

No semissupervisionado, pode-se classificar espécies de plantas usando poucas imagens rotuladas e muitas não rotuladas.

No não supervisionado, pode-se agrupar músicas por características semelhantes.

No aprendizado online, um sistema de previsão de demanda é atualizado continuamente com novas vendas."""

#ex15
"""No underfitting, o modelo grau 0 captura apenas a média dos dados.

O modelo grau 1 representa bem a tendência geral e generaliza melhor.

No overfitting, o modelo grau 9 aprende o ruído do treino e tende a errar em novos dados."""

#ex16
"""a) Usar o conjunto de teste para escolher modelos faz com que ele deixe de ser independente.

b) O treino ajusta o modelo, a validação escolhe o melhor modelo e o teste mede o desempenho final.

c) Padrões não generalizáveis são relações casuais do treino, como associar IDs pares a compras."""
 
#ex17
"""Questão A

A acurácia é (TP + TN) / Total = (70 + 981070) / 1000000 = 98,1%.

A precisão é TP / (TP + FP) = 70 / 5000 = 1,4%.

O recall é TP / (TP + FN) = 70 / 14000 = 0,5%.

A acurácia é enganosa porque o modelo quase não identifica os casos positivos.

Questão B

	Predito Positivo	Predito Negativo
Real Positivo	TP = 70	FN = 13.930
Real Negativo	FP = 4.930	TN = 981.070

Questão C

A acurácia é enganosa em problemas com classes desbalanceadas, como detecção de fraude e identificação de falhas industriais."""

#ex18
"""A precisão é TP / (TP + FP) = 150 / 200 = 75%.

O recall é TP / (TP + FN) = 150 / 180 = 83,3%.

O modelo identifica a maioria dos positivos, mas ainda gera alguns falsos positivos."""

#ex19
"""O F1-Score é 2 * (0,90 * 0,50) / (0,90 + 0,50) = 0,64.

Isso indica alta precisão, mas recall moderado.

mAP50 = 0,92 significa que o modelo detecta plantas com excelente desempenho considerando IoU ≥ 0,50.

AP mede o desempenho de uma classe. mAP é a média do AP de todas as classes."""

#ex20
"""Alto recall e baixa precisão são aceitáveis quando perder positivos é mais grave, como em triagens médicas.

Alta precisão e baixo recall são preferíveis quando falsos positivos têm alto custo, como em filtros de spam.

Reduzir o threshold aumenta recall e diminui precisão.

A curva Precision-Recall ajuda a escolher o melhor equilíbrio entre as duas métricas."""

#ex21
"""Baixa variância não basta se o viés for alto, pois o modelo pode errar de forma consistente.

Alta variância é problemática porque o modelo muda muito com pequenas alterações nos dados e generaliza mal.

Ao treinar em diferentes amostras, modelos com alto viés produzem resultados semelhantes e ruins, enquanto modelos com alta variância produzem resultados instáveis."""

#ex22
"""Mais dados não resolvem alta variância quando os dados têm baixa qualidade, quando o modelo é complexo demais, quando as features não são relevantes ou quando os novos dados são pouco diversos."""

#ex23
"""Escolher uma família de modelos é definir a estrutura do modelo. Aprender os parâmetros é ajustar seus valores com os dados.

Na regressão linear, os parâmetros são os coeficientes da reta.

Em árvores de decisão, os parâmetros incluem os atributos escolhidos, os pontos de corte e a estrutura da árvore."""

#ex24
"""Um exemplo de aprendizado supervisionado é prever cancelamento de clientes com base em uso, valor pago e histórico de suporte.

No PCA, não há rótulos. Ele encontra as direções de maior variância e correlação entre as variáveis."""

#ex25
"""O PCA reduz overfitting ao remover variáveis redundantes e ruidosas. O benefício é melhor generalização; o custo é menor interpretabilidade.

Com precisão = 0,90 e recall = 0,50, o modelo de fraude deixa passar muitos casos. Eu reduziria o threshold para aumentar o recall.

Acurácia de 95% no treino e 60% no teste indica overfitting. Para corrigir: reduzir a complexidade do modelo, aplicar PCA e usar mais dados.

Pandas facilita o tratamento dos dados, e o scikit-learn oferece implementações otimizadas de PCA, padronização, validação e integração com outros modelos."""