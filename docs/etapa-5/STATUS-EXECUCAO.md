# STATUS-EXECUCAO — Etapa 5

**Projeto:** CoreMotion (grafia oficial ainda PENDENTE)
**Branch da sessão:** `arena/92deaf3d-coremotion`
**Commit de referência:** `4f2c1d820e2627eb00ace7eab4139311624f5f1b` (`main`)
**Data desta rodada:** 19/10/2026
**Modo:** diagnóstico integrado e reformulação dos papéis da equipe; nenhuma alteração no código da aplicação
**Versão avaliada:** código deste checkout + documentos em `docs/etapa-5/`
**Execução:** Arena como assistente integrador; resultados precisam de revisão humana

> Esta rodada **não alterou código de aplicação**, não executou migração, não publicou nada
> e não fez push. O que está registrado abaixo foi observado por leitura de código e por
> comandos executados neste ambiente. O que não pôde ser executado está marcado como
> NÃO VERIFICADO ou BLOQUEADO.

---

## 1. Alerta P0 — credencial de banco exposta

**Status: ABERTO — BLOQUEADOR DE ENTREGA. Exige ação humana imediata.**

- O repositório `BIRFeuFeu/-CoreMotion` é **público** (confirmado via `gh repo view`: `isPrivate=false`).
- `lib/db.ts:8-9` contém uma **string de conexão PostgreSQL com usuário e senha embutidos**
  (valor redigido neste relatório) e a usa como fallback quando `DATABASE_URL` não existe.
- `components/SupabaseConfigModal.tsx:29` monta um template de `.env` com a **mesma senha**.
  Esse arquivo é `'use client'`; o build de produção contém a credencial no **bundle do cliente**
  (2 ocorrências da senha em `.next/static`, 3 em `.next/server` — busca feita sem imprimir o valor).
- Consequência: qualquer pessoa pode ler a credencial no GitHub e no JavaScript servido ao
  navegador. Deve ser tratada como **comprometida**, mesmo que o modal nunca seja aberto.

**Ações necessárias (dependem de acesso humano ao Supabase):** rotacionar a senha do banco,
revisar logs de conexão, remover os fallbacks do código e limpar o histórico Git **depois** da
rotação. Detalhes em `docs/etapa-5/diagnosticos/incidente-credenciais-expostas.md`.

---

## 2. Estado por frente

Cada frente é independente e responde pelo próprio estado. A coluna de próxima ação é executada
pela própria frente, sem esperar liberação de outra pessoa.

| Frente independente | Estado nesta rodada | Evidência produzida | Próxima ação da própria frente |
|---|---|---|---|
| Pessoa 1 — Identidade, acesso e administração | DIAGNÓSTICO CONCLUÍDO; P0 de credencial aberto | `diagnosticos/backend.md`, `contratos/matriz-permissoes.md`, `diagnosticos/incidente-credenciais-expostas.md` | Rotacionar a credencial (ação humana) e implementar sessão, papéis e RLS |
| Pessoa 2 — Catálogo, negócio e comunidade | DIAGNÓSTICO CONCLUÍDO | `diagnosticos/frontend.md`, `contratos/contrato-integracao.md` | Implementar persistência, verificação de loja e checkout |
| Pessoa 3 — Documento e diagramas | NÃO INICIADO | `pessoa-3/README.md` | Produzir requisitos documentais, estrutura e diagramas |
| Pessoa 4 — Verificação e entrega | AMBIENTE PRÓPRIO AINDA NÃO MONTADO | `pessoa-4/README.md` | Montar banco de testes e executar o plano |
| Contratos (artefato comum) | RASCUNHO | `contratos/matriz-permissoes.md`, `contratos/contrato-integracao.md` | Registrar as decisões D-01 a D-10 |
| Publicação | A ESCLARECER / AUTORIZAR | Seção 5 | Confirmar o que "apenas no github.com" exige |

## 3. Verificações técnicas realmente executadas

Nenhum destes comandos substitui teste funcional. Build e type-check não validam regras de negócio.

| Comando | Resultado | Limitação |
|---|---|---|
| `npm install --no-package-lock --no-audit --no-fund` | 995 pacotes instalados, sem erro | Não gerou lockfile; `node_modules/` é ignorado pelo Git |
| `npm run type-check` | **PASSOU** (`tsc --noEmit`, exit 0) | Só valida tipos, não comportamento |
| `npm run lint` | **PASSOU** com 23 avisos `@next/next/no-img-element`, 0 erros | `next.config.ts` ignora ESLint no build |
| `npm run build` | **PASSOU** — Next.js 15.5.28, 5 páginas estáticas, rotas `/api/*` dinâmicas | Não prova integração com banco |
| `npm run start -- -H 0.0.0.0 -p 3000` | Servidor subiu; `GET /` retornou **200** | Renderização sem inspeção visual. O Next avisa que, com `output: 'standalone'`, o comando correto seria `node .next/standalone/server.js` — registrar no README |
| `GET /api/products` | **500** — `Connection terminated unexpectedly` | Bloqueio de rede do sandbox ao Supabase; não é bug de código |
| `GET /api/stores` | **500** — `read ECONNRESET` | Idem |
| `GET /api/users` e `?include_internal=true` | **500** — `read ECONNRESET` | Idem |
| Consulta ao banco real, RLS aplicada, seeds | **NÃO VERIFICADO** | Sem credenciais válidas/ambiente autorizado neste sandbox |

**Conclusão desta seção:** o projeto **compila e sobe**, mas **não foi possível validar
persistência, autenticação real nem RLS em execução**. As vulnerabilidades descritas nos
relatórios foram confirmadas por **leitura de código e configuração**, não por exploração.

---

## 4. Bloqueadores identificados

Cada item tem dono declarado. O dono corrige e verifica sem esperar outra frente; as outras registram o efeito no próprio escopo.

1. **Credencial de banco exposta em repositório público e no bundle do cliente** (P0) — frente 1, com ação humana de rotação.
2. **APIs e Server Actions sem verificação de sessão** — qualquer chamada externa pode listar,
   promover, banir e excluir usuários, criar/apagar produtos e lojas (`app/api/*`, `app/actions/*`) — frente 1 no escopo de identidade; frente 2 no escopo de catálogo.
3. **Login contorna o Supabase Auth** quando a senha está errada (`services/auth.ts:88-134`):
   o erro é ignorado e o fluxo segue para sincronização, retornando `success: true` — frente 1.
4. **Hierarquia exigida ausente**: não existe `Supervisor` em nenhum arquivo do projeto; os papéis
   são `visitor`, `user`, `seller`, `admin` (`lib/types.ts:1`) — frente 1.
5. **Autopromoção**: papel admin atribuído por metadado de cadastro no trigger SQL
   (`supabase/migrations/...:159-165`) e por e-mail/prefixo fixo em código; RLS permite
   `UPDATE` do próprio perfil sem restrição de coluna (`:234-236`) — frente 1.
6. **Banco não recriável pelos scripts**: as APIs usam `public.users`, tabela que **não é criada**
   por nenhuma migração nem script; as migrações criam `public.profiles` — frente 1.
7. **Pagamento/custódia não são reais**: PIX é gerado localmente com `Math.random`, o status
   "pago" é gravado por um clique de sandbox e a interface afirma "custódia garantida" — frente 2.
8. **Modo demonstrativo se confunde com sistema real**: login de 1 clique como Super Admin,
   troca de papel pelo menu, dados iniciais locais e ações administrativas que só alteram estado
   do navegador com toast de sucesso — frente 1 na autenticação e troca de papel; frente 2 nos dados e ações do catálogo.
9. **Documentação acadêmica sem dados**: autores, orientador, banca e período não fornecidos;
   TCC e diagramas não podem ser declarados prontos — frente 3, com os campos mantidos como `PENDENTE`.

---

## 5. Informações pendentes (não presumidas)

- [ ] Grafia oficial: o repositório alterna `CoreMotion`, `CoreMotiom` e `Core Motiom`.
- [ ] Nomes completos dos quatro integrantes e vínculo com as funções 1–4.
- [ ] Instituição, curso, cidade, período, orientador/coorientador e banca.
- [ ] Significado de "sistema publicado apenas no github.com" (código, demonstração ou ambos).
- [ ] Prazo, duração da apresentação e formato aceito dos links.
- [ ] Decisão sobre o papel **Supervisor** (escopo exato) e sobre como modelar o lojista (D-01 a D-10).
- [ ] Autorização para rotacionar credenciais e limpar histórico Git.
- [ ] Ambiente de teste isolado com banco próprio — a ser montado pela frente de verificação com os scripts do repositório.

---

## 5.1 Inventário consolidado do que falta

Criado em `docs/etapa-5/PENDENCIAS-E-LACUNAS.md` (19/10/2026): 76 itens lacrados por frente,
com evidência em arquivo e linha, estado (`FALTA`, `PARCIAL`, `BLOQUEADO`, `PENDENTE`,
`NÃO VERIFICADO`), dono e critério de aceitação. Nenhum item está concluído. A seção 4 deste
arquivo lista os bloqueadores; o inventário lista **tudo** o que falta, inclusive os artefatos
documentais que as pastas `pessoa-N/` ainda não contêm.

---

## 6. Arquivos criados ou reorganizados nesta rodada

```
CONTRIBUTING.md   # 4 frentes independentes, sem revisão bloqueante
docs/etapa-5/DOCUMENTO-FINAL-DE-EXECUCAO.md        # papéis reformulados
docs/etapa-5/Documento-Final-Execucao-CoreMotion.docx
docs/etapa-5/PLANO-EQUIPE-E-PROMPTS.md             # papéis reformulados
docs/etapa-5/Plano-Equipe-e-Prompts-CoreMotion.docx
docs/etapa-5/STATUS-EXECUCAO.md
docs/etapa-5/contratos/matriz-permissoes.md
docs/etapa-5/contratos/contrato-integracao.md
docs/etapa-5/diagnosticos/frontend.md
docs/etapa-5/diagnosticos/backend.md
docs/etapa-5/diagnosticos/incidente-credenciais-expostas.md
docs/etapa-5/pessoa-1/README.md
docs/etapa-5/pessoa-2/README.md
docs/etapa-5/pessoa-3/README.md
docs/etapa-5/pessoa-4/README.md
docs/etapa-5/PENDENCIAS-E-LACUNAS.md            # inventário de 76 lacunas (19/10/2026)
docs/etapa-5/pessoa-4/apresentacao/CoreMotion-Etapa5-animado.pptx
docs/etapa-5/pessoa-4/apresentacao/CoreMotion-Pitch-animado.pptx
docs/etapa-5/pessoa-4/apresentacao/gerar-pitch-animado.py
docs/etapa-5/pessoa-4/apresentacao/gerar-apresentacao-animada.py
docs/etapa-5/pessoa-4/apresentacao/roteiro-apresentacao.md      # fala por slide e cuidados
docs/etapa-5/pessoa-4/apresentacao/roteiro-pitch.md             # fala por slide do pitch à banca
```

Dois decks foram criados no Google Slides e estão registrados em
`docs/etapa-5/PENDENCIAS-E-LACUNAS.md`: o **pitch do produto** (15 slides, seção 6.2), que é a
peça para a banca — vende o site, suas funções, mecânicas e as ondas de atualização —, e o
**deck de pendências** (16 slides, seção 6.1), rebaixado a anexo interno da equipe, com o PPTX
animado como portador do movimento que a API do Slides não grava. Em nenhum dos dois há
afirmação de item concluído: o que falta aparece rotulado `FALTA`, `PARCIAL`, `EM CONSTRUÇÃO` ou
`PRÓXIMA ONDA`, e o que depende de dados da equipe fica `PENDENTE`.
O PPTX da mesma pasta carrega transições e entradas por parágrafo gravadas no próprio XML —
a API do Google Slides não expõe esses recursos, então o movimento não pôde ser aplicado lá.

Os diagnósticos deixaram de ficar dentro da pasta de uma pessoa: são insumos compartilhados.
Cada frente tem a própria pasta para registros e evidências.

Nenhum arquivo em `app/`, `components/`, `lib/`, `services/`, `supabase/` ou `scripts/` foi modificado nesta rodada.

---

## 7. Próxima ação recomendada

1. **Antes de qualquer push:** pessoa com acesso ao Supabase rotacionar a senha do banco e
   confirmar a rotação (ver incidente). Sem isso, nenhuma correção resolve o vazamento.
2. Registrar em ata as decisões D-01 a D-10 de `contratos/matriz-permissoes.md`. É uma decisão da
   equipe, tomada uma vez, e não um portão entre frentes.
3. Cada frente segue o próprio diagnóstico em paralelo:
   - frente 1: B0 (segredos), B1/B2 (sessão, papéis, RLS) e F0 (remover admin de demonstração);
   - frente 2: persistência do catálogo, verificação de loja, checkout e estados de UI;
   - frente 3: requisitos documentais, estrutura do TCC e diagramas;
   - frente 4: ambiente de teste próprio, plano e execução dos casos.
4. Nenhuma frente aguarda a conclusão das outras. O único ato conjunto é a liberação final
   (merge e publicação), feita uma vez com a versão verificada.
