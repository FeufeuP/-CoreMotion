# Roteiro do pitch — CoreMotion, o marketplace do corredor

**Deck:** Google Slides · `CoreMotion · Pitch — comprar, vender e viver o mesmo tênis` · 15 slides
**Link:** <https://docs.google.com/presentation/d/1lcx5Dsv7ojEZM58hA5zDW_bMt6lAD_-8g2sOuvxvSBQ/edit>
**Versão animada:** `CoreMotion-Pitch-animado.pptx` (mesma pasta) — transições e entrada por bloco já gravadas no arquivo; gerador `gerar-pitch-animado.py`
**Duração-alvo:** ~11 min corridos; ~14 min com uma pausa por bloco
**Base factual:** `lib/types.ts`, `components/`, `app/api/` no commit `b0827ec` + `docs/etapa-5/PENDENCIAS-E-LACUNAS.md` (76 itens) · leitura de 19/10/2026

> Este é o deck que **vende o site para a banca**: o produto, as funções, as mecânicas e o que vem depois.
> O deck de 16 slides (`roteiro-apresentacao.md`) é o anexo de diagnóstico — fica para a reunião interna da equipe,
> não para a apresentação pública.

---

## Slide a slide

| # | Slide | Fala de abertura | Tempo |
|---:|---|---|---:|
| 1 | Capa — *comprar, vender e viver o mesmo tênis* | «A gente não veio mostrar um site de tênis. Veio mostrar o lugar onde o corredor compra sem medo, vende sem perder dinheiro e continua depois da compra.» | 40 s |
| 2 | O problema — *comprar tênis de corrida é um ato de fé* | Quatro dores: procedência incerta, lojista pequeno sem vitrine, revenda às cegas e a compra separada do treino. Fechar com a frase do rodapé: ninguém quer mais um checkout. | 60 s |
| 3 | A solução — *um só lugar para comprar, vender e treinar* | Apresentar os quatro pilares e o que diferencia: marketplace generalista não entende de corrida, grupo de WhatsApp não prova procedência. | 60 s |
| 4 | Como funciona — comprador | Percorrer os seis passos como narrativa de uso. Se pedirem demo ao vivo, avisar antes: o banco responde 500 no ambiente atual e a vitrine exibida vem do catálogo inicial. | 60 s |
| 5 | Como funciona — lojista | Vender a dor do lojista de bairro. Ele entra pela verificação e fica pelo estoque; as duas peças que faltam (aprovação pelo admin e pedido no servidor) estão nomeadas no rodapé. | 50 s |
| 6 | Mecânicas de confiança | O coração do pitch: selo, condição, cotação, moderação, reputação e ciclo do pedido. Cada um tem campo no modelo de dados — não é promessa de slide. | 60 s |
| 7 | Os papéis | Quatro papéis existem hoje, o quinto (supervisor) é exigência do enunciado e está marcado como onda 1. Se perguntarem por que não está pronto: a decisão `D-01` vem antes do código. | 45 s |
| 8 | Ecossistema | Comunidade, treinadores com CREF, atletas com status de patrocínio e editorial. Citar que a view de notícias já está modelada e falta ligá-la no menu — trabalho pequeno, efeito visível. | 50 s |
| 9 | SmartScan | O diferencial. Deixar claro o estado real: o componente existe, está completo na tela, mas fora da navegação e sem consumir histórico de pedidos. É a peça que vira argumento comercial quando entrar no fluxo. | 50 s |
| 10 | Arquitetura | Responder antes da pergunta: por que não plugar o Supabase amanhã? Porque hoje a store é a fonte de verdade. Primeiro o servidor, depois o resto. | 45 s |
| 11 | Onde estamos | O slide de credibilidade: três colunas — no ar hoje, em construção, próxima onda. Ler a coluna do meio sem rodeios. É aqui que a banca decide se confia no resto do pitch. | 60 s |
| 12 | Roadmap | Três ondas, ~16 semanas. Reforçar a ordem: fundação segura antes de função nova. Cada item tem arquivo e linha no documento de pendências. | 70 s |
| 13 | Riscos | Não esconder nenhum dos quatro. Fechar dizendo que todos já estavam descritos no diagnóstico, com evidência — não apareceram na hora da apresentação. | 45 s |
| 14 | Métricas | North star + quatro metas. Não inventar baseline: sem tráfego real, o que não existe fica `PENDENTE` no documento e entra em vigor com a onda 2. | 40 s |
| 15 | O pedido à banca | Pedir as três coisas uma por uma e parar de falar. A última frase é a que fica: o produto não pede nota, pede para continuar. | 40 s |

## As três decisões que este pitch quer da banca

1. **Validar a onda 1 como próximo passo** — sessão em cookie `httpOnly`, autorização e preço no servidor, rotação da credencial exposta, antes de qualquer função nova.
2. **Aprovar `D-01`** — lojista é papel ou vínculo com a loja? A resposta muda tabela, permissão e o fluxo de verificação.
3. **Autorizar dados de teste** — sem tráfego de teste e consentimento no cadastro, conversão e retenção não têm como serem medidas.

## Cuidados ao apresentar

- Nada de «segurança validada», «testes passando» ou «100% concluído»: os rótulos **NO AR HOJE / EM CONSTRUÇÃO / PRÓXIMA ONDA** existem para serem lidos como estão.
- O SmartScan é apresentado como componente pronto **fora do fluxo** — não como IA em produção.
- A credencial do banco aparece apenas como «valor redigido»; o e-mail pessoal, só mascarado (`mattheusxmljz@…`).
- Número de tração, faturamento e percentual de mercado não existem neste deck: não há medição ainda, e a banca vai perceber se houver.
- Se a apresentação for pelo link do Slides, aplicar antes **Transições → Esmaecer → Aplicar a todos os slides** — a API do Slides não grava movimento. O `CoreMotion-Pitch-animado.pptx` desta pasta já vem com transições e entrada de bloco a cada clique: é o arquivo a usar se a banca exigir PowerPoint.

## Depois de apresentar

1. Registrar em ata as três decisões acima e voltar o resultado para `docs/etapa-5/contratos/matriz-permissoes.md` e `PENDENCIAS-E-LACUNAS.md` (§7).
2. Publicar o link de leitura do pitch (ou exportar) e testar em janela anônima — `P4-08`/`P4-10`.
3. Quando `pessoa-4/relatorio-testes.md` existir, substituir o slide 11 por evidência real de teste e incluir telas nos slides 4, 5 e 9.
