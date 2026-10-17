# Malandro local

Uma cópia local do cliente público de https://malandro.app para jogar sozinho, obtida em 17/10/2026. Esta versão usa o pacote de produção com modificações, e não o projeto com o código-fonte original.

## Como executar

```sh
python3 server.py
```

Abra http://127.0.0.1:8080. É necessário ter Python 3 e curl instalados. Para usar outra porta: `python3 server.py --port 8081`.

A exigência de login foi substituída pelo modo local já integrado ao cliente. O nome padrão do jogador local é `igor3k`. O progresso fica no localStorage deste navegador; use o mesmo endereço e a mesma porta para mantê-lo. Nenhuma conta é criada ou acessada no servidor.

Requisições relacionadas a contas, telemetria, recursos sociais, rankings e serviços multijogador são bloqueadas. O modo individual é mantido. Recursos que dependem do servidor de produção ficam indisponíveis.

Imagens, fontes e áudios são baixados do site público conforme necessário pelo servidor local e salvos em `.asset-cache/`. É necessário acesso à internet para baixar arquivos que ainda não estejam no cache. Esta cópia não inclui todos os arquivos necessários para jogar sem internet; mantenha o servidor em execução enquanto joga. O pacote JavaScript do cliente e o CSS ficam armazenados localmente.

O servidor escuta em 127.0.0.1 e disponibiliza os arquivos do jogo e os arquivos estáticos públicos. Chamadas à API de contas nunca são encaminhadas. O pacote permanece na versão obtida nessa data; futuras atualizações do site original não são aplicadas automaticamente.
