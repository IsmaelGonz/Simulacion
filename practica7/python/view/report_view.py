"""Vista de informes de verificacion de reproducibilidad."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path

YES_NO = lambda value: "SI" if value else "NO"


def write_verification_report(verification: dict, path: Path) -> None:
    """Escribe el informe de texto de la verificacion de reproducibilidad."""
    lines = [
        "VERIFICACION DE REPRODUCIBILIDAD - APE 007",
        "=" * 60,
        f"Fecha de ejecucion: {datetime.now().isoformat(timespec='seconds')}",
        f"Pares verificados por el hash: {verification['pairs']} "
        f"({verification['pairs'] * 2} uniformes)",
        f"Pares mostrados en los CSV: {verification['shown_pairs']}",
        f"SHA-256 Python: {verification['hash_python']}",
        f"SHA-256 Java:   {verification['hash_java']}",
        f"Los hashes coinciden: {YES_NO(verification['same_hash'])}",
        f"Los primeros {verification['shown_pairs']} pares coinciden bit a bit: "
        f"{YES_NO(verification['same_first_pairs'])}",
        f"Nc coincide en los cuatro experimentos: {YES_NO(verification['same_nc'])}",
        f"pi estimado coincide en los cuatro experimentos: "
        f"{YES_NO(verification['same_pi'])}",
    ]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
