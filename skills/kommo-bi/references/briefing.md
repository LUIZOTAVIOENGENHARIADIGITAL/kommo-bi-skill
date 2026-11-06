# Diagnóstico para um BI que ajuda a decidir

Use como roteiro adaptável, não como formulário para enviar inteiro. Registre o que já sabe, descubra fatos no CRM e pergunte pelas decisões e regras que só o negócio conhece. Se o usuário não souber, explique opções com exemplos e proponha um padrão explícito.

## Primeira rodada

Exemplo de abertura quando não houver contexto:

1. Qual é seu negócio, o que você vende e qual é seu processo comercial hoje?
2. Quais são as três perguntas que você mais precisa responder com esse painel? Por exemplo: de onde vêm as vendas, onde os leads travam ou quanto a IA contribui para agendamentos.
3. O BI será uma demonstração ou usará dados reais? Quem vai consultar: só você, gestores ou vendedores?

Na sequência, peça o subdomínio da conta e descubra se já existe um projeto ou hospedagem. Configure o acesso por variável local protegida/secret; a pessoa não precisa colar um token na conversa. Não peça senha do usuário quando a API resolve o acesso.

## Rodadas seguintes, conforme as respostas

### Venda, dinheiro e funis

- O que define uma venda ganha: contrato assinado, pagamento, reserva ou outro marco? Há cancelamento ou reabertura?
- O valor do negócio representa venda total, comissão, mensalidade ou receita recebida? Qual moeda e fuso?
- Qual é o ciclo típico? Quais funis entram na análise? Quais são comerciais, prospecção, pós-venda ou suporte?
- Se um prospectado vira comercial, o mesmo negócio muda de funil ou nasce outro? Como preservar vínculo e impedir contagem duplicada?
- Há motivos de perda padronizados? Entradas inválidas e duplicados devem sair de quais indicadores?

Inspecione IDs e etapas pela API. Um status chamado “ganho” em prospecção não prova venda. Se receita mensal e valor total coexistem, mantenha métricas separadas com fonte própria.

### Aquisição e atribuição

- Quais canais geram demanda? Origem é primeira interação, última interação ou preenchimento manual?
- UTMs são capturadas no CRM? Em quais campos? Há campanha, conjunto e anúncio identificáveis?
- O usuário quer comparar quantidade, qualidade, vendas ou retorno financeiro por canal?
- Existe investimento por campanha e período, vindo de qual fonte? Sem investimento confiável, não calcular CPL, CAC ou ROAS. Mesmo com investimento, definir a população e a atribuição de cada cálculo.

Não sobrescreva UTMs originais para completar o relatório. Preserve valores brutos e normalize só na camada de análise. Distinga “sem informação” de tráfego orgânico. A soma dos grupos deve reconciliar com o total filtrado.

### Atendimento, IA e agenda

- Como o CRM identifica atendimento por IA: tag, campo, autor do evento ou integração?
- O que significa agendamento feito pela IA? Há registro de autoria e data? Confirmado, compareceu, cancelou e reagendou são eventos distintos?
- É importante comparar IA e humano em qual resultado e população?
- Quantos agendamentos pode haver por lead? O indicador conta pessoas, leads ou eventos?

Uma tag “IA” prova somente a classificação registrada. Não conclua que a IA agendou ou vendeu sem evidência específica. Comparações descritivas não demonstram que a IA causou a melhora: explicite diferenças de origem, período ou perfil quando relevantes.

### Dimensões do negócio

Escolha somente dimensões que mudem uma decisão. Exemplos:

| Negócio | Dimensões possíveis | Distinções importantes |
|---|---|---|
| Imobiliária | empreendimento, construtora, região, corretor, faixa de preço | VGV, comissão, reserva, visita e contrato |
| Serviços | serviço, equipe, unidade, segmento do cliente | proposta, contrato e recebimento |
| Educação | curso, turma, unidade, consultor | matrícula, pagamento e cancelamento |
| SaaS/recorrência | plano, segmento, canal, executivo | MRR, contrato total, churn e expansão exigem fontes próprias |
| Varejo/B2B | produto, categoria, representante, território | pedido, faturamento e margem não são equivalentes |

### Gestão e experiência

- Quais metas existem, para qual período e por equipe/pessoa? Qual a fonte? Uma meta global não deve ser rateada por vendedor sem regra.
- Qual período padrão faz sentido e qual comparação importa: período anterior, mesmo mês do ano passado ou meta?
- Quais filtros e detalhamentos são necessários? Quem pode ver valores, contatos e resultados de outros vendedores?
- Desktop dentro da Kommo, celular ou TV? Há marca, cores e um exemplo visual desejado?
- Qual atualização é suficiente: diária, a cada poucos minutos ou após mudanças? Há volume, hospedagem, orçamento ou stack existente a respeitar?

Escolhas opcionais podem receber padrões explícitos. Permissões e significado de valores não podem ser adivinhados em produção. Token administrador no backend não deve ignorar o acesso de cada pessoa ao relatório.

### Eventos e integrações opcionais

Pergunte sobre Meta somente se fizer parte do objetivo. Separe prévia didática, eventos enviados, confirmação técnica e atribuição. Não criar uma conta Meta ou enviar eventos para demonstrar um painel. Se houver envio real solicitado, identificar fonte, consentimento aplicável, deduplicação e contrato atual da API antes de implementar.

## Verificar o que os dados permitem

Classifique cada indicador desejado como:

- **Disponível:** dados e definição suficientes para cálculo.
- **Parcial:** cálculo possível com cobertura ou janela limitada, mostrada no painel.
- **Exige instrumentação:** falta histórico, autoria, investimento ou outra fonte. Proponha registrar daqui para frente; não fabrique retrospectiva.

Teste cobertura de campos, duplicidade, datas, valores nulos e semântica dos status. Se não houver acesso, prepare protótipo local com fixtures explicitamente fictícias e deixe o mapeamento pendente. Um snapshot da etapa atual não reconstrói todas as passagens anteriores.

## Briefing de saída

Salve no projeto quando útil, sem credenciais ou dados pessoais:

```text
Negócio e oferta:
Decisões que o BI deve apoiar:
Público e permissões:
Conta autorizada e funis incluídos:
Demo / dados reais / protótipo sem conexão:
Definição de venda e significado dos valores:
Moeda, fuso e período padrão:
Indicadores prioritários (normalmente 5–8 na primeira tela):
Filtros e detalhamento:
Metas e comparações:
Atualização, hospedagem e acesso:
Qualidade dos dados, limitações e instrumentação necessária:
Premissas adotadas e dúvidas que ainda bloqueiam cálculos:
```

Para cada indicador prioritário, monte um contrato:

| Indicador / decisão | Fórmula e unidade | População e exclusões | Data e janela | Fonte/campo | Limitação |
|---|---|---|---|---|---|
| Conversão / avaliar fechamento | ganhos ÷ encerrados, % | apenas comercial; excluir negócios inválidos conforme regra acordada | fechamento no período | pipeline, status, closed_at | não mede conversão da coorte de entrada |
| Agendamentos IA / avaliar agenda | contagem de eventos distintos | autoria IA comprovada; regra de reagendamento definida | data do agendamento | eventos ou campos validados | se só há marco por lead, contar leads agendados |

O briefing orienta a implementação. Não exige uma reunião extra ou confirmação ritual; esclareça apenas os pontos materiais ainda sem resposta e execute o escopo já solicitado.
