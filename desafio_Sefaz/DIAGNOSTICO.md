| Code smell                                 | Local                     | Problema                                                                                      |
| ------------------------------------------ | ------------------------- | --------------------------------------------------------------------------------------------- |
| **Long Method / muitas responsabilidades** | `05_gerar_indicadores.py` | `gerar_indicadores()` realiza várias etapas do pipeline em uma única função                   |
| **Long Method / baixa coesão**             | `03_tratar_dados.py`      | `tratar_dados()` mistura leitura, limpeza, transformação, correções, persistência e relatório |
| **Tratamento de erro insuficiente**        | `01_extrair_dados.py`     | extração de ZIP não trata arquivo corrompido ou erro de I/O                                   |
