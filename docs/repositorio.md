# Repositorio y publicación del proyecto

Estado vigente: **2 de noviembre de 2026**. Origin actual: **https://github.com/eldanielh31/mumai**, público por confirmación expresa de Daniel, incluidos los videos del motor. **No hacer commit ni push salvo solicitud explícita de Daniel.** Las notas anteriores de privacidad y publicación automática que siguen se conservan como historial y quedan sustituidas por esta decisión.

Registro histórico del 1 de noviembre de 2026:

- Cuenta autenticada: `eldanielh31`.
- Repositorio creado y privacidad comprobada mediante API: **privado**.
- URL: https://github.com/eldanielh31/Generacion-de-sistema-de-identificacion-de-danos-en-maquinaria-usando-magnificacion-Euleriana-e-IA
- El nombre conserva el título del proyecto con “IA” como abreviatura y sin tildes en la URL.
- Remoto local: `origin`, HTTPS; rama `main`.
- Publicación verificada el 1 de noviembre de 2026: commit `c3842af2f4d3818be937a2a6961d09f46a8eca7c` presente en `main` remoto. Esta anotación se enviará en un commit documental posterior.

## Contenido autorizado

Código, dependencias, pruebas, scripts, historial Git, documentación técnica, evidencias sintéticas y todos los documentos de `Proyecto/`. Se preservan los originales académicos. Daniel autorizó explícitamente el 1/11/2026 publicar `data/input/`, incluidos motor.mp4 y motor_30fps.avi. Los ocho videos de entrada se almacenan mediante Git LFS; los cinco JSON de referencias se versionan normalmente. `data/output/` sigue excluido salvo su marcador vacío .gitkeep. Entornos y credenciales permanecen excluidos. Para obtener los videos después de clonar, instalar Git LFS y ejecutar `git lfs install` y `git lfs pull`.

## Continuidad

GitHub CLI está instalado en `/home/daniel/.local/bin/gh` y autenticado por Daniel. Git utiliza esa autenticación para este repositorio; no hay tokens en archivos versionados. Cada entrega debe documentarse, probarse, guardarse en un commit y enviarse; verificar que `origin/main` coincide con `HEAD`. No hay sincronización automática en segundo plano.

El estado del 21 de octubre (sin conexión) se conserva en el historial Git. La revisión del 1 de noviembre está en [revision-2026-11-01/README.md](revision-2026-11-01/README.md).

## Verificación del remoto actual — 2 de noviembre de 2026

En la copia WSL `/home/danbg/mumai`, origin es
`https://github.com/eldanielh31/mumai.git`, distinto del nombre histórico indicado
arriba. La API pública de GitHub devuelve `private: false`, `visibility: public`.
Véase [registro](pru02-2026-11-02/remoto.json). Se mantiene esta diferencia explícita;
la publicación de PRU-02 queda pendiente de aclarar la visibilidad con Daniel.
No se cambió la privacidad ni se enviaron los cambios de esta sesión.

### Decisión posterior de Daniel — 2 de noviembre

Daniel confirma mantener público el remoto actual y los videos del motor. REP-002
queda resuelto mediante autorización explícita de esa visibilidad. Además, ordena
no hacer commit ni push hasta que lo solicite expresamente. Esta decisión sustituye
la publicación al final de cada entrega. En PRU-02 no se ejecutaron commit ni push.
Véase [confirmaciones](pru02-2026-11-02/confirmaciones-daniel.json).
