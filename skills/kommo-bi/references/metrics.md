# Métricas que não enganam

| Indicador | População e cálculo |
|---|---|
| VGV vendido | Soma de `price` em leads comerciais ganhos, com fechamento dentro do período. Não chamar de comissão ou lucro. |
| Conversão de encerrados | Ganhos ÷ (ganhos + perdidos), ambos encerrados no período. Sem encerrados: null/“—”, não 0% inventado. |
| Estoque aberto | Leads atualmente em estágios abertos. Filtros dimensionais valem; filtro de período não altera o estoque atual se assim rotulado. |
| Coorte de entrada | Leads com entrada comercial no intervalo. Conte os que atingiram cada marco até o fim do intervalo. |
| Taxa por etapa | Alcançaram etapa B ÷ elegíveis que alcançaram A, com mesma coorte e janela. Salto de etapa precisa de regra explícita. |
| Agendamentos por IA | Marcos de agendamento no período com indicador de autoria IA. Tag de atendimento não basta. Se contar leads, rotular leads agendados, não total de visitas. |
| Conversão da prospecção | Passagens ao comercial registradas no período. Não considerar “ganho” da prospecção como venda imobiliária. |
| Rankings | Informar se o ranking é por entrada, estoque, quantidade vendida ou VGV. |
| Eventos Meta | Contagem separada por simulado, tentado, aceito e atribuído. Nunca presumir atribuição a partir de um HTTP 200. |

Mudanças de etapa exigem histórico durável se a análise for histórica. O estado atual não diz por quais etapas um lead passou nem em que datas. Campos de marcos podem servir a uma demo identificada; produção deve preservar eventos, inclusive reabertura, reagendamento, retrocesso e múltiplas visitas.

Períodos devem usar um fuso explícito. Use o fuso do negócio (por exemplo, America/Sao_Paulo), sem depender do fuso da máquina. Trate o fim do dia e do mês nesse fuso. Validar `from <= to`. Exibir data de entrada e de fechamento separadamente.

Testes úteis: ganho na prospecção não entra em VGV; sem dados não gera NaN; combinação de filtros reduz a base corretamente; estoque atual independe do período; conversão usa encerrados, não entradas; record reaberto não continua na venda atual; horário na virada do dia respeita o fuso.
