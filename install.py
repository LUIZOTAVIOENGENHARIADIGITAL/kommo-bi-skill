#!/usr/bin/env python3
"""Instala somente a skill local. Não acessa rede, CRM ou credenciais."""
import argparse
from datetime import datetime, timezone
from pathlib import Path
import shutil
import sys
import tempfile

SOURCE = Path(__file__).resolve().parent / "skills" / "kommo-bi"


def inventory(root):
    files = {}
    for path in sorted(root.rglob("*")):
        if path.is_symlink():
            raise ValueError(f"Link simbólico não suportado: {path}")
        if path.is_file():
            files[str(path.relative_to(root))] = path.read_bytes()
    return files


def destinations(agent, root, legacy=False):
    targets = []
    if agent in ("codex", "both"):
        targets.append(root / (".codex" if legacy else ".agents") / "skills" / "kommo-bi")
    if agent in ("claude", "both"):
        targets.append(root / ".claude" / "skills" / "kommo-bi")
    return targets


def install(targets, update=False, dry_run=False, source=SOURCE):
    if not (source / "SKILL.md").is_file():
        raise ValueError("SKILL.md não encontrado. Execute a partir de uma cópia completa do repositório.")
    expected = inventory(source)
    pending = []
    # Verifica todos os destinos antes de modificar qualquer instalação.
    for dest in targets:
        if dest.is_symlink():
            raise ValueError(f"Destino é link simbólico; preserve e ajuste manualmente: {dest}")
        if dest.exists():
            if not dest.is_dir():
                raise ValueError(f"Destino não é uma pasta: {dest}")
            if inventory(dest) == expected:
                print(f"Já atualizado: {dest}")
                continue
            if not update:
                raise ValueError(f"Skill existente preservada: {dest}. Use --update para atualizar com backup.")
        pending.append(dest)
    for dest in pending:
        if dry_run:
            print(f"Simulação: {'atualizar com backup' if dest.exists() else 'instalar'} {dest}")
            continue
        dest.parent.mkdir(parents=True, exist_ok=True)
        backup = None
        with tempfile.TemporaryDirectory(prefix=".kommo-bi-stage-", dir=dest.parent) as stage:
            staged = Path(stage) / "kommo-bi"
            shutil.copytree(source, staged)
            if dest.exists():
                stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
                # Fora de skills/, para o agente não carregar uma segunda cópia.
                backup_root = dest.parent.parent / "skill-backups"
                backup_root.mkdir(exist_ok=True)
                backup = backup_root / f"kommo-bi-{stamp}"
                dest.rename(backup)
            try:
                staged.rename(dest)
            except OSError:
                if backup is not None:
                    backup.rename(dest)
                raise
        if backup:
            print(f"Backup: {backup}")
        print(f"Instalado: {dest}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--agent", choices=["codex", "claude", "both"], required=True)
    parser.add_argument("--scope", choices=["user", "project"], default="user")
    parser.add_argument("--project-dir", type=Path, help="Obrigatório para --scope project")
    parser.add_argument("--codex-legacy", action="store_true", help="Usar ~/.codex/skills em instalações antigas")
    parser.add_argument("--update", action="store_true", help="Atualizar preservando backup da versão anterior")
    parser.add_argument("--dry-run", action="store_true", help="Mostrar destinos sem alterar arquivos")
    args = parser.parse_args()
    if args.scope == "project" and args.project_dir is None:
        parser.error("Informe --project-dir para instalar em um projeto.")
    if args.scope == "user" and args.project_dir is not None:
        parser.error("--project-dir requer --scope project.")
    if args.codex_legacy and args.agent == "claude":
        parser.error("--codex-legacy só se aplica ao Codex.")
    root = Path.home() if args.scope == "user" else args.project_dir.expanduser().resolve()
    if args.scope == "project" and not root.is_dir():
        parser.error("A pasta do projeto precisa existir.")
    try:
        install(destinations(args.agent, root, args.codex_legacy), args.update, args.dry_run)
    except (ValueError, OSError) as exc:
        print(f"Erro: {exc}", file=sys.stderr)
        return 1
    print("Abra uma nova sessão. Codex: $kommo-bi | Claude Code: /kommo-bi")
    return 0


if __name__ == "__main__":
    sys.exit(main())
