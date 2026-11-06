# Arquitetura e integração

`Kommo API → backend (secret) → snapshot → aplicação HTTPS → iframe nos Insights`

O navegador consulta a API do próprio BI. A API do BI consulta a Kommo com credencial protegida. O iframe não é a integração de dados: ele apenas apresenta a aplicação.

## Fontes consultadas em 06/11/2026

- https://support.kommo.com/docs/manage-your-dashboard
- https://developers.kommo.com/reference/add-pipelines
- https://developers.kommo.com/reference/add-stages
- https://developers.kommo.com/reference/add-custom-fields
- https://developers.kommo.com/reference/loss-reasons
- https://developers.kommo.com/docs/webhooks-general
- https://developers.cloudflare.com/workers/static-assets/
- https://developers.cloudflare.com/workers/configuration/secrets/
- https://developers.facebook.com/docs/marketing-api/conversions-api/parameters

O exemplo oficial de widget é um HTML, disponível pelo link de download na página de suporte. O exemplo menciona `kommo_period`; na UI inspecionada, o iframe recebeu `period`, `date_from`, `date_to`, `lang`, `currency`, `t`. Não dependa de um nome sem verificar a conta. `date_from=false` não é data válida.

## Contrato de dados recomendado

Lead: id, pipeline_id, status_id, responsible_user_id, price, created_at, closed_at, custom_fields_values e tags. Dimensões: origem, UTMs, empreendimento, construtora, região. Marcos: qualificação, agendamento, proposta e fechamento. Guarde horários Unix no backend e renderize no fuso do negócio.

Leia todas as páginas (`_links.next`) com limite explícito. A API pode devolver um JSON serializado como string em alguns conectores; faça parse somente quando necessário. Não assuma que `request_id` é uma chave de idempotência persistida: é correlação de resposta.

Nunca monte um proxy público arbitrário para `path`, URL ou métodos fornecidos pelo cliente. Mantenha uma API pequena que só devolve dados autorizados. Registre erros sem headers de autorização.

## Particularidades verificadas

- IDs de ganho/perda: 142 e 143; pertencem a cada pipeline. Filtre também `pipeline_id` para não contar ganho de prospecção como venda.
- Etapa de entrada não classificada não recebe leads pelo mesmo POST de uma etapa comercial. Escolha uma etapa normal editável.
- A API desta demo rejeitou renomear 142/143 por PATCH de status; mantenha nomes nativos ou verifique as opções ao criar o funil.
- Ao renomear etapas por PATCH individual, informe `sort` explicitamente. Nesta conta, omitir `sort` reordenou as colunas. O PATCH na coleção de statuses retornou 405. Releia e valide a ordem após alterações.
- Cores de status são enumerações aceitas pela API. Não presuma qualquer HEX válido; omita a cor se não precisar customizar.
- Deletar lead não foi assumido como rollback. Faça carga identificável, com plano e reconciliação; não repita POST após resultado incerto sem consultar o CRM.
- Um snapshot KV pode ter defasagem entre regiões. Mostre o timestamp; não prometa atualização imediata.

## Implantação

Use configuração específica da nova aplicação, sem alterar sites existentes. Exemplo de comandos (adaptar ao ambiente): `npm install`, `npx wrangler dev`, `npx wrangler secret put KOMMO_TOKEN`, `npx wrangler deploy`. Se OAuth localhost expirar, `wrangler login --device` pode resolver em versões que suportem esse fluxo. Não instale/atualize outras skills por efeito colateral.

No painel, a largura/altura são unidades de grade, não pixels. Nesta conta, o limite validado foi 6×6. Após um valor inválido, o formulário mantém a classe de erro até o campo receber foco; reabra a janela ou refaça o foco antes de salvar. Verifique a grade atual antes de dimensionar. Preserve outros widgets; não remova relatórios sem autorização.
