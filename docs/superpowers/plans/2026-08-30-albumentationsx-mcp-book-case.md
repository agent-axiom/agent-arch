# AlbumentationsX MCP Author Case Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a transparent, evidence-backed AlbumentationsX MCP author case to the multilingual practical chapter and its deterministic Russian publisher projection.

**Architecture:** Keep one editorial home in the MCP-versus-A2A practical page, translated in lockstep across Russian, English, and Chinese. Project that case into publisher Chapter 11 through one final deterministic manuscript transformation that replaces generic MCP prose, preserves structural budgets, and adds pinned sources. Guard both surfaces with focused marker, source, size, and reproducibility tests.

**Tech Stack:** Markdown, MkDocs Material, Python 3.12, pytest, the repository's deterministic Russian manuscript transformer, `uv`.

---

## File Map

- `tests/test_docs_surface.py`: multilingual disclosure, source, content, and Russian case-length contract.
- `docs/book/part-iv/practical-mcp-a2a.md`: canonical Russian online author case.
- `docs/book/part-iv/practical-mcp-a2a.en.md`: semantically equivalent English case.
- `docs/book/part-iv/practical-mcp-a2a.zh.md`: semantically equivalent Chinese case.
- `docs/appendix/sources.md`: Russian source-list entries for the official guide and pinned project snapshot.
- `docs/appendix/sources.en.md`: English source-list entries.
- `docs/appendix/sources.zh.md`: Chinese source-list entries.
- `tests/test_ru_manuscript_revision.py`: publisher disclosure, source, word-count, heading-count, and deterministic-regeneration contract.
- `docs/publisher/tools/revise_ru_manuscript.py`: final author-case transformation and publisher source injection.
- `docs/publisher/ru-manuscript-editorial-2026-07-13.md`: regenerated canonical publisher manuscript.

The working tree already contains unrelated publisher files and generated artifacts. Do not edit, stage, or commit them.

### Task 1: Add the multilingual online author case

**Files:**
- Modify: `tests/test_docs_surface.py`
- Modify: `docs/book/part-iv/practical-mcp-a2a.md`
- Modify: `docs/book/part-iv/practical-mcp-a2a.en.md`
- Modify: `docs/book/part-iv/practical-mcp-a2a.zh.md`
- Modify: `docs/appendix/sources.md`
- Modify: `docs/appendix/sources.en.md`
- Modify: `docs/appendix/sources.zh.md`

- [ ] **Step 1: Write the failing multilingual contract test**

Add this test beside the existing MCP/A2A documentation tests in `tests/test_docs_surface.py`:

```python
def test_albumentationsx_mcp_author_case_is_transparent_and_localized() -> None:
    required_by_file = {
        "docs/book/part-iv/practical-mcp-a2a.md": (
            "### 2.1. Авторский кейс: AlbumentationsX MCP — возможность, а не отдельный агент",
            "разработанная автором этой книги",
            "не является официальным продуктом AlbumentationsX",
            "ограничивается настроенным `allowed-root`",
            "не жёстким шлюзом авторизации",
            "не доказывает широкое промышленное внедрение",
            "честную границу доказательств",
        ),
        "docs/book/part-iv/practical-mcp-a2a.en.md": (
            "### 2.1. Author Case: AlbumentationsX MCP Is a Capability, Not a Separate Agent",
            "developed by this book's author",
            "not an official AlbumentationsX product",
            "restricted to the configured `allowed-root`",
            "not a hard authorization gate",
            "does not demonstrate broad production adoption",
            "an honest evidence boundary",
        ),
        "docs/book/part-iv/practical-mcp-a2a.zh.md": (
            "### 2.1. 作者案例：AlbumentationsX MCP 是一种能力，而不是独立智能体",
            "由本书作者开发",
            "并非 AlbumentationsX 官方产品",
            "限制在已配置的 `allowed-root`",
            "并不是硬性的授权门",
            "不能证明已经得到广泛的生产采用",
            "诚实的证据边界",
        ),
    }
    source_urls = (
        "https://albumentations.ai/docs/integrations/mcp/",
        "https://github.com/dKosarevsky/albu-mcp/releases/tag/v1.21.1",
        (
            "https://github.com/dKosarevsky/albu-mcp/tree/"
            "171e2ca44830a16c363c8e3614825f2a0d2215b8"
        ),
    )

    for path, markers in required_by_file.items():
        text = _read(path)
        for marker in (*markers, *source_urls):
            assert marker in text, (path, marker)

    russian = _read("docs/book/part-iv/practical-mcp-a2a.md")
    case = russian.split("### 2.1. Авторский кейс:", 1)[1].split("## 3.", 1)[0]
    assert 180 <= len(re.findall(r"[A-Za-zА-Яа-яЁё0-9]+", case)) <= 220

    _assert_files_contain_all(
        (
            "docs/appendix/sources.md",
            "docs/appendix/sources.en.md",
            "docs/appendix/sources.zh.md",
        ),
        ("AlbumentationsX MCP integration", *source_urls),
    )
```

- [ ] **Step 2: Run the test and confirm that the case is absent**

Run:

```bash
uv run pytest tests/test_docs_surface.py::test_albumentationsx_mcp_author_case_is_transparent_and_localized -v
```

Expected: FAIL on the missing Russian heading.

- [ ] **Step 3: Insert the Russian case**

In `docs/book/part-iv/practical-mcp-a2a.md`, insert the following immediately after `Именно здесь \`MCP\` ложится естественно.` and before `## 3. Когда тебе действительно нужен A2A`:

```markdown
### 2.1. Авторский кейс: AlbumentationsX MCP — возможность, а не отдельный агент

AlbumentationsX MCP — open-source community-интеграция, разработанная автором этой книги. Она не является официальным продуктом AlbumentationsX и не заменяет Python API: сервер даёт MCP-хосту типизированный путь для проверки конвейеров аугментации, небольших локальных превью, сравнения вариантов, фиксации визуальной обратной связи и экспорта принятой конфигурации.[^albu-mcp-guide][^albu-mcp-project]

Архитектурно это возможность, а не отдельный агент. У сервера нет собственной операционной роли, цели или права самостоятельно менять процесс обучения. Он не обучает модели, не загружает удалённые изображения, не перезаписывает наборы данных и не исполняет переданный пользователем произвольный Python-код. Зато граница возможности выражена явно: чтение ограничивается настроенным `allowed-root`, результаты пишутся в отдельный каталог артефактов, запрос проверяется до рендеринга и ограничивается по числу входов и вариантов. Детерминированные seed, манифесты и трассы применённых преобразований помогают воспроизвести результат; профили возможностей уменьшают видимую поверхность инструментов, а снапшоты контрактов и golden evals обнаруживают дрейф интерфейса.

Эти свойства не превращают проект в гарантию безопасности. Узкий `allowed-root` нужно задавать явно; принятие превью остаётся правилом рабочего процесса, а не жёстким шлюзом авторизации; молодой проект не доказывает широкое промышленное внедрение. Переносимый урок скромнее и полезнее: хороший MCP-сервер соединяет узкий доменный контракт, исполняемые ограничения, воспроизводимые артефакты и честную границу доказательств.
```

Append these footnotes beside the existing footnotes at the bottom of the file:

```markdown
[^albu-mcp-guide]: [Albumentations, AlbumentationsX MCP integration](https://albumentations.ai/docs/integrations/mcp/)
[^albu-mcp-project]: [dKosarevsky/albu-mcp, release v1.21.1](https://github.com/dKosarevsky/albu-mcp/releases/tag/v1.21.1) и [снимок исходного кода 171e2ca](https://github.com/dKosarevsky/albu-mcp/tree/171e2ca44830a16c363c8e3614825f2a0d2215b8)
```

- [ ] **Step 4: Insert the English case**

In `docs/book/part-iv/practical-mcp-a2a.en.md`, insert the following immediately after `That is where \`MCP\` fits naturally.` and before `## 3. When You Actually Need A2A`:

```markdown
### 2.1. Author Case: AlbumentationsX MCP Is a Capability, Not a Separate Agent

AlbumentationsX MCP is an open-source community integration developed by this book's author. It is not an official AlbumentationsX product or a replacement for the Python API. Instead, it gives an MCP host a typed path for validating augmentation pipelines, rendering small local previews, comparing variants, recording concrete visual feedback, and exporting an accepted configuration.[^albu-mcp-guide][^albu-mcp-project]

Architecturally, this is a capability rather than a separate agent. The server has no independent operational role, goal, or authority to change the training process. It does not train models, fetch remote images, overwrite datasets, or execute arbitrary user-supplied Python. Its capability boundary is explicit: reads are restricted to the configured `allowed-root`, outputs go to a separate artifact directory, and requests are validated before rendering and bounded by input and variant counts. Deterministic seeds, manifests, and applied-transform traces support reproduction; capability profiles reduce the visible tool surface; contract snapshots and golden evaluations detect interface drift.

Those properties do not turn the project into a security guarantee. A narrow `allowed-root` must be configured explicitly; preview acceptance is a workflow rule, not a hard authorization gate; and a young project does not demonstrate broad production adoption. The transferable lesson is narrower and more useful: a good MCP server combines a focused domain contract, enforceable execution limits, reproducible artifacts, and an honest evidence boundary.
```

Append:

```markdown
[^albu-mcp-guide]: [Albumentations, AlbumentationsX MCP integration](https://albumentations.ai/docs/integrations/mcp/)
[^albu-mcp-project]: [dKosarevsky/albu-mcp, release v1.21.1](https://github.com/dKosarevsky/albu-mcp/releases/tag/v1.21.1) and [source snapshot 171e2ca](https://github.com/dKosarevsky/albu-mcp/tree/171e2ca44830a16c363c8e3614825f2a0d2215b8)
```

- [ ] **Step 5: Insert the Chinese case**

In `docs/book/part-iv/practical-mcp-a2a.zh.md`, insert the following immediately after `这正是 \`MCP\` 最合适的位置。` and before `## 3. 什么情况下你才真的需要 A2A`:

```markdown
### 2.1. 作者案例：AlbumentationsX MCP 是一种能力，而不是独立智能体

AlbumentationsX MCP 是由本书作者开发的开源 community integration。它并非 AlbumentationsX 官方产品，也不取代 Python API；它为 MCP host 提供一条类型化路径，用于验证数据增强 pipeline、生成小批量本地 preview、比较候选方案、记录具体的视觉反馈，并导出已经接受的配置。[^albu-mcp-guide][^albu-mcp-project]

从架构上看，它是一种能力，而不是独立智能体。服务器没有自己的 operational role、目标，也无权自行改变训练流程。它不会训练模型、抓取远程图像、覆盖数据集或执行用户提供的任意 Python 代码。能力边界是明确的：读取被限制在已配置的 `allowed-root`，输出写入独立的 artifact directory，请求在渲染前接受验证，并受输入数和 variant 数限制。确定性 seed、manifest 和 applied-transform trace 支持复现；capability profile 缩小可见工具面；contract snapshot 与 golden eval 用于发现接口漂移。

这些属性并不构成安全保证。狭窄的 `allowed-root` 必须显式配置；接受 preview 是工作流规则，并不是硬性的授权门；年轻项目也不能证明已经得到广泛的生产采用。更可迁移的结论是：好的 MCP server 应把聚焦的领域契约、可执行的运行限制、可复现的 artifact 和诚实的证据边界结合起来。
```

Append:

```markdown
[^albu-mcp-guide]: [Albumentations，AlbumentationsX MCP integration](https://albumentations.ai/docs/integrations/mcp/)
[^albu-mcp-project]: [dKosarevsky/albu-mcp，v1.21.1 release](https://github.com/dKosarevsky/albu-mcp/releases/tag/v1.21.1) 与 [171e2ca 源码快照](https://github.com/dKosarevsky/albu-mcp/tree/171e2ca44830a16c363c8e3614825f2a0d2215b8)
```

- [ ] **Step 6: Add the two source entries to every source appendix**

Add these entries after the two Model Context Protocol sources in each file.

`docs/appendix/sources.md`:

```markdown
- Albumentations, [AlbumentationsX MCP integration](https://albumentations.ai/docs/integrations/mcp/)
- GitHub, [dKosarevsky/albu-mcp release v1.21.1](https://github.com/dKosarevsky/albu-mcp/releases/tag/v1.21.1) и [снимок исходного кода 171e2ca](https://github.com/dKosarevsky/albu-mcp/tree/171e2ca44830a16c363c8e3614825f2a0d2215b8)
```

`docs/appendix/sources.en.md`:

```markdown
- Albumentations, [AlbumentationsX MCP integration](https://albumentations.ai/docs/integrations/mcp/)
- GitHub, [dKosarevsky/albu-mcp release v1.21.1](https://github.com/dKosarevsky/albu-mcp/releases/tag/v1.21.1) and [source snapshot 171e2ca](https://github.com/dKosarevsky/albu-mcp/tree/171e2ca44830a16c363c8e3614825f2a0d2215b8)
```

`docs/appendix/sources.zh.md`:

```markdown
- Albumentations，[AlbumentationsX MCP integration](https://albumentations.ai/docs/integrations/mcp/)
- GitHub，[dKosarevsky/albu-mcp v1.21.1 release](https://github.com/dKosarevsky/albu-mcp/releases/tag/v1.21.1) 与 [171e2ca 源码快照](https://github.com/dKosarevsky/albu-mcp/tree/171e2ca44830a16c363c8e3614825f2a0d2215b8)
```

- [ ] **Step 7: Run the focused online test**

Run:

```bash
uv run pytest tests/test_docs_surface.py::test_albumentationsx_mcp_author_case_is_transparent_and_localized -v
```

Expected: PASS.

- [ ] **Step 8: Commit the online case**

```bash
git add tests/test_docs_surface.py \
  docs/book/part-iv/practical-mcp-a2a.md \
  docs/book/part-iv/practical-mcp-a2a.en.md \
  docs/book/part-iv/practical-mcp-a2a.zh.md \
  docs/appendix/sources.md \
  docs/appendix/sources.en.md \
  docs/appendix/sources.zh.md
git commit -m "docs: add AlbumentationsX MCP author case"
```

### Task 2: Project the case into publisher Chapter 11

**Files:**
- Modify: `tests/test_ru_manuscript_revision.py`
- Modify: `docs/publisher/tools/revise_ru_manuscript.py`
- Modify: `docs/publisher/ru-manuscript-editorial-2026-07-13.md`

- [ ] **Step 1: Write the failing publisher contract test**

Add this test beside the current August MCP and source tests in `tests/test_ru_manuscript_revision.py`:

```python
def test_albumentationsx_mcp_author_case_is_transparent_in_publisher_chapter() -> None:
    text = EXPECTED.read_text(encoding="utf-8")
    chapter_eleven = revision_tool.extract_chapter(text, 11)
    appendix = text.split("## Приложение 4\\.", 1)[1]

    for marker in (
        "Авторский кейс: AlbumentationsX MCP — возможность, а не отдельный агент",
        "разработанная автором этой книги",
        "не является официальным продуктом AlbumentationsX",
        "настроенным `allowed-root`",
        "не является жёсткой авторизацией",
        "не доказывает широкое промышленное внедрение",
        "**S123.**",
        "**S124.**",
    ):
        assert marker in chapter_eleven

    expected_urls = {
        "S123": "https://albumentations.ai/docs/integrations/mcp/",
        "S124-release": "https://github.com/dKosarevsky/albu-mcp/releases/tag/v1.21.1",
        "S124-source": (
            "https://github.com/dKosarevsky/albu-mcp/tree/"
            "171e2ca44830a16c363c8e3614825f2a0d2215b8"
        ),
    }
    for url in expected_urls.values():
        assert appendix.count(url) == 1

    chapter_sources = chapter_eleven.split("### Источники главы", 1)[1]
    for source_id in ("S123", "S124"):
        assert chapter_sources.count(f"**{source_id}.**") == 1

    assert len(re.findall(r"[A-Za-zА-Яа-яЁё0-9]+", chapter_eleven)) <= 4985
    assert len(re.findall(r"^#### ", chapter_eleven, re.MULTILINE)) <= 17
```

- [ ] **Step 2: Run the publisher test and confirm that the case is absent**

Run:

```bash
uv run pytest tests/test_ru_manuscript_revision.py::test_albumentationsx_mcp_author_case_is_transparent_in_publisher_chapter -v
```

Expected: FAIL on the missing author-case heading.

- [ ] **Step 3: Add the deterministic publisher transformation**

Add this function after `apply_technical_book_polish_2026_08_02()` and before `revise()` in `docs/publisher/tools/revise_ru_manuscript.py`:

```python
def apply_albumentationsx_mcp_author_case_2026_08_30(text: str) -> str:
    """Add the disclosed author case without increasing Chapter 11 density."""

    text = _replace_once_in_chapter(
        text,
        11,
        "Теперь типовые проблемы повторяются уже на двух уровнях: на уровне "
        "отдельного адаптера и на уровне всего ландшафта MCP.\n\n"
        "Типовые проблемы очень повторяемы:\n\n",
        "",
        "duplicate Chapter 11 common-problems lead-in",
    )

    author_case = """**Авторский кейс: AlbumentationsX MCP — возможность, а не отдельный агент.** AlbumentationsX MCP — open-source community-интеграция, разработанная автором этой книги; она не является официальным продуктом AlbumentationsX и не заменяет Python API (см. источники **S123**, **S124**). Сервер даёт MCP-хосту типизированный путь для проверки конвейеров аугментации, ограниченных локальных превью, сравнения вариантов, обратной связи и воспроизводимого экспорта.

Это возможность, а не самостоятельная операционная роль: она не владеет целью или политикой и не обучает модель. Чтение ограничивается настроенным `allowed-root`, запись — отдельным каталогом артефактов; до рендеринга проверяются запрос и лимиты, а seed, манифесты, трассы, профили возможностей, снапшоты контрактов и golden evals делают поведение наблюдаемым.

Граница доказательств тоже явна: узкий корень нужно настроить, принятие превью не является жёсткой авторизацией, а молодой проект не доказывает широкое промышленное внедрение."""
    text = _replace_pattern_once_in_chapter(
        text,
        11,
        r"Именно поэтому песочница не должна быть галочкой в проверочном списке\. "
        r"Она должна быть частью модели выполнения\.\n\n"
        r"\*\*Короткое правило\.\*\*\n\n"
        r".*?"
        r"Именно здесь MCP ложится естественно\.\n\n",
        author_case + "\n\n",
        "AlbumentationsX MCP author case",
    )

    bibliography = """#### Авторский кейс AlbumentationsX MCP

**S123.** [Albumentations, AlbumentationsX MCP integration](https://albumentations.ai/docs/integrations/mcp/), дата обращения: 30 августа 2026 года.
**S124.** [GitHub, dKosarevsky/albu-mcp v1.21.1](https://github.com/dKosarevsky/albu-mcp/releases/tag/v1.21.1) и [снимок исходного кода 171e2ca](https://github.com/dKosarevsky/albu-mcp/tree/171e2ca44830a16c363c8e3614825f2a0d2215b8), дата обращения: 30 августа 2026 года.

"""
    text = _replace_editorial_anchor(
        text,
        "### Дополнительное чтение",
        bibliography + "### Дополнительное чтение",
        "sources S123-S124",
    )
    text = _append_unique_chapter_sources(
        text,
        11,
        (
            "**S123.** Albumentations, AlbumentationsX MCP integration.",
            "**S124.** GitHub, dKosarevsky/albu-mcp v1.21.1 and source snapshot 171e2ca.",
        ),
    )
    return re.sub(r"\n{4,}", "\n\n", text).rstrip() + "\n"
```

Call it immediately after the existing final polish pass inside `revise()`:

```python
    text = apply_technical_book_polish_2026_08_02(text)
    text = apply_albumentationsx_mcp_author_case_2026_08_30(text)
    text = "\n".join(line.rstrip() for line in text.splitlines()) + "\n"
```

- [ ] **Step 4: Regenerate the canonical publisher manuscript**

Run:

```bash
uv run python docs/publisher/tools/revise_ru_manuscript.py \
  docs/publisher/ru-manuscript-google-doc-final-2026-07-11.md \
  docs/publisher/ru-manuscript-editorial-2026-07-13.md \
  --manifest docs/publisher/ru-inline-diagrams-2026-07-13.json
```

Expected: exit code 0; the canonical manuscript contains the case once. The diagram manifest remains byte-identical because this pass runs after diagram extraction.

- [ ] **Step 5: Run the focused publisher and reproducibility tests**

Run:

```bash
uv run pytest \
  tests/test_ru_manuscript_revision.py::test_albumentationsx_mcp_author_case_is_transparent_in_publisher_chapter \
  tests/test_ru_manuscript_revision.py::test_revision_is_reproducible \
  -v
```

Expected: 2 passed.

- [ ] **Step 6: Confirm that structural budgets did not change**

Run:

```bash
uv run pytest tests/test_ru_manuscript_revision.py \
  -k "gateway_discovery_sync_has_practice_sources_and_density_guards or every_manuscript_table_has_a_numbered_caption or reader_experience_pass or albumentationsx_mcp_author_case" \
  -v
```

Expected: all selected tests pass; Chapter 11 remains at or below its 4,985-word baseline and at or below 17 level-four headings.

- [ ] **Step 7: Commit the publisher projection**

```bash
git add tests/test_ru_manuscript_revision.py \
  docs/publisher/tools/revise_ru_manuscript.py \
  docs/publisher/ru-manuscript-editorial-2026-07-13.md
git commit -m "docs: sync AlbumentationsX MCP case to manuscript"
```

Do not stage the pre-existing publisher workflow, learning-outcome map, `.tmp`, DOCX, PDF, or QA artifact changes.

### Task 3: Run repository-level verification

**Files:**
- Verify only; no planned modifications.

- [ ] **Step 1: Run the complete documentation surface suite**

```bash
uv run pytest tests/test_docs_surface.py -q
```

Expected: PASS.

- [ ] **Step 2: Run the complete Russian manuscript revision suite**

```bash
uv run pytest tests/test_ru_manuscript_revision.py -q
```

Expected: PASS.

- [ ] **Step 3: Run publisher rendering regression tests**

```bash
uv run pytest tests/test_publisher_docx.py -q
```

Expected: PASS without changing generated DOCX or PDF files.

- [ ] **Step 4: Run focused static checks**

```bash
uv run ruff check \
  docs/publisher/tools/revise_ru_manuscript.py \
  tests/test_docs_surface.py \
  tests/test_ru_manuscript_revision.py
uv run ruff format --check \
  docs/publisher/tools/revise_ru_manuscript.py \
  tests/test_docs_surface.py \
  tests/test_ru_manuscript_revision.py
```

Expected: both commands pass.

- [ ] **Step 5: Build the multilingual site strictly**

```bash
uv run mkdocs build --strict
```

Expected: exit code 0 with no broken links or missing footnotes.

- [ ] **Step 6: Run the full test suite**

```bash
uv run pytest -q
```

Expected: PASS.

- [ ] **Step 7: Audit the final diff and working tree**

```bash
git diff --check
git status --short
git log -4 --oneline
```

Expected: no whitespace errors; only the pre-existing unrelated files remain modified or untracked; the two implementation commits appear above the design and plan commits.
