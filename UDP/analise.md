Introdução


A atividade teve como foco trabalhar com o protocolo UDP, explorando suas limitações e formas de contornar os problemas que ele apresenta, como perda de pacotes e falta de confiabilidade. Durante a aula, foi possível aplicar esses conceitos de forma prática com base em três propostas diferentes.




ATV1: Chat UDP Simples


Essa parte foi voltada para montar um chat básico, onde várias pessoas pudessem se comunicar usando UDP.
Foi possível analisar através do Wireshark os momentos quando o protocolo UDP era utilizado quando alguém entrava na conversa, enviava algo e saia dela.


ATV2: Sistema de Transferência de Arquivos


O foco aqui foi o envio de arquivos por UDP, que por padrão não garante que tudo vai chegar. Para isso, foi trabalhado um sistema que separa o arquivo em pedaços, envia um por vez e espera uma confirmação.
Foi possível analisar através do Wireshark a diferença da quantidade de pacotes enviados em função do tamanho do arquivo, também a diferença de tempo para realizar  o processo.


ATV3: Análise Comparativa UDP vs TCP


Depois de montar tudo com UDP, foi feita uma comparação com o protocolo TCP. Como o TCP já possui mecanismos prontos para controle de erro e confirmação, o trabalho que antes era feito manualmente no UDP se torna automático.




CENÁRIOS


Os testes foram feitos localmente, simulando trocas de mensagens e arquivos entre clientes. Também foram testadas situações com perda de pacotes para verificar como o sistema reagia. Foi feita a comparação com o TCP para entender as vantagens e desvantagens de cada protocolo em cada caso.
Não consegui concluir algo pelos cenários, como realizei somente com um PC, mesmo buscando outros métodos e aumentando o nível de perda e de latência, não foi notado uma discrepância entre os resultados.

