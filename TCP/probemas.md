Descrição da Captura do Wireshark

Durante os testes com o Wireshark, foi possível observar claramente o funcionamento do protocolo TCP em ação.

Dentre os principais eventos observados estão:

Three-Way Handshake (3-Way Handshake): Foi identificado o processo de estabelecimento da conexão TCP com os pacotes SYN, SYN-ACK e ACK, caracterizando o "aperto de mãos" inicial entre cliente e servidor.

Encerramento da conexão: Foi identificado o pacote com flag FIN, ACK, que indica o encerramento correto de uma das conexões TCP.

Esses eventos comprovam que o servidor está utilizando TCP corretamente e que as conexões são de fato iniciadas e encerradas de maneira controlada.

Problemas Identificados no Código Original

Durante a execução e testes do servidor de chat, foram observados os seguintes problemas:

Problemas com reconexões: Após a desconexão de um cliente, reconectar no mesmo terminal fazia com que mensagens deixassem de aparecer corretamente para outros clientes.

Mensagens de introdução ausentes: Em algumas reconexões, o cliente não recebia mais as mensagens iniciais, como seu nome de usuário ou comandos disponíveis.

Threads não encerrando corretamente: Parecia que as threads associadas a clientes desconectados continuavam vivas ou causavam comportamento inesperado.

Soluções Implementadas

Tratamento aprimorado de desconexão: Foram adicionados trechos de código para lidar melhor com ConnectionResetError e remoção de clientes da lista compartilhada.

Lock para acesso a lista de clientes: Uso de threading.Lock para evitar condições de corrida na lista de clientes.

Mensagens de entrada padronizadas: Reestruturação da função de boas-vindas para garantir que toda nova conexão receba as instruções iniciais.

Apesar disso, persistiram problemas de comunicação entre clientes após uma desconexão e reconexão, o que pode estar relacionado à forma como as threads e sockets são manipulados.

Resultados dos Testes de Resiliência

Teste 1: Conexão recusada
SUCESSO: Conexão recusada detectada corretamente

Teste 2: Desconexão súbita
Conectado ao servidor
SUCESSO: Socket fechado abruptamente

Teste 3: Dados malformados
Conectado ao servidor
Timeout na resposta (pode ser esperado)
SUCESSO: Teste de dados malformados concluído

Reflexão sobre as Limitações e Melhorias Futuras

A atividade expôs as limitações de um servidor de chat simples com múltiplas conexões concorrentes. Apesar do funcionamento básico, a reconexão de clientes causou problemas de sincronização e perda de mensagens. A ausência de um mecanismo robusto de gerenciamento de sessões (por exemplo, identificadores de cliente persistentes, timeout de inatividade e validação de estado) compromete a resiliência da aplicação.

Para melhorar, seria necessário:

Encerrar corretamente as threads dos clientes desconectados

Garantir a consistência da lista de clientes conectados

Utilizar select, selectors, ou bibliotecas como asyncio para controle eficiente de múltiplas conexões

Implementar logs de depuração mais robustos

A experiência mostrou que programar com sockets é desafiador, especialmente sem apoio docente adequado, mas ainda assim permitiu entender na prática aspectos críticos de aplicações em rede.

