# CIE-10 Edu

[English](README.md) | **Español**

Mini laboratorio educativo de codificación médica con **Gemma 4** y un catálogo de 11.008 códigos CIE-10. Una pantalla, sin instalación de paquetes ni base de datos.

## Qué hace

- Analiza texto o imágenes PNG/JPEG/WebP de casos ficticios.
- Gemma propone códigos y explica la evidencia, resume y genera tres preguntas con respuestas desplegables.
- El servidor normaliza códigos (por ejemplo `I219` → `I21.9`) y contrasta su pertenencia con 11.008 entradas del catálogo. La descripción mostrada proviene del catálogo, no del modelo.
- Incluye un validador local independiente de IA y tres ejemplos ficticios.
- Prepara imágenes en el navegador: máximo 1280 px, JPEG calidad 80 y reducción adaptativa a menos de 350.000 bytes de Base64 incluyendo prefijo.
- Permite copiar el resultado. No guarda los casos en el servidor.

## Ejecutar

Requiere Python 3.11 o superior y una clave con acceso a Gemma 4 en la API Gemini.

```powershell
Copy-Item .env.example .env
# Edita .env y coloca tu GEMINI_API_KEY. Este archivo está ignorado por Git.
python server.py
```

Abre http://127.0.0.1:8091. No necesitas npm, Docker, PostgreSQL ni dependencias de Python externas. La clave permanece en el servidor. Usa únicamente datos sintéticos: el texto y la imagen se envían a Google para su procesamiento. No publiques este servidor de demostración en Internet: escucha solo en localhost y no incluye autenticación ni limitación de solicitudes.

Modelo predeterminado `gemma-4-26b-a4b-it`; también se admite `gemma-4-31b-it`. Sin acceso al modelo o cuota, se informa el error: no se reemplaza silenciosamente por Gemini ni por respuestas simuladas. Usa la [documentación oficial de Gemma en Gemini API](https://ai.google.dev/gemma/docs/core/gemma_on_gemini_api) para configurar el acceso.

## Demostración de dos minutos

1. Introduce `i219` en el validador local: muestra código y descripción canónicos.
2. Pulsa el ejemplo Neumonía y crea una sesión: revisa resumen, J18.9 y preguntas.
3. Abre las respuestas después de intentar contestarlas.
4. Prueba Texto ambiguo: el resultado no debe inventar un diagnóstico confirmado.
5. Prueba una imagen sintética clara, sin datos de pacientes.

Puedes usar `examples/caso_neumonia.png`, una imagen generada con texto ficticio para la demostración.

## Pruebas

```powershell
python -m unittest discover -s tests -v
```

Las pruebas no consumen API ni utilizan una base de datos. Verifican normalización, catálogo, contrato de respuesta y entradas inválidas. Las llamadas reales dependen del acceso y cuota de la cuenta; no hay afirmación de precisión clínica ni de latencia garantizada.

### Verificación local del prototipo (31/10/2026)

- 14 pruebas automáticas aprobadas y JavaScript sin errores de sintaxis.
- Navegador real: validación local `i219`, caso de texto y caso de imagen sintética con Gemma 4, tres preguntas y respuestas desplegables.
- El ejemplo ambiguo no produjo códigos; no es una evaluación clínica general.
- Vista móvil de 390 px sin desbordamiento horizontal y sin errores de JavaScript durante la prueba.
- Entrada vacía rechazada con HTTP 422 y solicitudes de otro origen con HTTP 403.

Estas comprobaciones se realizaron con una clave autorizada solo en el entorno del proceso. No se incluye ninguna clave en el repositorio. No equivalen a una certificación clínica ni a pruebas bajo carga.

## Alcance y límites

Herramienta educativa, no sistema de diagnóstico, tratamiento o priorización clínica. Que un código exista no demuestra que corresponda al caso. Gemma puede equivocarse o interpretar mal una imagen; la compresión también puede reducir legibilidad. La evidencia textual y las preguntas son generadas por IA y requieren revisión. No hay PDF, historial persistente, login ni LangGraph en esta demo.

## Licencia y procedencia

El proyecto incorpora componentes adaptados bajo licencia MIT. Los avisos de copyright y las condiciones de uso se conservan en `LICENSE` y `NOTICE.md`. La procedencia del catálogo se documenta en `data/PROVENANCE.md`.

No se afirma que el catálogo represente todas las modificaciones nacionales ni la edición más reciente de CIE-10.
