# Procedencia del catálogo CIE-10

`cie10_catalog.json` contiene 11.008 códigos únicos y sus descripciones en español.
Se obtuvo del archivo `cie10_master.json` proporcionado por el responsable del proyecto, generado previamente a partir de `CIE-10.pdf`.
Se conservaron los códigos y descripciones; únicamente se transformó la lista en un índice JSON de código a descripción.

Huellas SHA-256 de las fuentes proporcionadas:

- JSON: `5ac8d47a4c27b68ede88a5b82f97b67a71ba67e2fe74b4ed37c51f08fa73ff1b`
- PDF: `07acd64eff54018522af5cbd656732348baa534a17b7eb93e8aab2650cfd40b8`

El índice incluye categorías de tres caracteres y subcategorías de cuatro. La normalización admite minúsculas, espacios en los extremos y ausencia de punto decimal: `i219` pasa a `I21.9`.

La validación comprueba pertenencia al catálogo, no correspondencia clínica. No se realizan coincidencias aproximadas ni se sustituyen códigos desconocidos por categorías más generales. No se afirma que este índice represente todas las modificaciones nacionales ni la edición más reciente.

Para actualizarlo, utilizar una fuente aprobada, conservar su procedencia y ejecutar las pruebas del catálogo.
