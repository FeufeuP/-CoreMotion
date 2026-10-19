# CoreMotion — Inventário de tudo o que falta (Etapa 5)

**Documento:** consolidação única de lacunas, pendências e bloqueios
**Data:** 19/10/2026
**Versão:** 1
**Commit inspecionado:** `b0827ecec5b09c148e7beb2ca1f0d770b8a037a7` (`main` → branch da sessão `arena/fa9f843f-coremotion`)
**Método:** releitura do código deste checkout (grep/sed em arquivos reais) + leitura dos diagnósticos em `docs/etapa-5/diagnosticos/`, dos contratos em `docs/etapa-5/contratos/` e do `STATUS-EXECUCAO.md`. Nenhum comando de escrita, migração ou teste destrutivo foi executado nesta rodada.
**Relação com outros documentos:** este arquivo **não substitui** `DOCUMENTO-FINAL-DE-EXECUCAO.md` (o guia) nem os diagnósticos (a evidência). Ele é o **índice do que ainda não existe**. Se este documento contradisser um diagnóstico sobre o código, o código vence: confira a linha citada.

> **Regra de integridade deste inventário.** Todo item abaixo está em um destes estados e nada além deles:
> `FALTA` (não existe), `PARCIAL` (existe, insuficiente), `BLOQUEADO` (depende de acesso/decisão externa),
> `PENDENTE` (depende de dado humano que não pode ser presumido), `NÃO VERIFICADO` (possível, mas ainda não comprovado em execução).
> Nenhum item pode ser marcado `PRONTO` por geração de texto, build que passa ou afirmação de IA.

---

## 1. Resumo em números

| Grupo | Itens | Mais crítico |
|---|---:|---|
| Bloqueadores de entrega (`P0-01`…`P0-03`) | 3 | credencial viva em repositório público |
| Frente 1 — identidade, acesso, banco (`P1-01`…`P1-13`) | 13 | nenhuma fronteira de autorização no servidor |
| Frente 2 — catálogo, negócio, comunidade (`P2-01`…`P2-10`) | 10 | checkout e anúncios aceitando dados do cliente |
| Frente 3 — TCC, requisitos, diagramas (`P3-01`…`P3-10`) | 10 | TCC não começou; sem diagrama válido para os papéis reais |
| Frente 4 — testes, README, entrega (`P4-01`…`P4-11`) | 11 | zero testes executados e zero README |
| Contratos e decisões (`D-01`…`D-11`) | 11 | D-01 a D-10 sem registro de aprovação |
| Dados acadêmicos (`A-01`…`A-10`) | 10 | autores, banca e definição de "publicar no GitHub" |
| Higiene de repositório (`R-01`…`R-08`) | 8 | CI citado em `CONTRIBUTING.md` não existe |
| **Total** | **76** | |

**Distribuição por estado:** `FALTA` 45 · `PENDENTE` 22 · `PARCIAL` 7 · `BLOQUEADO` 2. Nenhum dos 76 itens está concluído.
Fora da contagem, 6 verificações permanecem `NÃO VERIFICADO` (seção 9): podem até já funcionar, mas não há evidência.

---

## 2. Bloqueadores de entrega (P0) — faltam antes de qualquer outra coisa

| ID | O que falta | Evidência no código | Estado | Dono |
|---|---|---|---|---|
| `P0-01` | **Rotacionar a senha do Postgres** exposta no repositório público e no bundle do cliente. Sem isso, remover o texto do código não invalida nada | `lib/db.ts:8-9` (`DEFAULT_DATABASE_URL` com usuário e senha, valor redigido aqui); `components/SupabaseConfigModal.tsx:29-33` (template de `.env` dentro de componente `'use client'`); `lib/supabase.ts:3-4` e `services/supabaseClient.ts:3-4` (URL e anon key como fallback) | **BLOQUEADO** — só uma pessoa com acesso ao Supabase executa | Frente 1 |
| `P0-02` | **Fronteira de autorização no servidor.** Nenhuma rota de API nem Server Action lê a sessão; todas aceitam `role`, `userId`, `seller_id`, `owner_id` e preços vindos do cliente | `app/api/users/route.ts` (GET/PATCH/DELETE públicos), `app/api/products/route.ts`, `app/api/stores/route.ts`, `app/api/listings/route.ts`, `app/api/auth/sync/route.ts`, `app/actions/products.ts:7-31`, `app/actions/stores.ts:7-30`, `app/actions/orders.ts:7-46`; `grep` por `getUser`/`cookies` em `app/api` não retorna nada | `FALTA` | Frente 1 (núcleo) + Frente 2 (rotas do domínio) |
| `P0-03` | **Login que aceita senha inválida.** `signInWithPassword` com erro gera apenas `console.warn` e o fluxo continua, associando um `supabaseId` fabricado (`usr_<timestamp>`) ao cadastro existente e devolvendo `success: true` | `services/auth.ts:88-134` (ramo `else if (error)` nas linhas ~112-115; `return { success: true }` em ~129), `lib/db-queries.ts:143-157` (`syncSessionWithDb`) | `FALTA` | Frente 1 |

**Contaminação de PII junto ao P0-01:** além da credencial, o bundle do cliente publica **dois endereços de e-mail pessoais** usados como lista de administradores (`lib/store.tsx:40`, `lib/db-queries.ts:5-6`, `components/AdminDashboard.tsx:94,213,1151`, `lib/initial-data.ts:6`, `services/auth.ts:10-20`). Faltam: remover a lista, anonimizar o histórico e tratar a exposição pessoal (LGPD) — item `P1-05`.

---

## 3. Frente 1 — Identidade, acesso, banco e scripts

| ID | O que falta | Onde deveria estar / evidência | Estado | Critério de aceitação mínimo |
|---|---|---|---|---|
| `P1-01` | Sessão server-side (cookie httpOnly) e **um único helper** de verificação usado por toda rota e action | `lib/supabase.ts`, `middleware.ts` | `FALTA` | Anônimo → 401; sem permissão → 403; nenhum dado sensível vem do cliente |
| `P1-02` | Papel **`supervisor`** em qualquer lugar do projeto | `grep -ri supervisor` em `*.ts`/`*.tsx`/`*.sql`/`*.mjs` → **zero ocorrências** | `FALTA` | `lib/types.ts`, tipos de API, RLS, painel e diagrama concordam com 3 níveis |
| `P1-03` | Modelo único de papéis. Hoje há **quatro** definições divergentes: `visitor\|user\|seller\|admin` (`lib/types.ts:1`), `admin\|merchant\|seller\|user` (migração), `athlete` como padrão (`lib/db-queries.ts:49,112`) e um `user_role` com `visitor` nunca aplicado (`lib/supabase.ts`) | ver coluna | `PARCIAL` | Uma fonte de verdade por camada, sem cast arbitrário `as UserRole` |
| `P1-04` | `public.users` **criada por script do repositório**. As APIs a consultam (`lib/db-queries.ts:77-158`) e `scripts/organize-database.mjs:58-75` faz `INSERT` nela, mas a única migração (`20250101000000_coremotiom_initial_schema.sql`) cria `profiles`, `stores`, `products`, `orders`, `community_posts` | `supabase/migrations/` tem 1 arquivo | `FALTA` | Ambiente limpo recriado só com `supabase/migrations/` + `scripts/` documentados |
| `P1-05` | Remoção da **regra de admin por e-mail/prefixo** (`startsWith('mattheusxmljz')`, `startsWith('professorchines')`, 2 e-mails fixos) no cliente, no serviço e no SQL (`is_admin()`, trigger ~`:159,204`) | `lib/store.tsx:32-48`, `lib/db-queries.ts:11-18`, `services/auth.ts:10-20`, `services/authService.ts:15-22`, migração `:30-41` | `FALTA` | Bootstrap administrativo único, autenticado, auditado e fora do fluxo público |
| `P1-06` | **RLS sem trava de coluna**: `profiles_update_policy` permite `UPDATE` no próprio perfil `USING (auth.uid() = id OR public.is_admin())`, sem `WITH CHECK` — autopromoção por REST | migração `:234-236` | `FALTA` | Alterar o próprio `role` falha no banco, não só na UI |
| `P1-07` | **RLS de INSERT ampla** (`OR auth.role() = 'authenticated'`) e `GRANT ALL` para `anon`/`authenticated` | migração `:249,266,283,300,312-314` | `FALTA` | `owner_id`/`seller_id`/`author_id` = `auth.uid()`; privilégios mínimos |
| `P1-08` | **Trigger de cadastro que aceita `role` do metadado** (`admin`, `merchant`, `seller`) | migração `:159-165` | `FALTA` | Cadastro público sempre resulta em `user`; teste negativo registrado |
| `P1-09` | **Modo demonstrativo separado do ambiente real**: sumiu o caminho honesto — hoje `loginAsMasterAdmin()` + botões "Acesso Rápido 1 Clique (👑 Super Admin)" + seletor "Modo" na sidebar abrem o painel admin de qualquer visitante | `components/AuthModal.tsx:51-65,150-200`, `lib/store.tsx:634-642`, `components/AdminDashboard.tsx:78-107`, `components/Sidebar.tsx:455-485` | `FALTA` | Sem demo em produção; se existir, flag + banner `SIMULAÇÃO` + sem dados reais |
| `P1-10` | **`localStorage` como fonte de identidade**: `coremotiom_state_v1` guarda `user` (inclusive `role`) e o painel decide acesso por `isUserAdmin(user?.email)` | `lib/store.tsx:250,351,362`, `components/AdminDashboard.tsx:78` | `FALTA` | Editar `localStorage` e recarregar não promove ninguém |
| `P1-11` | **Auditoria de ações sensíveis** (mudança de papel, ban, exclusão, verificação de loja, status de pedido) — não existe tabela nem gravação | ausente em todo o repositório | `FALTA` | Registro com autor, data, alvo e motivo, consultável |
| `P1-12` | **Exclusão de usuário sem transação e sem anonimização**, apagando `auth.users`/`auth.identities` direto pela credencial `postgres` | `lib/db-queries.ts:212-241` | `FALTA` | Exclusão lógica + transação + auditoria |
| `P1-13` | `middleware.ts` que **não protege rota nenhuma** (só injeta `x-coremotiom-platform` e devolve cedo para `/api`) e SSL com `rejectUnauthorized: false` em `lib/db.ts:52-55` | `middleware.ts:5-25` | `PARCIAL` | Middleware para páginas administrativas + TLS verificado; APIs ainda verificam sessão no handler |

## 4. Frente 2 — Catálogo, negócio, comunidade e checkout

| ID | O que falta | Evidência | Estado | Critério de aceitação mínimo |
|---|---|---|---|---|
| `P2-01` | **Persistência real** em vez de fachada: `INITIAL_PRODUCTS/STORES/USERS/COMMUNITY_POSTS/COACHES` são usados como estado inicial **e como fallback de erro** | `lib/store.tsx:181-189`, `services/products.ts:43-50`, `services/stores.ts:26-28` | `PARCIAL` | API fora do ar ⇒ UI de erro/vazio, nunca catálogo "cheio" falso |
| `P2-02` | **Verificação de loja gravando o status errado**: a solicitação envia `approve: false` e o banco grava `rejected`, enquanto a tela anuncia `pending` | `services/stores.ts:87-100`, `lib/db-queries.ts:568-585`, `lib/store.tsx:892-910` | `FALTA` | Solicitação ≠ aprovação; `pending` persistido e visível ao supervisor |
| `P2-03` | **Checkout sem sessão e com total vindo do cliente** | `components/CheckoutModal.tsx:56`, `app/actions/orders.ts:7-46` | `FALTA` | Sem login não há pedido; subtotal/frete/total/estoque recalculados no servidor |
| `P2-04` | **Pagamento e custódia apresentados como reais**: PIX montado com `Math.random()` (`services/orderService.ts:7-20`) e outro PIX no navegador com QR de `api.qrserver.com`; a UI diz "Transação criptografada com custódia segura" (`components/CheckoutModal.tsx:125`); `confirmPaymentSandbox` grava `payment_status='completed'` com toast "custódia garantida" (`lib/store.tsx:822-836`) | ver coluna | `FALTA` | Toda promessa financeira removida ou rotulada `SIMULAÇÃO`; nenhum pedido marcado como pago sem PSP |
| `P2-05` | **Estados de UI** (`loading`, `empty`, `success`, `error`, `denied`) nas telas do domínio | exigidos em `contratos/contrato-integracao.md` §8 | `FALTA` | Cada tela do escopo tem os cinco estados, com evidência |
| `P2-06` | **Tela de perfil/favoritos**: `setActiveView('profile')` existe, `app/page.tsx` não renderiza nada para `profile`; `news` nunca é usada | `components/Sidebar.tsx:336-343`, `lib/store.tsx:55-64` | `FALTA` | Nenhum item de menu leva a área vazia; view inexistente sai do tipo |
| `P2-07` | **Ações administrativas de catálogo que só alteram o navegador** (status de produto/pedido, moderação e denúncia) — persistem só até o F5 | `lib/store.tsx:574-608,1018-1032` | `FALTA` | Efeito persistente comprovado ou rótulo explícito de demonstração |
| `P2-08` | **Comunidade e treinadores**: `CoachesView` é 100% `INITIAL_COACHES`, sem backend | `components/CoachesView.tsx` | `PARCIAL` | Integrar ou marcar como não integrado no TCC, sem meia palavra |
| `P2-09` | **`contrato-catalogo.md`**: prometido no guia (seção 9) como artefato da frente 2 | `docs/etapa-5/contratos/` contém só 2 arquivos | `FALTA` | Operações, entradas/saídas e erros reais publicados |
| `P2-10` | **Camada única de serviços**: `services/auth.ts` + `/api/*` no frontend e `services/authService.ts`/`productService.ts`/`storeService.ts` nas Server Actions, com fallbacks diferentes | `services/index.ts:1-7` não exporta as duplicatas | `FALTA` | Uma implementação por domínio; duplicata removida |

## 5. Frente 3 — TCC, requisitos, diagramas e evidência visual

| ID | O que falta | Estado | Observação |
|---|---|---|---|
| `P3-01` | `pessoa-3/requisitos-documentais.md` | `FALTA` | exigido pelo Prompt 3A |
| `P3-02` | Estrutura de capítulos e arquivos de trabalho em `pessoa-3/tcc/` | `FALTA` | a pasta `pessoa-3/` tem apenas `README.md` |
| `P3-03` | TCC em DOCX editável com estilos, sumário por campos e folha de aprovação sem aprovação fictícia | `FALTA` | modelo é PDF; precisa reconstruir estrutura editável (guia §12) |
| `P3-04` | Exportação em PDF e revisão visual do exportado | `FALTA` | sem renderização não há como declarar conformidade |
| `P3-05` | `pessoa-3/revisao-diagramas.md` + atualização das fontes em `scripts/lib/usecase-core.mjs` e `flowchart-core.mjs` | `FALTA` | diagramas atuais não incluem o `Supervisor` porque ele não existe no código |
| `P3-06` | Diagrama de casos de uso legível em A4 **e** em slide (com recortes por módulo) | `FALTA` | existem `Fluxograma/Diagrama C. De Uso/casos-de-uso.pdf` e `fluxograma-usuario.pdf`, porém derivados do catálogo antigo |
| `P3-07` | Matriz de rastreabilidade requisito → caso de uso → tela/API → teste → evidência | `FALTA` | depende dos testes da frente 4 |
| `P3-08` | Catálogo de casos de uso documentados (ator, objetivo, pré/pós-condições, fluxo, alternativas) | `FALTA` | `mestre-casos-de-uso.md` é gerado, não revisado |
| `P3-09` | Roteiro de capturas de tela (com legenda, data, versão e ocultação de dados pessoais) | `FALTA` | **nenhuma captura existe**; sem ferramenta de navegador, não se inventa |
| `P3-10` | Referências verificáveis e apêndices de autoria da equipe | `FALTA` | proibido citar fonte não lida; exemplos do modelo não são referências |

## 6. Frente 4 — Testes, README, apresentação e publicação

| ID | O que falta | Estado | Observação |
|---|---|---|---|
| `P4-01` | **`README.md` na raiz** — hoje simplesmente não existe | `FALTA` | requisito literal do enunciado |
| `P4-02` | Ambiente de teste isolado (banco próprio + contas fictícias) | `FALTA` | sem ele, nada acima é verificável |
| `P4-03` | `pessoa-4/plano-testes.md` | `FALTA` | casos positivos e negativos, 3 perfis |
| `P4-04` | Execução de qualquer teste funcional e `relatorio-testes.md` | `FALTA` | só há `type-check`, `lint`, `build` e `GET /` = 200 |
| `P4-05` | `backlog-falhas.md` com retestes | `FALTA` | |
| `P4-06` | Ferramenta de teste configurada no projeto (Playwright/Vitest/Jest ausentes em `package.json`; zero arquivos `*.test.*`/`*.spec.*`) | `FALTA` | decidir e instalar na frente 4 |
| `P4-07` | `pessoa-4/daily-scrum.md` com registros reais | `PENDENTE` | nenhum registro foi fornecido; proibido reconstruir atas de commits |
| `P4-08` | Apresentação publicada no Google Slides ou PowerPoint Online, com link de leitura testado | `PARCIAL` | dois decks nesta rodada, em `docs/etapa-5/pessoa-4/apresentacao/`: **pitch do produto** (15 slides no Google Slides, para a banca) e **deck de pendências** (16 slides no Slides + PPTX animado, anexo interno da equipe); nenhum dos dois mostra resultado de teste nem tela real; link de leitura ainda não foi publicado nem testado em janela anônima |

### 6.1 Deck de diagnóstico (uso interno da equipe)

| Item | Situação |
|---|---|
| Arquivo principal | Google Slides — `CoreMotion · Etapa 5 — Estado real e tudo o que falta`, 16 slides: <https://docs.google.com/presentation/d/11HCy0Tq585Tmqj5cA3exp3vBcdRbXV9VJabgWo_804U/edit> |
| Conteúdo | capa; legenda dos 5 estados e a regra de honestidade; veredito com métricas da rodada; os 7 entregáveis por estado; as 4 frentes; `P0` da credencial exposta (valor redigido); cadeia de falha de autenticação; hierarquia exigida × real; banco, migrações e RLS; catálogo, checkout, verificação e comunidade como fachada; frontend, UX, a11y e grafia; contagem das 76 lacunas por grupo; decisões `D-01…D-11` e dados `A-01…A-10`; ordem de execução em 7 passos; animações e transições; encerramento com o próximo lote |
| Versão animada | `docs/etapa-5/pessoa-4/apresentacao/CoreMotion-Etapa5-animado.pptx` — 16 slides com transições (`fade`, `push`, `wipe`, `morph`), entrada de conteúdo por parágrafo a cada clique e notas do apresentador. Gerado por `gerar-apresentacao-animada.py` (mesma pasta), que escreve `p:transition`/`p:timing` direto no XML PresentationML |
| Por que o PPTX existe | a API do Google Slides (v1, Apps Script e o conector usado) **não expõe** request de transição de slide nem de animação de objeto — só forma, cor, texto, tabela, vídeo, z-order e fundo. Motion no Slides precisa ser aplicado no editor ou vindo de um arquivo que já o traga |
| Falta no deck | ① aplicar **Transições → Esmaecer 0,6 s → Aplicar a todos os slides** no editor (2 min) para o link do Slides ter o mesmo movimento; ② decidir a plataforma exigida e publicar o link de leitura, testado em janela anônima; ③ este deck passa a ser **anexo interno**: a apresentação pública da Etapa 5 é o pitch do produto (§6.2), e o deck de defesa continua devendo evidência de teste e telas reais; ④ conferir nomes, instituição, período e grafia oficial (itens `A-01…A-04`) antes de qualquer exportação |
| Regra mantida | nenhum slide afirma que um item está concluído; toda asserção aponta arquivo e linha; e-mail pessoal mascarado e credencial redigida |

### 6.2 Pitch do produto — o deck que vai para a banca

| Item | Situação |
|---|---|
| Arquivo principal | Google Slides — `CoreMotion · Pitch — comprar, vender e viver o mesmo tênis`, 15 slides: <https://docs.google.com/presentation/d/1lcx5Dsv7ojEZM58hA5zDW_bMt6lAD_-8g2sOuvxvSBQ/edit> |
| Objetivo | vender o site para a banca: o produto, as funções, as mecânicas de confiança e as atualizações que serão implementadas — não é um deck de pendências |
| Conteúdo | capa com as três linhas do produto; problema (procedência, vitrine do lojista pequeno, preço de revenda, compra separada do treino); solução em quatro pilares; fluxo do comprador em 6 passos; fluxo do lojista em 5 passos; seis mecânicas de confiança; papéis (4 de hoje + supervisor como próxima onda); ecossistema (comunidade, treinadores com CREF, atletas com `sponsorship_status`, editorial); SmartScan (entrada → análise → saída); arquitetura Next.js 15/App Router, `app/api` + `app/actions` + `services`, Postgres/Supabase com RLS; três colunas **NO AR HOJE / EM CONSTRUÇÃO / PRÓXIMA ONDA**; roadmap em 3 ondas (~16 semanas); riscos e mitigação; métricas com north star; pedido à banca |
| Regra de honestidade | função que não está no ar aparece rotulada **EM CONSTRUÇÃO** ou **PRÓXIMA ONDA**; o SmartScan é mostrado como componente pronto **fora da navegação**; nenhum número de tração existe no deck (a coluna de métricas declara a ausência de baseline); credencial citada como valor redigido e e-mail pessoal mascarado |
| Versão animada | `docs/etapa-5/pessoa-4/apresentacao/CoreMotion-Pitch-animado.pptx` — 15 slides em 13,33" × 7,5" com transições (`fade`/`morph`/`push`/`wipe`, 650 ms) e entrada de cada bloco de conteúdo a um clique (Appear + fade, 520 ms, `build="p"` por parágrafo), mais as notas do apresentador. Gerado por `gerar-pitch-animado.py`, que escreve `p:transition`/`p:timing` direto no XML PresentationML. Fontes do arquivo: Arial Black / Arial / Consolas — sem depender de Archivo Black ou Montserrat instalados na máquina da banca |
| Roteiro de fala | `docs/etapa-5/pessoa-4/apresentacao/roteiro-pitch.md` — fala de abertura e tempo por slide (~11 min), as três decisões pedidas à banca e os cuidados ao apresentar |
| Fontes | `lib/types.ts`, `components/` (`MarketplaceView`, `StoresView`, `CheckoutModal`, `CommunityView`, `CoachesView`, `SellC2CView`, `SmartScanView`, `AdminDashboard`), `app/api/`, `app/actions/` no commit `b0827ec`; estados e ondas derivados de `PENDENCIAS-E-LACUNAS.md` |
| Falta no deck | ① aplicar transição no editor do Slides, se a exibição for pelo link (a API não grava movimento — o PPTX animado desta pasta já traz o pacote); ② telas reais do produto, quando houver ambiente com banco funcionando; ③ nome/orientador/banca, que dependem dos itens `A-01…A-04` |
| Não substitui | o deck de defesa exigido pelo roteiro: sem `relatorio-testes.md` não há evidência de teste para apresentar — este pitch é a defesa do **produto**, não a da qualidade verificada |

| `P4-09` | `checklist-entrega.md` e `entrega-final.md` com os campos do professor | `FALTA` | |
| `P4-10` | Verificação dos links públicos em janela anônima (repositório, TCC, slides) | `BLOQUEADO` | depende de publicação autorizada |
| `P4-11` | Validação das instruções do README em ambiente limpo | `FALTA` | não é possível validar um README que não existe |

## 7. Decisões que travam trabalho (só a equipe decide)

| ID | Decisão | Onde registrada | Consequência enquanto não decide |
|---|---|---|---|
| `D-01` | Lojista é papel de acesso ou vínculo `stores.owner_id`? | `contratos/matriz-permissoes.md` §5 | `lib/types.ts`, migração e RLS não podem ser fechados |
| `D-02` | Supervisor/Admin podem criar loja? | idem | contrato de lojas |
| `D-03` | Quem aprova verificação de loja? | idem | `P2-02` sem dono de aprovação |
| `D-04` | Supervisor pode banir conta? | idem | matriz do painel admin |
| `D-05` | Supervisor vê lista de usuários (completa/mínima/não)? | idem | `P1-…` escopo de `GET /api/users` |
| `D-06` | Supervisor vê/edita pedidos? | idem | contrato de pedidos |
| `D-07` | Admin vê financeiro por loja ou agregado? | idem | relatórios administrativos |
| `D-08` | Quem administra segredos de integração? | idem | sem resposta, `P0-01` fica sem processo |
| `D-09` | Como isolar o modo demo (flag, rota, remover)? | idem | `P1-09` |
| `D-10` | Admin pode se rebaixar/excluir? | idem | regras de proteção do último admin |
| `D-11` | **`contrato-catalogo.md` ainda não existe** | `docs/etapa-5/contratos/` | frente 2 implementa "contra o próprio plano" em vez de contrato publicado |

As duas matrizes publicadas (`matriz-permissoes.md`, `contrato-integracao.md`) estão marcadas como **RASCUNHO** e descrevem o **alvo**, não o implementado.

## 8. Dados humanos ausentes (não presumíveis por IA)

| ID | Dado | Usado em | Estado |
|---|---|---|---|
| `A-01` | Grafia oficial: `CoreMotion` × `CoreMotiom` × `Core Motiom` | `metadata.json` e `app/layout.tsx` usam **CoreMotiom**; o SQL usa "CORE MOTIOM"; os docs usam CoreMotion | `PENDENTE` |
| `A-02` | Nomes completos dos 4 integrantes e a função de cada um | capa, folha de rosto, resposta ao professor | `PENDENTE` |
| `A-03` | Instituição, curso, cidade e período reais | capa/folha de rosto | `PENDENTE` (modelo diz Colégio Estadual Prof. Júlio Szymanski / Técnico em Desenv. de Sistemas / Araucária / 3.º trim. 2026 — confirmar) |
| `A-04` | Orientador e coorientador | folha de rosto | `PENDENTE` |
| `A-05` | Banca, data de defesa, conceito | folha de aprovação | `PENDENTE` — proibido fabricar |
| `A-06` | Prazo, duração da apresentação e formato aceito de links | defesa e resposta final | `PENDENTE` |
| `A-07` | Significado de "sistema publicado **apenas** no github.com" (código? demo? ambos?) | entrega | `PENDENTE` — `next.config.ts` usa `output: 'standalone'`; GitHub Pages não executa o backend |
| `A-08` | Autorização para rotacionar credencial, limpar histórico Git e tornar visibilidades públicas | `P0-01`, `P4-10` | `PENDENTE` |
| `A-09` | Segundo PDF de requisitos da Etapa 5 (se existir) | guia §1 | `PENDENTE` |
| `A-10` | Consentimento para uso de imagens reais dos integrantes | Daily Scrum, slides | `PENDENTE` |

## 9. Verificações que ainda **não** existem (o que não podemos afirmar)

- Se as políticas RLS do repositório estão de fato aplicadas no banco real.
- Se existe acesso indevido registrado nos logs do Supabase desde a exposição.
- Se `public.users` existe no banco atual (não existe no versionamento).
- Comportamento de autorização em execução (401/403), persistência após F5 e isolamento por dono.
- Renderização visual: responsividade, foco de teclado, contraste, hidratação — **nenhuma captura foi feita**.
- 23 avisos `@next/next/no-img-element` seguem abertos e o build **ignora ESLint** (`next.config.ts: eslint.ignoreDuringBuilds: true`).

## 10. Higiene de repositório e divergências de documentação

| ID | Lacuna | Evidência | Estado |
|---|---|---|---|
| `R-01` | `.github/workflows/ci.yml` inexistente, embora `CONTRIBUTING.md` afirme CI/CD com GitHub Actions + Vercel e `npm run ci` exista no `package.json` | `ls .github/workflows` → pasta ausente | `FALTA` |
| `R-02` | Lockfile: só `bun.lock`; não há `package-lock.json` | `ls *.lock` | `PENDENTE` (decidir o gerenciador antes de escrever o README) |
| `R-03` | Zero framework de testes e zero arquivo de teste em `package.json` | ver §6 `P4-06` | `FALTA` |
| `R-04` | Código órfão: `components/SmartScanView.tsx` (356 linhas, sem importador), `components/ui/*` sem uso, `Header/Footer` reexportados, `@google/genai` declarado sem uso no fluxo | `diagnosticos/frontend.md` §1.3, F-09 | `FALTA` (inventário usar/remover) |
| `R-05` | Migração única e com nome grafado errado (`20250101000000_coremotiom_initial_schema.sql`); sem script de *reverter* | `supabase/migrations/` | `FALTA` |
| `R-06` | `.env.example` não documenta `NEXT_PUBLIC_*` como público/privado nem alerta sobre `SUPABASE_SERVICE_ROLE_KEY` no servidor | `.env.example` | `PARCIAL` |
| `R-07` | `docs/etapa-5/auditoria-final.md` (exigida pelo guia §10) e `pessoa-1/auditoria-identidade.md`, `pessoa-2/diagnostico-catalogo.md`, `registro-implementacao.md`, `estado-*.md` | as 4 pastas de pessoas contêm **só `README.md`** | `FALTA` |
| `R-08` | Nenhum dos entregáveis finais listados na §9 do guia (estrutura de pastas) foi criado; `STATUS-EXECUCAO.md` ainda referencia a branch `arena/92deaf3d-coremotion` da rodada anterior | `docs/etapa-5/STATUS-EXECUCAO.md` | `PARCIAL` |

## 11. Ordem de execução recomendada (sem esperar outra frente)

1. **`P0-01`** rotação da credencial por quem tem acesso — antes disso, qualquer push é prematuro.
2. **`P0-02` + `P1-01`** helper de sessão e aplicação em todas as rotas (lote B1).
3. **`P1-02/03/05/06/07/08`** papéis, migração incremental e RLS (lote B2/B3), depois de registrar `D-01…D-10`.
4. **`P1-09/10` + `P2-01`** remover demo/`localStorage`/fachada (lote F0/F2).
5. **`P2-02/03/04/05`** verificação de loja, checkout, rótulos de simulação e estados de UI (F1/F3).
6. Em paralelo desde o dia 1: **`P4-01…P4-06`** (ambiente, testes, README) e **`P3-01…P3-06`** (requisitos, estrutura, diagramas).
7. Só no fim: **`P4-07…P4-11`** (Daily, slides publicados, checklist, links) e `auditoria-final.md`.

## 12. Checklist de liberação (marcar apenas com evidência anexada)

- [ ] `P0-01` a [ ] `P0-02` a [ ] `P0-03` resolvidos e **retestados em execução**
- [ ] `Supervisor` existe em código, banco, painel e diagrama
- [ ] Banco limpo recriado apenas com os arquivos do repositório
- [ ] Nenhum segredo, e-mail pessoal ou lista de admin no bundle do cliente
- [ ] Checkout com sessão, total no servidor e simulações rotuladas
- [ ] `README.md` validado em ambiente limpo (ou com limitações declaradas)
- [ ] `plano-testes.md` + `relatorio-testes.md` com resultados reais e falhas visíveis
- [ ] TCC em DOCX/PDF conforme o modelo, sem aprovação fabricada e com `PENDENTE` onde falta dado
- [ ] Casos de uso e fluxogramas compatíveis com o código, legíveis em A4 e no slide
- [ ] Daily Scrum com presença e imagens reais, consentidas
- [ ] Slides publicados na plataforma exigida e links testados em janela anônima
- [ ] Resposta ao professor preenchida com nomes e URLs verificadas, sem colchetes
- [ ] `docs/etapa-5/auditoria-final.md` registrado, sem "100% concluído" enquanto houver `FALTA`

---

*Documento gerado por leitura do repositório. Credenciais não são reproduzidas aqui; os valores permanecem apenas onde já estavam — o que, exatamente, é o item `P0-01`.*
