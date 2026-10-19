# Roteiro do deck de pendências — Etapa 5

**Deck:** Google Slides · `CoreMotion · Etapa 5 — Estado real e tudo o que falta` · 16 slides
**Link:** <https://docs.google.com/presentation/d/11HCy0Tq585Tmqj5cA3exp3vBcdRbXV9VJabgWo_804U/edit>
**Versão animada:** `CoreMotion-Etapa5-animado.pptx` (mesma pasta) — transições e entradas já gravadas no arquivo
**Duração-alvo:** ~12 min se apresentado corrido; ~18 min com um clique por bloco de texto
**Base factual:** `docs/etapa-5/PENDENCIAS-E-LACUNAS.md` (76 itens), commit `b0827ec`, leitura de 19/10/2026

> Este deck é de **diagnóstico**, não de defesa. Ele existe para a equipe decidir o que corrigir.
> Quando os testes e o TCC existirem, o deck de defesa precisa ser outro (resultados, telas, riscos).

---

## Slide a slide

| # | Slide | Fala de abertura | Tempo |
|---:|---|---|---:|
| 1 | Capa — *Tudo o que falta, antes de corrigir qualquer coisa* | «Nesta rodada não tocamos o código. Lemos tudo e lacramos o que falta, com arquivo e linha.» | 40 s |
| 2 | Cinco estados, nenhuma promessa | «Todo item do inventário está em FALTA, PARCIAL, BLOQUEADO, PENDENTE ou NÃO VERIFICADO. Só sai de FALTA com execução registrada — build que passa e afirmação de IA não contam.» | 35 s |
| 3 | Veredito — *compila, sobe, nada está provado* | «type-check, lint e build passam e a home responde 200; as rotas `/api/*` caem em 500 e a aplicação volta ao dado local. O build não prova o negócio.» | 50 s |
| 4 | Os 7 entregáveis, um por linha | «Documento final, plano de testes, plano de implementação: faltam. Relatório e Daily existem pela primeira vez. Apresentação: este deck — ainda não é a defesa.» | 1 min |
| 5 | As 4 frentes | «Backend registrou 13 lacunas, frontend 10, documentos 10, qualidade 8. Nenhuma frente abriu código — e nenhuma tem motivo para achar que está adiantada.» | 45 s |
| 6 | P0 — a credencial exposta | «Senha do banco dentro do código, publicada e empacotada no bundle. Apagar o arquivo não apaga o histórico: primeiro se rotaciona, depois se limpa a história. A decisão é de quem tem o acesso.» | 1 min 20 |
| 7 | Autenticação — a cadeia que deixa entrar | «O login que falha ainda devolve sucesso: `console.warn` e segue, com `usr_<timestamp>` fabricado e papel vindo do metadado. Todo o resto do app confia no papel que recebe do cliente. Ajustar a interface do modal não resolve nada.» | 1 min 05 |
| 8 | Hierarquia exigida × real | `supervisor` tem **zero** ocorrências no repositório. Sem a decisão D-01, tipos, migração e RLS ficam sem base. E o botão administrativo de fachada não passa de cosmético: falta sessão no servidor. | 45 s |
| 9 | Banco, migrações e RLS | «As APIs leem `public.users`; a única migração cria `profiles`. O 500 não é detalhe de infraestrutura: é a prova. `GRANT ALL` para `anon` e UPDATE sem `WITH CHECK` deixam o resto frágil.» | 55 s |
| 10 | Catálogo, checkout, verificação, comunidade | «Catálogo: a vitrine está sempre cheia, não reflete o banco. Checkout: PIX com `Math.random()`, QR de serviço externo e “pagamento aprovado” que só existe no navegador — a UI promete o que a rota não faz. Verificação: vira `rejected` silencioso. Comunidade: só estado local.» | 1 min 20 |
| 11 | Frontend, UX, acessibilidade e grafia | «Uma tela só, alternada por `switch`; identidade no `localStorage`; seletor “Modo” para qualquer visitante; admin com um clique. E a marca está escrita de três jeitos diferentes. Responsivo e acessibilidade: NÃO VERIFICADO — sem medição, sem captura.» | 1 min |
| 12 | As 76 lacunas por grupo | «O maior bloco é identidade e acesso, porque dele dependem negócio, comunidade, checkout e entrega. Fora da contagem ficam as 6 verificações sem evidência.» | 45 s |
| 13 | Decisões e dados que só a equipe tem | «Onze decisões da matriz sem ata, dez dados que ninguém pode presumir — inclusive a grafia oficial. Nada aqui trava as outras frentes: registre PENDENTE e siga pelo contrato.» | 50 s |
| 14 | Ordem de execução em 7 passos | «Segurança primeiro, contrato depois, interface por último. Antes do próximo push: nenhum commit novo enquanto a senha antiga valer.» | 1 min |
| 15 | Animações e transições | «A API do Slides grava forma, cor, texto e fundo — não grava transição nem animação de objeto. Por isso o movimento mora no PPTX desta pasta, e no Slides ele é aplicado no editor em dois minutos.» | 45 s |
| 16 | Próximo lote | «Três responsáveis, três tarefas: rotacionar a credencial, bater as decisões em ata, e aí sim deixar o Arena executar o lote B1 com as documentações em dia.» | 30 s |

## Três perguntas que precisam sair da reunião

1. **Quem roda a credencial hoje**, com data e hora registradas (`P0-01`)?
2. **Lojista é papel ou vínculo** (`D-01`)? Sem isso, a frente 1 não decola.
3. **CoreMotion ou CoreMotiom** (`A-01`)? A grafia aparece em três formas diferentes no repositório e em todas as peças do TCC.

## Cuidados ao apresentar

- Não dizer «segurança validada», «testes passando» ou «100% concluído»: nenhuma frase deste deck permite isso.
- Onde o slide diz NÃO VERIFICADO, manter a palavra — não trocar por «deve estar ok».
- Não mostrar a credencial: o valor permanece redigido, inclusive aqui.
- E-mail pessoal: citar só o prefixo que já está no código, nunca o endereço completo.
- Se a banca pedir a demo ao vivo, avisar antes que o banco responde 500 no ambiente do sandbox e que a home exibida vem do catálogo inicial.

## Depois de apresentar

1. Publicar o link de leitura no Slides (ou manter só o PPTX no repositório) e testar em janela anônima — `P4-08`/`P4-10`.
2. Aplicar as transições no editor do Google Slides (passo a passo no slide 15) se o link do Slides for o meio de entrega.
3. Alimentar o deck de defesa com os resultados de `pessoa-4/relatorio-testes.md` quando ele existir — hoje não há o que mostrar.
