# Auditoria previa del servidor

## Resumen
- HEAD servidor: `c9f496c1402fc0d6983c03b020816356f424ef2f` (segun captura).
- `origin/main`: coincide con HEAD en la captura.
- Worktree servidor limpio: `False`.
- Borrados bajo `tesis-rag/documentos`: 89.
- Untracked bajo `tesis-rag/documentos`: 0.
- Health status: `ok`.
- Chroma health chunks: `591`.
- Ollama: `ok`; modelos: `{'chat': 'llama3.1:8b', 'embedding': 'nomic-embed-text'}`.

## Hallazgo operativo
El servidor esta sano para lectura, pero no esta limpio para una escritura de indice: conserva cambios locales sin commit en `tesis-rag/documentos` y reportes untracked. Por tanto cualquier correccion de Chroma debe tener backup previo y quedar documentada; un deploy por `git pull` no es suficiente mientras el worktree siga dirty.

## Captura cruda
```text
## git status -sb
## main...origin/main
 D tesis-rag/documentos/no_indexar/desde_gestor/01_contenido_canonico.md
 D tesis-rag/documentos/no_indexar/desde_gestor/e2_l01_another_trap.json
 D tesis-rag/documentos/no_indexar/desde_gestor/e2_l01_e2_l01_guia_practica_hpf_lpf.json
 D tesis-rag/documentos/no_indexar/desde_gestor/e2_l01_e2_l01_guia_practica_hpf_lpf.pdf
 D tesis-rag/documentos/no_indexar/desde_gestor/e3_l01_e3_l01_guia_practica_bell_shelving.json
 D tesis-rag/documentos/no_indexar/desde_gestor/e3_l01_e3_l01_guia_practica_bell_shelving.pdf
 D tesis-rag/documentos/no_indexar/desde_gestor/e4_l01_e4_l01_guia_practica_threshold_ratio_knee.json
 D tesis-rag/documentos/no_indexar/desde_gestor/e4_l01_e4_l01_guia_practica_threshold_ratio_knee.pdf
 D tesis-rag/documentos/no_indexar/modulo_01_fundamentos_acustica_medicion/M01_actividades.json
 D tesis-rag/documentos/no_indexar/modulo_01_fundamentos_acustica_medicion/M01_dossier_fuente.md
 D tesis-rag/documentos/no_indexar/modulo_01_fundamentos_acustica_medicion/M01_errores_comunes.json
 D tesis-rag/documentos/no_indexar/modulo_01_fundamentos_acustica_medicion/M01_faq.json
 D tesis-rag/documentos/no_indexar/modulo_01_fundamentos_acustica_medicion/M01_glosario.json
 D tesis-rag/documentos/no_indexar/modulo_01_fundamentos_acustica_medicion/M01_guia_canonica.md
 D tesis-rag/documentos/no_indexar/modulo_01_fundamentos_acustica_medicion/M01_recursos.json
 D tesis-rag/documentos/no_indexar/modulo_01_fundamentos_acustica_medicion/paqueteM01.md
 D tesis-rag/documentos/no_indexar/modulo_01_fundamentos_acustica_medicion/temarioPablo.md
 D tesis-rag/documentos/no_indexar/modulo_02_estructura_ganancia_flujo_senal/M02_actividades.json
 D tesis-rag/documentos/no_indexar/modulo_02_estructura_ganancia_flujo_senal/M02_dossier_fuente.md
 D tesis-rag/documentos/no_indexar/modulo_02_estructura_ganancia_flujo_senal/M02_errores_comunes.json
 D tesis-rag/documentos/no_indexar/modulo_02_estructura_ganancia_flujo_senal/M02_faq.json
 D tesis-rag/documentos/no_indexar/modulo_02_estructura_ganancia_flujo_senal/M02_glosario.json
 D tesis-rag/documentos/no_indexar/modulo_02_estructura_ganancia_flujo_senal/M02_guia_canonica.md
 D tesis-rag/documentos/no_indexar/modulo_02_estructura_ganancia_flujo_senal/M02_recursos.json
 D tesis-rag/documentos/no_indexar/modulo_03_polaridad_fase_monocompatibilidad/M03_actividades.json
 D tesis-rag/documentos/no_indexar/modulo_03_polaridad_fase_monocompatibilidad/M03_dossier_fuente.md
 D tesis-rag/documentos/no_indexar/modulo_03_polaridad_fase_monocompatibilidad/M03_errores_comunes.json
 D tesis-rag/documentos/no_indexar/modulo_03_polaridad_fase_monocompatibilidad/M03_faq.json
 D tesis-rag/documentos/no_indexar/modulo_03_polaridad_fase_monocompatibilidad/M03_glosario.json
 D tesis-rag/documentos/no_indexar/modulo_03_polaridad_fase_monocompatibilidad/M03_guia_canonica.md
 D tesis-rag/documentos/no_indexar/modulo_03_polaridad_fase_monocompatibilidad/M03_recursos.json
 D tesis-rag/documentos/no_indexar/modulo_04_filtros_ecualizacion/M04_actividades.json
 D tesis-rag/documentos/no_indexar/modulo_04_filtros_ecualizacion/M04_dossier_fuente.md
 D tesis-rag/documentos/no_indexar/modulo_04_filtros_ecualizacion/M04_errores_comunes.json
 D tesis-rag/documentos/no_indexar/modulo_04_filtros_ecualizacion/M04_faq.json
 D tesis-rag/documentos/no_indexar/modulo_04_filtros_ecualizacion/M04_glosario.json
 D tesis-rag/documentos/no_indexar/modulo_04_filtros_ecualizacion/M04_guia_canonica.md
 D tesis-rag/documentos/no_indexar/modulo_04_filtros_ecualizacion/M04_recursos.json
 D tesis-rag/documentos/no_indexar/modulo_05_procesadores_dinamicos/M05_actividades.json
 D tesis-rag/documentos/no_indexar/modulo_05_procesadores_dinamicos/M05_dossier_fuente.md
 D tesis-rag/documentos/no_indexar/modulo_05_procesadores_dinamicos/M05_errores_comunes.json
 D tesis-rag/documentos/no_indexar/modulo_05_procesadores_dinamicos/M05_faq.json
 D tesis-rag/documentos/no_indexar/modulo_05_procesadores_dinamicos/M05_glosario.json
 D tesis-rag/documentos/no_indexar/modulo_05_procesadores_dinamicos/M05_guia_canonica.md
 D tesis-rag/documentos/no_indexar/modulo_05_procesadores_dinamicos/M05_recursos.json
 D tesis-rag/documentos/no_indexar/modulo_06_espacialidad_profundidad_ambiencia/M06_actividades.json
 D tesis-rag/documentos/no_indexar/modulo_06_espacialidad_profundidad_ambiencia/M06_dossier_fuente.md
 D tesis-rag/documentos/no_indexar/modulo_06_espacialidad_profundidad_ambiencia/M06_errores_comunes.json
 D tesis-rag/documentos/no_indexar/modulo_06_espacialidad_profundidad_ambiencia/M06_faq.json
 D tesis-rag/documentos/no_indexar/modulo_06_espacialidad_profundidad_ambiencia/M06_glosario.json
 D tesis-rag/documentos/no_indexar/modulo_06_espacialidad_profundidad_ambiencia/M06_guia_canonica.md
 D tesis-rag/documentos/no_indexar/modulo_06_espacialidad_profundidad_ambiencia/M06_recursos.json
 D tesis-rag/documentos/no_indexar/modulo_07_practica_integradora_mezcla/M07_actividades.json
 D tesis-rag/documentos/no_indexar/modulo_07_practica_integradora_mezcla/M07_dossier_fuente.md
 D tesis-rag/documentos/no_indexar/modulo_07_practica_integradora_mezcla/M07_errores_comunes.json
 D tesis-rag/documentos/no_indexar/modulo_07_practica_integradora_mezcla/M07_faq.json
 D tesis-rag/documentos/no_indexar/modulo_07_practica_integradora_mezcla/M07_glosario.json
 D tesis-rag/documentos/no_indexar/modulo_07_practica_integradora_mezcla/M07_guia_canonica.md
 D tesis-rag/documentos/no_indexar/modulo_07_practica_integradora_mezcla/M07_recursos.json
 D tesis-rag/documentos/no_indexar/modulo_08_masterizacion_optimizacion_comercial/M08_actividades.json
 D tesis-rag/documentos/no_indexar/modulo_08_masterizacion_optimizacion_comercial/M08_dossier_fuente.md
 D tesis-rag/documentos/no_indexar/modulo_08_masterizacion_optimizacion_comercial/M08_errores_comunes.json
 D tesis-rag/documentos/no_indexar/modulo_08_masterizacion_optimizacion_comercial/M08_faq.json
 D tesis-rag/documentos/no_indexar/modulo_08_masterizacion_optimizacion_comercial/M08_glosario.json
 D tesis-rag/documentos/no_indexar/modulo_08_masterizacion_optimizacion_comercial/M08_guia_canonica.md
 D tesis-rag/documentos/no_indexar/modulo_08_masterizacion_optimizacion_comercial/M08_recursos.json
 D tesis-rag/documentos/oficial/curso_2/seccion_02_leer_la_senal/contenido_canonico.md
 D tesis-rag/documentos/oficial/curso_2/seccion_03_integridad_de_la_senal/contenido_canonico.md
 D tesis-rag/documentos/oficial/curso_2/seccion_04_identidad_espectral/contenido_canonico.md
 D tesis-rag/documentos/oficial/curso_2/seccion_05_energia_y_movimiento/contenido_canonico.md
 D tesis-rag/documentos/oficial/curso_2/seccion_07_integracion_global/contenido_canonico.md
 D tesis-rag/documentos/oficial/curso_2/seccion_08_traduccion_y_entrega/contenido_canonico.md
 D tesis-rag/documentos/oficial/guiones/piloto.md
 D tesis-rag/documentos/oficial/guiones/v1/Eje0_Guiones_KENTH.md
 D tesis-rag/documentos/oficial/guiones/v1/Eje1_Guiones_KENTH.md
 D tesis-rag/documentos/oficial/guiones/v1/Eje2_Guiones_KENTH.md
 D tesis-rag/documentos/oficial/guiones/v1/Eje3_Guiones_KENTH.md
 D tesis-rag/documentos/oficial/guiones/v1/Eje4_Guiones_KENTH.md
 D tesis-rag/documentos/oficial/guiones/v1/Eje5_Guiones_KENTH.md
 D tesis-rag/documentos/oficial/guiones/v1/Eje6_Guiones_KENTH.md
 D tesis-rag/documentos/oficial/guiones/v1/Eje7_Guiones_KENTH.md
 D tesis-rag/documentos/oficial/guiones/v2/Eje0_Guiones_KENTH_v2.md
 D tesis-rag/documentos/oficial/guiones/v2/Eje1_Guiones_KENTH_v2.md
 D tesis-rag/documentos/oficial/guiones/v2/Eje2_Guiones_KENTH_v2.md
 D tesis-rag/documentos/oficial/guiones/v2/Eje3_Guiones_KENTH_v2.md
 D tesis-rag/documentos/oficial/guiones/v2/Eje4_Guiones_KENTH_v2.md
 D tesis-rag/documentos/oficial/guiones/v2/Eje5_Guiones_KENTH_v2.md
 D tesis-rag/documentos/oficial/guiones/v2/Eje6_Guiones_KENTH_v2.md
 D tesis-rag/documentos/oficial/guiones/v2/Eje7_Guiones_KENTH_v2.md
?? reports/alineacion_corpus_20260705_104116/
?? reports/ingesta_seccion0_lessons_20260705_145139/
?? reports/ingesta_seccion_0_20260705_033332/
?? reports/reconcile_untracked_seccion_00_before_c9f496c/

## git log --oneline -5
c9f496c chore(corpus): completa ingesta de seccion 0
396cf86 Merge branch 'chore/corpus-canonical-cleanup': limpia documentos antiguos y unifica ubicación canónica del corpus
e4dbf17 chore(corpus): limpia documentos antiguos y unifica ubicación canónica del corpus
8042271 Merge pull request #11 from nosoykenneth/corpus/seccion-0-ingesta
24750cb Merge pull request #10 from nosoykenneth/fix/rag-ingest-flags-visible-sources

## HEAD
c9f496c1402fc0d6983c03b020816356f424ef2f

## origin/main
c9f496c1402fc0d6983c03b020816356f424ef2f

## docker compose ps
NAME              IMAGE                                                                     COMMAND                  SERVICE       CREATED          STATUS                PORTS
tic-fastapi       tic-kenth/fastapi:latest                                                  "uvicorn main:app --…"   fastapi       34 minutes ago   Up 34 minutes         8000/tcp
tic-frontend      tic-kenth/frontend:latest                                                 "sh -c 'rm -rf /shar…"   frontend      3 hours ago      Up 3 hours            
tic-gateway       nginx:alpine                                                              "/docker-entrypoint.…"   gateway       2 days ago       Up 35 minutes         0.0.0.0:8090->80/tcp, [::]:8090->80/tcp
tic-grafana       grafana/grafana:10.4.0                                                    "/run.sh"                grafana       5 days ago       Up 5 days             127.0.0.1:3000->3000/tcp
tic-loki          grafana/loki:2.9.0                                                        "/usr/bin/loki -conf…"   loki          5 days ago       Up 5 days             3100/tcp
tic-mariadb       mariadb:11.4                                                              "docker-entrypoint.s…"   mariadb       6 days ago       Up 6 days (healthy)   3306/tcp
tic-moodle        tic-kenth/moodle:5.0-real                                                 "/usr/local/bin/mood…"   moodle        2 days ago       Up 2 days             80/tcp, 0.0.0.0:8091->8080/tcp, [::]:8091->8080/tcp
tic-moodle-cron   sha256:3009f2cd8631755ce67d6e1464ea5debf8f1c9491646f6d6a26550391cefd343   "sh -c 'while true; …"   moodle-cron   5 days ago       Up 5 days             80/tcp, 8080/tcp
tic-promtail      grafana/promtail:2.9.0                                                    "/usr/bin/promtail -…"   promtail      5 days ago       Up 5 days             

## health
{"status":"ok","fastapi":"ok","moodle_db":"ok","moodle_ws":"ok","chroma":"ok","ollama":"ok","models":{"chat":"llama3.1:8b","embedding":"nomic-embed-text"},"details":{"chroma_chunks":591,"ollama_models_present":{"chat":true,"embedding":true},"db_backend":"moodle"}}
```
