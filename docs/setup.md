# Configuración inicial del entorno de trabajo

Este documento describe los pasos necesarios para preparar el entorno de desarrollo que se utilizará durante el proyecto.

## Terminal utilizada durante el proyecto

Durante este proyecto se utilizará **Git Bash**, el cual se instala automáticamente junto con Git para Windows.

La mayoría de los ejemplos y comandos mostrados en esta guía deberán ejecutarse desde Git Bash.

Para abrir Git Bash:

* Menú Inicio → Git Bash

La terminal mostrará una ventana similar a un entorno Linux, lo que facilitará el uso de herramientas y ejemplos que se utilizarán durante el proyecto.

## 1. Instalar Python

Descargar e instalar Python 3.11 desde:

https://www.python.org/downloads/

Durante la instalación en Windows, activar la opción:

* Add Python to PATH

Verificar la instalación abriendo una terminal (PowerShell o CMD):

```bash
py --version
```

Deberá mostrarse una versión similar a:

```text
Python 3.11.x
```

---

## 2. Instalar Visual Studio Code

Descargar e instalar Visual Studio Code:

https://code.visualstudio.com/

Extensiones recomendadas:

* Python (Microsoft)
* GitHub Pull Requests and Issues (opcional)

Verificar que VSCode pueda abrir archivos y carpetas normalmente.

---

## 3. Instalar Git

Descargar e instalar Git para Windows:

https://git-scm.com/download/win

Después de la instalación, abrir una terminal Git Bash y verificar:

```bash
git --version
```

Deberá mostrarse una versión similar a:

```text
git version 2.x.x
```

---

## 4. Crear una cuenta de GitHub

Si aún no se cuenta con una cuenta, registrarse en:

https://github.com/

Guardar el nombre de usuario seleccionado, ya que será necesario para acceder al repositorio del proyecto.

## Activar autenticación de dos factores (2FA)

GitHub requiere autenticación de dos factores para proteger las cuentas.

Se recomienda utilizar la aplicación GitHub Mobile.

Una vez configurada la cuenta:

1. Ir a Settings.
2. Seleccionar Password and authentication.
3. Activar Two-factor authentication.
4. Seguir las instrucciones mostradas por GitHub.
5. Guardar los códigos de recuperación en un lugar seguro.

---

## 5. Configurar Git

Abrir **Git Bash** y ejecutar:

```bash
git config --global user.name "Nombre Apellido"
git config --global user.email "correo@ejemplo.com"
```

Verificar la configuración:

```bash
git config --list
```

Confirmar que aparecen los campos:

```text
user.name
user.email
```

---
## 6. Generar una llave SSH

GitHub utilizará autenticación mediante SSH para acceder al repositorio del proyecto.

Abrir **Git Bash** y ejecutar:

```bash
ssh-keygen -t ed25519
```

Presionar ENTER para aceptar las opciones predeterminadas.

Los archivos generados normalmente se almacenarán en:

```text
~/.ssh/
```

y deberán existir los archivos:

```text
id_ed25519
id_ed25519.pub
```

---
## 7. Mostrar la llave pública

Abrir **Git Bash** y ejecutar:

```bash
cat ~/.ssh/id_ed25519.pub
```

Se mostrará un texto similar a:

```text
ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAA...
```

Copiar todo el contenido mostrado.

---

## 8. Registrar la llave en GitHub

Ingresar a GitHub:

Settings → SSH and GPG Keys → New SSH Key

Pegar el contenido de la llave pública y guardar.

---

## 9. Verificar la conexión

Abrir **Git Bash** y ejecutar:

```bash
ssh -T git@github.com
```

La primera vez aparecerá una pregunta para confirmar la conexión.

Responder:

```text
yes
```

Si todo funciona correctamente se mostrará un mensaje similar a:

```text
Hi usuario! You've successfully authenticated...
```

---

## 10. Acceder al repositorio del proyecto

Abrir **Git Bash**.

Antes de descargar el repositorio, navegar al directorio donde deseas almacenarlo. Por ejemplo, si deseas guardarlo dentro de la carpeta *Documentos*:

```bash
cd ~/Documents
```

Para verificar tu ubicación actual puedes utilizar:

```bash
pwd
```

Y para listar el contenido del directorio actual:

```bash
ls
```

Una vez ubicado en el directorio deseado, clonar el repositorio:

```bash
git clone git@github.com:afranco-astro/verano-2026.git
```

Entrar al directorio del proyecto:

```bash
cd verano-2026
```

Verificar que el repositorio remoto fue configurado correctamente:

```bash
git remote -v
```

Deberá mostrarse algo similar a:

```text
origin  git@github.com:afranco-astro/verano-2026.git (fetch)
origin  git@github.com:afranco-astro/verano-2026.git (push)
```

Verificar la configuración de Git:

```bash
git config --list
```

Confirmar que aparecen los valores configurados previamente para:

```text
user.name
user.email
```

Abrir el proyecto en Visual Studio Code:

```bash
code .
```

Verificar que la carpeta del proyecto se abre correctamente y que los archivos del repositorio son visibles desde VSCode.

---

## 11. Primer commit

Crear el archivo:

```text
docs/student_background.md
```

con el siguiente contenido:

```markdown
# Antecedentes del estudiante

## Experiencia previa

### Programación

-
-

## Herramientas instaladas

-
-

## Intereses relacionados con el proyecto

-
-
-

## Objetivos para este verano

-
-
-

## Dudas o comentarios iniciales

-
-
-
```

Guardar el archivo y posteriormente ejecutar:

```bash
git add docs/student_background.md
git commit -m "Add student background"
git push
```

### Objetivo de esta actividad

* Verificar que Git y GitHub funcionan correctamente.
* Confirmar acceso al repositorio compartido.
* Documentar la experiencia e intereses iniciales del estudiante.
* Familiarizarse con el flujo básico de trabajo utilizando Git.
