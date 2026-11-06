# Uma demonstração imobiliária

Exemplo adaptável, não quantidade obrigatória: 96 negócios comerciais e 24 prospectados, contatos fictícios com email example.com e sem telefone roteável. Use marca identificável para reconciliar carga repetida. Não disparar WhatsApp, SMS ou e-mail.

Comercial: Novo lead → Qualificado → Agendado → Orçamento/proposta → Ganho ou perda.
Prospecção: Em prospecção → Responderam → Ganho (mover ao comercial) ou perda.

Campos: origem; UTMs source/medium/campaign/content/term; empreendimento; construtora; região; tipo de imóvel; atendimento por IA; agendamento por IA; convertido da prospecção e sua data. Reaproveite campos/tags pelo nome e tipo, sem criar equivalentes redundantes.

Use distribuições variadas e coerentes. Um lead com proposta deve ter data de qualificação anterior; uma venda não deve preceder sua entrada. Se forem marcos inventados para aula, use “demo” nos campos e na interface. Não crie timestamps de eventos históricos afirmando que a API observou aquelas transições.

Passagem de funil: mova o mesmo lead, preserve campos e contato, defina a nova etapa e retire o fechamento anterior se a API exigir. Teste com um lead sintético e verifique a mesma identidade após duas execuções. Documente se é webhook, cron ou ação manual.

Meta: eventos comuns do exemplo são Lead, Schedule, Purchase. QualifiedLead, ProposalSent e LostLead podem ser eventos personalizados neste desenho; confirme o contrato atual antes da produção. Não inclua fbp/fbc falsos como se fossem identificadores de anúncios reais. Prévia de payload deve usar placeholders para dados pessoais normalizados/hashed e para `test_event_code`.

Roteiro de aula: mostrar CRM preenchido → comparar um lead com o painel → filtrar origem e região → explicar denominador da conversão → marcar um prospectado como ganho e mostrar a passagem automática → abrir prévia de evento → ensinar hospedagem HTTPS e widget → entregar skill.
