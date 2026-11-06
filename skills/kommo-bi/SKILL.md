---
name: kommo-bi
description: Diagnosticar o negócio e construir um BI personalizado dentro dos Insights da Kommo. Usar para dashboards comerciais, indicadores, origem e UTMs, desempenho de IA, funis conectados e demos. Inclui entrevista de descoberta, definição das métricas, aplicação local e integração HTTPS; não é widget de cartão ou app de Marketplace.
---

# BI dentro dos Insights da Kommo

Construa uma aplicação web que lê a API da Kommo no servidor e aparece no painel por iframe. O usuário pode pedir somente uma revisão local, uma demo ou uma implementação de produção; preserve esse escopo.

## Começar pelo negócio

Antes de desenhar um BI novo, conduza a descoberta de [references/briefing.md](references/briefing.md). Aproveite as respostas já presentes na conversa e nos arquivos; pergunte somente o que falta. Em uma correção pontual, preserve o briefing existente em vez de reabrir toda a entrevista.

Faça perguntas em rodadas curtas, normalmente até três por vez. Comece pelo negócio, pelas decisões que o painel precisa apoiar e pelo contexto de uso (demo ou operação real). Aguarde as respostas necessárias antes de fixar fórmulas ou arquitetura. Continue inspeções e preparações independentes enquanto isso. Não despeje o questionário inteiro nem imponha escolhas que o usuário já fez.

Identifique a conta autorizada e a forma segura de acesso. Peça o subdomínio e oriente a configuração da credencial em secret/env local; não solicite token em repositório, print ou código frontend. Quando houver acesso autorizado, descubra pela API os funis, etapas, campos, tags, motivos de perda e usuários, em vez de pedir que o usuário transcreva tudo. Inspeção não autoriza criar dados ou alterar funis. Reaproveite cadastros existentes.

Produza um briefing curto, com objetivo, público, decisões, indicadores prioritários, filtros, escopo de dados, metas, frequência e acesso. Para cada indicador, defina fórmula, população, data usada, unidade monetária, fonte e limitações. Use [references/briefing.md](references/briefing.md) como modelo. Resolva ambiguidades materiais com o usuário; não transforme preferências opcionais em bloqueios ou peça uma aprovação extra se o pedido já autoriza a execução.

Não reutilize conta, IDs, tokens ou campos de outra instalação. Esta skill não inclui credenciais, não exige nenhum MCP específico nem depende de outra skill instalada. Consulte a documentação oficial atual das APIs e da hospedagem ao implementar; exemplos das referências precisam ser adaptados à conta.

## Traduzir o diagnóstico em um painel

Leia [references/metrics.md](references/metrics.md) antes de calcular indicadores e [references/architecture.md](references/architecture.md) antes de integrar. Para aulas e contas de teste autorizadas, use [references/demo.md](references/demo.md).

Selecione os indicadores que respondem às decisões declaradas. Uma visão executiva pode mostrar resultados e metas; aquisição compara origens e campanhas; operação evidencia gargalos e próximos passos. Adapte as dimensões ao setor: empreendimento/construtora/região são úteis para imóveis, mas não são obrigatórios em outros negócios.

Exiba o significado de cada número e permita conferir os registros que o compõem. Separe estoque atual, resultado do período e coorte de entrada. Rotule ausência de informação como indisponível ou sem preenchimento; não invente histórico, investimento em anúncios, receita recorrente ou atribuição. Mostre cobertura de preenchimento quando ela afeta a comparação.

A função **Insights → Painel → Configurações → + → Adicionar novo widget** aceita uma página hospedada em HTTPS. Esse widget não exige `manifest.json`, ZIP de integração ou publicação no Marketplace. Consulte a [documentação oficial do painel](https://support.kommo.com/docs/manage-your-dashboard) antes de configurar a interface.

## Construir

- Backend: token em secret/env protegido; domínio fixo ou validado; API paginada; limites de requisição; erros explícitos; snapshot com timestamp. Não coloque o token em HTML, JavaScript, URL do iframe, bundle ou ZIP distribuído.
- Frontend: filtro por período e dimensões relevantes, indicadores com denominadores explícitos, data da última atualização, estado vazio e erro. Vincule os registros ao CRM para permitir auditoria.
- Produção: autenticação e autorização por conta/usuário. `frame-ancestors`, CORS, URL difícil de adivinhar ou `Origin` não substituem controle de acesso. Um token de administrador no backend não autoriza expor todos os dados para todos os usuários.
- Demo pública: limitar a uma conta de teste e a registros sintéticos identificados; excluir contatos reais, tokens e outros dados pessoais. Identificar claramente a simulação.
- Cloudflare: Worker com assets pode servir página e API; Pages precisa de backend para segredos. Use KV para cache de snapshots, não como banco transacional de deduplicação. D1/DO/filas são opções quando há eventos duráveis ou concorrência.
- Permita enquadramento por `Content-Security-Policy: frame-ancestors 'self' https://SUBDOMINIO.kommo.com`. Não use `X-Frame-Options: DENY` ou `SAMEORIGIN` nesse documento.
- Mantenha os filtros do BI independentes ou implemente explicitamente a integração com os parâmetros do painel. Não afirme que o filtro nativo controla o iframe sem testar.

## Conectar funis

Antes de escolher entre mover ou criar outro negócio, considere a unidade de análise. Mover o mesmo lead da prospecção para o comercial preserva o contato e evita duplicar vendas. Registre a origem e a data da conversão. Se criar outra oportunidade for necessário, persista o vínculo e uma chave idempotente.

Valide conta, funil, etapa e marca de escopo antes de escrever. Reconsulte o estado atual antes da transição. Gatilhos repetidos não podem criar cópias ou apagar dados. Uma demo pode usar cron; identifique a latência. Para operação real, prefira webhook com processamento confiável e reconciliação periódica conforme a necessidade.

## Meta e rastreamento

Quando o pedido for simulação, gere prévias locais e nunca chame a Graph API. Distinga “evento modelado”, “tentativa de envio”, “aceito pela API” e “conversão atribuída”. Campos ou tags não provam que um evento foi recebido pela Meta.

Antes de um envio real, valide a documentação atual da CAPI: `event_name`, `event_time`, `event_id`, `action_source`, dados do usuário e regras de deduplicação Pixel+CAPI. Não confunda dados enviados com receita atribuída. Teste somente quando houver autorização e credenciais para esse escopo.

## Entregar e verificar

Abra a versão localhost para revisão quando solicitada. Teste as fórmulas com conjuntos pequenos, sem resultados e com filtros combinados. Compare os totais com a API. Confira carregamento no iframe, ausência de token no frontend, responsividade e links dos registros.

Se a implantação estiver autorizada, publique em HTTPS, configure o widget e recarregue o painel para verificar persistência. Não declare “instalado” se apenas gerou a URL ou preparou instruções.

Entregue os links localhost/produção/CRM e o que foi efetivamente validado. Registre limitações concretas: expiração do token, atualidade do snapshot, histórico sintético ou automação ainda não testada. Distribua somente os arquivos necessários, sem `.env`, `.dev.vars`, credenciais, estado do navegador, logs ou dados de clientes.
